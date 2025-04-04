import django_filters
from django_filters import FilterSet

from apps.system.models import *


class UserFilter(FilterSet):
    role = django_filters.NumberFilter(field_name='role_set', label='角色')
    warehouse = django_filters.NumberFilter(field_name='warehouse_set', label='仓库')

    class Meta:
        model = User
        fields = ['role', 'warehouse', 'is_enabled', 'is_deleted']


__all__ = [
    'UserFilter',
]
