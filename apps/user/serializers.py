from django.contrib.auth.hashers import make_password

from extensions.serializers import ModelSerializerEx
from apps.user.models import *
from apps.user.items import *


class RoleSerializer(ModelSerializerEx):

    class Meta:
        model = Role
        read_only_fields = ['id', 'update_time', 'create_time']
        fields = ['name', 'remark', 'permissions', *read_only_fields]


class UserSerializer(ModelSerializerEx):
    warehouse_items = WarehouseItemSerializer(source='warehouse_set', many=True, read_only=True, label='仓库Items')
    role_items = RoleItemSerializer(source='role_set', many=True, read_only=True, label='角色Items')

    class Meta:
        model = User
        read_only_fields = ['id', 'number', 'warehouse_items', 'role_items', 'permissions', 'is_manager',
                            'update_time', 'create_time']
        fields = ['username', 'name', 'phone', 'warehouse_set', 'role_set', 'remark', 'is_active', *read_only_fields]

    def create(self, validated_data):
        validated_data['number'] = f'U{str(User.objects.count()).zfill(3)}'
        validated_data['password'] = make_password(validated_data['username'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.is_manager:
            validated_data['warehouse_set'] = []
            validated_data['role_set'] = []
            validated_data['is_active'] = True
        return super().update(instance, validated_data)

    def save(self, **kwargs):
        role_set = self.validated_data.get('role_set', [])
        permissions = {permission for role in role_set for permission in role.permissions}
        kwargs['permissions'] = list(permissions)
        return super().save(**kwargs)


class WarehouseSerializer(ModelSerializerEx):

    class Meta:
        model = Warehouse
        read_only_fields = ['id', 'number', 'is_locked', 'update_time', 'create_time']
        fields = ['name', 'address', 'remark', 'is_active', *read_only_fields]

    def create(self, validated_data):
        validated_data['number'] = f'W{str(Warehouse.objects.count()).zfill(3)}'
        return super().create(validated_data)


__all__ = [
    'RoleSerializer', 'UserSerializer', 'WarehouseSerializer',
]
