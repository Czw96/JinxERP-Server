from rest_framework.permissions import BasePermission
from django_tenants.utils import get_tenant
from django.utils import timezone

from extensions.exceptions import ValidationError
from apps.system.models import User


class IsAuthenticated(BasePermission):
    message = '未登陆验证'

    def has_permission(self, request, view):
        if not isinstance(request.user, User):
            return False

        tenant = get_tenant(request)
        if tenant.expiry_time < timezone.now():
            raise ValidationError(f'已到期, 到期日期: {tenant.expiry_time}')

        if request.user.is_manager:
            return True

        if not request.user.is_active:
            raise ValidationError('账号未激活, 无法执行任何操作')

        return True


class IsManagerPermission(BasePermission):
    message = '非管理员账号'

    def has_permission(self, request, view):
        return request.user.is_manager


class ModelPermission(BasePermission):
    code = None
    message = '未添加操作权限'
    methods = {
        'GET': 'query',
        'POST': 'create',
        'PUT': 'update',
        'DELETE': 'delete',
    }

    def has_permission(self, request, view):
        if request.user.is_manager:
            return True

        code = f'{self.code}.{self.methods[request.method]}'
        return code in request.user.permissions


class FunctionPermission(BasePermission):
    """功能权限"""

    code = None
    message = '未添加操作权限'

    def has_permission(self, request, view):
        if request.user.is_manager:
            return True

        return self.code in request.user.permissions


__all__ = [
    'BasePermission',
    'IsAuthenticated',
    'IsManagerPermission',
    'ModelPermission',
    'FunctionPermission',
]
