from django.utils import timezone
from rest_framework.permissions import BasePermission

from apps.system.models import User
from extensions.exceptions import ValidationError


class IsAuthenticated(BasePermission):
    message = '未登陆验证'

    def has_permission(self, request, view):
        if not isinstance(request.user, User):
            return False

        if view.tenant.expiry_time < timezone.now():
            raise ValidationError(f'账号已到期, 到期日期: {view.tenant.expiry_time}')

        if request.user.is_manager:
            return True

        if not request.user.is_enabled:
            raise ValidationError('账号已禁用, 无法执行任何操作')

        return True


class IsManagerPermission(BasePermission):
    message = '非管理员账号'

    def has_permission(self, request, view):
        return request.user.is_manager


class ModelPermission(BasePermission):
    code = None
    message = '未添加操作权限'
    method_map = {
        'GET': 'query',
        'POST': 'create',
        'PUT': 'update',
        'DELETE': 'delete',
    }

    def has_permission(self, request, view):
        if request.user.is_manager:
            return True

        code = f'{self.code}.{self.method_map[request.method]}'
        return code in request.user.permissions

    @property
    def OPTION(self):
        return f'{self.code}.query'


class FunctionPermission(BasePermission):
    """功能权限"""

    code = None
    message = '未添加操作权限'

    def has_permission(self, request, view):
        if request.user.is_manager:
            return True

        return self.code in request.user.permissions


class QueryPermission:
    """查询权限"""

    code = None

    @classmethod
    def has_permission(cls, request):
        if request.user.is_manager:
            return True

        return cls.code in request.user.permissions


class OptionPermission(BasePermission):
    """选项权限"""

    code_set = set()
    message = '未添加操作权限'

    def has_permission(self, request, view):
        if request.user.is_manager:
            return True

        return self.code_list.isdisjoint(request.user.permissions)


__all__ = [
    'BasePermission',
    'IsAuthenticated',
    'IsManagerPermission',
    'ModelPermission',
    'FunctionPermission',
    'QueryPermission',
    'OptionPermission',
]
