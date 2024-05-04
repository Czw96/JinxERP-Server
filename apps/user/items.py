from extensions.serializers import ModelSerializerEx
from apps.user.models import *


class RoleItemSerializer(ModelSerializerEx):

    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions']


class WarehouseItemSerializer(ModelSerializerEx):

    class Meta:
        model = Warehouse
        fields = ['id', 'number', 'name', 'address', 'is_locked', 'is_active']


__all__ = [
    'RoleItemSerializer',
    'WarehouseItemSerializer',
]
