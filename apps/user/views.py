from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction

from extensions.permissions import IsAuthenticated, IsManagerPermission
from extensions.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated
from extensions.viewsets import ModelViewSetEx, FunctionViewSet
from apps.user.serializers import *
from apps.user.permissions import *
from apps.user.filters import *
from apps.user.schemas import *
from apps.user.models import *
from apps.product.models import *


class RoleViewSet(ModelViewSetEx):
    """角色"""

    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsManagerPermission]
    search_fields = ['name']
    ordering_fields = ['id', 'update_time']
    queryset = Role.objects.all()

    @transaction.atomic
    def perform_update(self, serializer):
        instance = serializer.save()

        # 更新用户权限
        user_set = instance.user_set.prefetch_related('role_set').all()
        for user in user_set:
            permissions = {permission for role in user.role_set.all() for permission in role.permissions}
            user.permissions = list(permissions)
        User.objects.bulk_update(user_set, ['permissions'])

    @transaction.atomic
    def perform_destroy(self, instance):
        user_set = instance.user_set.prefetch_related('role_set').all()
        super().perform_destroy(instance)

        # 更新用户权限
        for user in user_set:
            permissions = {permission for role in user.role_set.all() for permission in role.permissions}
            user.permissions = list(permissions)
        User.objects.bulk_update(user_set, ['permissions'])


class UserViewSet(ModelViewSetEx):
    """用户"""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManagerPermission]
    filterset_class = UserFilter
    search_fields = ['username', 'name']
    ordering_fields = ['id', 'username', 'update_time']
    prefetch_related_fields = ['warehouse_set', 'role_set']
    queryset = User.objects.all()

    def perform_destroy(self, instance):
        if instance.is_manager:
            raise ValidationError('无法删除管理员账号')
        super().perform_destroy(instance)

    @extend_schema(responses={204: None})
    @action(detail=True, methods=['post'])
    def reset_password(self, request, *args, **kwargs):
        """重置密码"""

        instance = self.get_object()
        instance.password = make_password(instance.username)
        instance.save(update_fields=['password'])
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserActionViewSet(FunctionViewSet):
    """用户操作"""

    @extend_schema(request=CreateTokenRequest, responses={200: CreateTokenResponse})
    @action(detail=False, methods=['post'])
    def create_token(self, request, *args, **kwargs):
        """创建令牌"""

        serializer = CreateTokenRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if not (user := User.objects.filter(username=validated_data['username']).first()):
            raise ValidationError('用户不存在')

        if not check_password(validated_data['password'], user.password):
            raise AuthenticationFailed('密码错误')

        token = RefreshToken()
        token['user_id'] = user.id

        data = {'access': str(token.access_token), 'refresh': str(token)}
        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(request=UpdateTokenRequest, responses={200: UpdateTokenResponse})
    @action(detail=False, methods=['post'])
    def update_token(self, request, *args, **kwargs):
        """更新令牌"""

        serializer = UpdateTokenRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            token = RefreshToken(validated_data['refresh'])
            token.blacklist()
            token.set_jti()
            token.set_exp()
            token.set_iat()
        except TokenError as e:
            raise ValidationError('令牌失效') from e

        data = {'access': str(token.access_token), 'refresh': str(token)}
        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(request=RevokeTokenRequest, responses={204: None})
    @action(detail=False, methods=['post'])
    def revoke_token(self, request, *args, **kwargs):
        """注销令牌"""

        serializer = RevokeTokenRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            token = RefreshToken(validated_data['refresh'])
            token.blacklist()
        except TokenError as e:
            raise NotAuthenticated('令牌失效') from e

        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses={200: UserInfoResponse})
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def info(self, request, *args, **kwargs):
        """用户信息"""

        serializer = UserInfoResponse(instance=self.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=SetPasswordRequest, responses={204: None})
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def set_password(self, request, *args, **kwargs):
        """设置密码"""

        serializer = SetPasswordRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if not check_password(validated_data['old_password'], self.user.password):
            raise AuthenticationFailed('密码错误')

        self.user.password = make_password(validated_data['new_password'])
        self.user.save(update_fields=['password'])

        return Response(status=status.HTTP_204_NO_CONTENT)


class WarehouseViewSet(ModelViewSetEx):
    """仓库"""

    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    filterset_fields = ['is_locked', 'is_active']
    search_fields = ['number', 'name']
    ordering_fields = ['id', 'number', 'update_time']
    queryset = Warehouse.objects.all()

    def get_queryset(self):
        return self.user.get_warehouse_set()

    @transaction.atomic
    def perform_create(self, serializer):
        instance = serializer.save()
        self.user.warehouse_set.add(instance)

        # 同步库存
        Inventory.objects.bulk_create([Inventory(warehouse=instance, product=product)
                                       for product in Product.objects.filter(include_deleted=True)])

    @extend_schema(responses={200: WarehouseSerializer})
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, WarehouseLockPermission])
    def lock(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_locked:
            raise ValidationError(f'仓库[{instance.name}] 已锁定')

        instance.is_locked = True
        instance.save(update_fields=['is_locked'])

        serializer = WarehouseSerializer(instance=instance, context=self.context)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: WarehouseSerializer})
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, WarehouseUnlockPermission])
    def unlock(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_locked:
            raise ValidationError(f'仓库[{instance.name}] 已解锁')

        # TODO: 盘点任务未完成无法解锁
        # if StockCheckOrder.objects.filter(warehouse=instance, status=TaskStatus.SUBMITTED).exists():
        #     raise ValidationError(f'仓库[{instance.name}]无法解锁, 盘点任务未完成')

        instance.is_locked = False
        instance.save(update_fields=['is_locked'])

        serializer = WarehouseSerializer(instance=instance, context=self.context)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


__all__ = [
    'RoleViewSet',
    'UserViewSet',
    'UserActionViewSet',
    'WarehouseViewSet',
]
