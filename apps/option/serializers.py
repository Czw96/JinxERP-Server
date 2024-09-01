from extensions.serializers import ModelSerializerEx

from apps.system.models import *


# System
class RoleOptionSerializer(ModelSerializerEx):

    class Meta:
        model = Role
        fields = ['id', 'name']


class UserOptionSerializer(ModelSerializerEx):

    class Meta:
        model = User
        fields = ['id', 'number', 'name', 'is_manager', 'is_active']


class WarehouseOptionSerializer(ModelSerializerEx):

    class Meta:
        model = Warehouse
        fields = ['id', 'number', 'name', 'is_locked', 'is_active']


__all__ = [
    'RoleOptionSerializer',
    'UserOptionSerializer',
    'WarehouseOptionSerializer',
]
