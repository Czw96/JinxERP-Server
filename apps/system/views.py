from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from django.http import FileResponse
from pathlib import Path
from django_tenants.utils import get_tenant

from extensions.permissions import IsAuthenticated, IsManagerPermission
from extensions.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated
from extensions.viewsets import ModelViewSetEx, FunctionViewSet, ArchiveViewSet, QueryViewSet, DestroyModelMixin
from apps.system.serializers import *
from apps.system.permissions import *
from apps.system.filters import *
from apps.system.schemas import *
from apps.system.models import *
from apps.product.models import *


class RoleViewSet(ModelViewSetEx):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsManagerPermission]
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name', 'update_time']
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


class UserViewSet(ArchiveViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManagerPermission]
    filterset_class = UserFilter
    search_fields = ['number', 'username', 'name', 'remark']
    ordering_fields = ['id', 'number', 'username', 'name' 'update_time', 'delete_time']
    prefetch_related_fields = ['warehouse_set', 'role_set']
    queryset = User.objects.all()

    def perform_destroy(self, instance):
        if instance.is_manager:
            raise ValidationError('管理员账号无法删除')
        super().perform_destroy(instance)

    def perform_batch_destroy(self, instance_set):
        if instance_set.filter(is_manager=True).exists():
            raise ValidationError('管理员账号无法删除')
        return super().perform_batch_destroy(instance_set)

    @extend_schema(responses={204: None})
    @action(detail=True, methods=['post'])
    def reset_password(self, request, *args, **kwargs):
        """重置密码"""

        instance = self.get_object()
        if instance.is_manager:
            raise ValidationError('管理员账号密码无法重置')

        instance.password = make_password(instance.username)
        instance.save(update_fields=['password'])
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserActionViewSet(FunctionViewSet):

    @extend_schema(request=CreateTokenRequest, responses={200: CreateTokenResponse})
    @action(detail=False, methods=['post'])
    def create_token(self, request, *args, **kwargs):
        """创建令牌"""

        serializer = CreateTokenRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if not (user := User.objects.filter(username=validated_data['username'], is_deleted=False).first()):
            raise ValidationError('用户不存在')

        if not check_password(validated_data['password'], user.password):
            raise AuthenticationFailed('密码错误')

        token = RefreshToken()
        tenant = get_tenant(request)
        token['user_id'] = user.id
        token['tenant_id'] = tenant.id

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

    @extend_schema(responses={200: UserProfileResponse})
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request, *args, **kwargs):
        """用户信息"""

        serializer = UserProfileResponse(instance=self.user)
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


class WarehouseViewSet(ArchiveViewSet):
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, WarehousePermission]
    filterset_fields = ['is_locked', 'is_active', 'is_deleted']
    search_fields = ['number', 'name', 'remark']
    ordering_fields = ['id', 'number', 'name', 'update_time', 'delete_time']
    queryset = Warehouse.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        instance = serializer.save()

        # 同步库存
        Inventory.objects.bulk_create([Inventory(warehouse=instance, product=product) for product in Product.objects.all()])

    @transaction.atomic
    def perform_destroy(self, instance):
        # 解除用户关联
        for user in instance.user_set.all():
            user.warehouse_set.remove(instance)
        return super().perform_destroy(instance)

    @extend_schema(responses={200: WarehouseSerializer})
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, WarehouseLockPermission])
    def lock(self, request, *args, **kwargs):
        """仓库锁定"""

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
        """仓库解锁"""

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


class ModelFieldViewSet(ArchiveViewSet):
    serializer_class = ModelFieldSerializer
    permission_classes = [IsAuthenticated, IsManagerPermission]
    filterset_fields = ['model', 'is_deleted']
    search_fields = ['number', 'name', 'remark']
    ordering_fields = ['id', 'number', 'name', 'update_time', 'delete_time']
    queryset = ModelField.objects.all()


class SystemConfigViewSet(FunctionViewSet):

    @extend_schema(responses={200: FieldConfigResponse(many=True)})
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def field_config(self, request, *args, **kwargs):
        """字段配置"""

        serializer = FieldConfigResponse(instance=ModelField.objects.filter(is_deleted=False), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class NotificationViewSet(QueryViewSet, DestroyModelMixin):
    """通知"""

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['is_read']
    queryset = Notification.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(notifier=self.user)

    def perform_destroy(self, instance):
        instance.attachment.delete()
        return super().perform_destroy(instance)

    @extend_schema(responses={200: NotificationSerializer})
    @action(detail=True, methods=['post'])
    def read(self, request, *args, **kwargs):
        """标记已读"""

        instance = self.get_object()
        instance.is_read = True
        instance.save(update_fields=['is_read'])

        serializer = NotificationSerializer(instance=instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses={204: None})
    @action(detail=False, methods=['post'])
    def read_all(self, request, *args, **kwargs):
        """全部已读"""

        Notification.objects.filter(notifier=self.user).update(is_read=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses={204: None})
    @action(detail=False, methods=['post'])
    def delete_unread(self, request, *args, **kwargs):
        """删除未读"""

        Notification.objects.filter(notifier=self.user, is_read=False).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses={204: None})
    @action(detail=False, methods=['post'])
    def delete_read(self, request, *args, **kwargs):
        """删除已读"""

        Notification.objects.filter(notifier=self.user, is_read=True).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses={200: OpenApiTypes.BINARY})
    @action(detail=True, methods=['post'])
    def download(self, request, *args, **kwargs):
        """下载附件"""

        notification = self.get_object()
        if not notification.has_attachment:
            raise ValidationError(f'不存在附件, 无法下载')

        file_path = notification.attachment.path
        if not Path(file_path).exists():
            raise ValidationError(f'附件不存在')

        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=notification.attachment_name)


__all__ = [
    'RoleViewSet',
    'UserViewSet',
    'UserActionViewSet',
    'WarehouseViewSet',
    'ModelFieldViewSet',
    'SystemConfigViewSet',
    'NotificationViewSet',
]
