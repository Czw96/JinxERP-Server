from extensions.serializers import ModelSerializerEx
from apps.system.models import *


class RoleItemSerializer(ModelSerializerEx):

    class Meta:
        model = Role
        fields = ['id', 'name']


class UserItemSerializer(ModelSerializerEx):

    class Meta:
        model = User
        fields = ['id', 'number', 'name', 'is_manager', 'is_enabled']


class WarehouseItemSerializer(ModelSerializerEx):

    class Meta:
        model = Warehouse
        fields = ['id', 'number', 'name', 'is_locked', 'is_enabled']


__all__ = [
    'RoleItemSerializer',
    'UserItemSerializer',
    'WarehouseItemSerializer',
]
