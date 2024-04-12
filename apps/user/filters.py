from django_filters import FilterSet
import django_filters

from apps.user.models import *


class UserFilter(FilterSet):
    role = django_filters.NumberFilter(field_name='role_set', label='角色')
    warehouse = django_filters.NumberFilter(field_name='warehouse_set', label='仓库')

    class Meta:
        model = User
        fields = ['role_set', 'warehouse_set', 'is_active']


__all__ = [
    'UserFilter',
]
