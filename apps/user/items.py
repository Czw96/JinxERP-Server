from extensions.serializers import ModelSerializerEx
from apps.user.models import *


class RoleItemSerializer(ModelSerializerEx):

    class Meta:
        model = Role
        fields = ['id', 'name', 'code', 'permission_set']


class WarehouseItemSerializer(ModelSerializerEx):

    class Meta:
        model = Warehouse
        fields = ['id', 'number', 'name', 'code', 'address', 'is_locked', 'is_active']


__all__ = [
    'RoleItemSerializer',
    'WarehouseItemSerializer',
]
