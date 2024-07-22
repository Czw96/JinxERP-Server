from django.contrib.auth.hashers import make_password
from rest_framework import serializers
import re

from extensions.serializers import ModelSerializerEx
from extensions.exceptions import ValidationError
from extensions.field_type import *
from apps.system.models import *
from apps.system.items import *


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


class FieldConfigSerializer(ModelSerializerEx):
    model_display = serializers.CharField(source='get_model_display', read_only=True, label='模型')
    type_display = serializers.CharField(source='get_type_display', read_only=True, label='类型')

    class Meta:
        model = FieldConfig
        read_only_fields = ['id', 'model_display', 'type_display', 'update_time', 'create_time']
        fields = ['name', 'model', 'type', 'code', 'priority', 'remark', 'property', *read_only_fields]

    def validate_code(self, value):
        if not re.match(r'^[0-9a-zA-Z_]+$', value):
            raise ValidationError('代码无效: 只能包含字母, 数字和下划线')
        return value

    def validate(self, attrs):
        type = attrs['type']
        property = attrs.get('property', {})

        if type == FieldConfig.DataType.TEXT:
            serializer = TextFieldProperty(data=property)
        elif type == FieldConfig.DataType.NUMBER:
            serializer = NumberFieldProperty(data=property)
        elif type == FieldConfig.DataType.DATE:
            serializer = DateFieldProperty(data=property)
        elif type == FieldConfig.DataType.TIME:
            serializer = TimeFieldProperty(data=property)
        elif type == FieldConfig.DataType.SINGLE_CHOICE:
            serializer = SingleChoiceFieldProperty(data=property)
        elif type == FieldConfig.DataType.MULTIPLE_CHOICE:
            serializer = MultipleChoiceFieldProperty(data=property)
        else:
            raise ValidationError('字段类型错误')

        serializer.is_valid(raise_exception=True)
        attrs['property'] = serializer.validated_data
        return super().validate(attrs)

    def update(self, instance, validated_data):
        if instance.model != validated_data['model']:
            raise ValidationError('模型不可修改')
        if instance.type != validated_data['type']:
            raise ValidationError('类型不可修改')
        if instance.code != validated_data['code']:
            raise ValidationError('代码不可修改')

        return super().update(instance, validated_data)


__all__ = [
    'RoleSerializer',
    'UserSerializer',
    'WarehouseSerializer',
    'FieldConfigSerializer',
]
