from apps.system.models import *
from extensions.serializers import ModelSerializerEx


# System
class RoleOptionSerializer(ModelSerializerEx):

    class Meta:
        model = Role
        fields = ['id', 'name']


class UserOptionSerializer(ModelSerializerEx):

    class Meta:
        model = User
        fields = ['id', 'number', 'name', 'is_manager', 'is_enabled']


class WarehouseOptionSerializer(ModelSerializerEx):

    class Meta:
        model = Warehouse
        fields = ['id', 'number', 'name', 'is_locked', 'is_enabled']


__all__ = [
    'RoleOptionSerializer',
    'UserOptionSerializer',
    'WarehouseOptionSerializer',
]
