from django.contrib.auth.hashers import make_password
# from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from extensions.serializers import ModelSerializerEx, UniqueTogetherValidatorEX
from extensions.exceptions import ValidationError
from extensions.field_configs import *
from apps.system.models import *
from apps.system.items import *


class RoleSerializer(ModelSerializerEx):

    class Meta:
        model = Role
        read_only_fields = ['id', 'update_time', 'create_time']
        fields = ['name', 'remark', 'permissions', 'extension_data', *read_only_fields]


class UserSerializer(ModelSerializerEx):
    warehouse_items = WarehouseItemSerializer(source='warehouse_set', many=True, read_only=True, label='仓库Items')
    role_items = RoleItemSerializer(source='role_set', many=True, read_only=True, label='角色Items')

    class Meta:
        model = User
        read_only_fields = ['id', 'number', 'warehouse_items', 'role_items', 'permissions', 'is_manager',
                            'update_time', 'create_time', 'is_deleted', 'delete_time']
        fields = ['username', 'name', 'phone', 'warehouse_set', 'role_set', 'remark', 'is_active', 'extension_data',
                  *read_only_fields]
        validators = [
            UniqueTogetherValidatorEX(User.objects.filter(is_deleted=False), ['username'], '用户名已存在'),
            UniqueTogetherValidatorEX(User.objects.filter(is_deleted=False), ['name'], '名称已存在'),
        ]

    def create(self, validated_data):
        total_count = User.objects.all().count() + 1
        validated_data['number'] = f'U{total_count:03d}'
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
        read_only_fields = ['id', 'number', 'is_locked', 'update_time', 'create_time', 'is_deleted', 'delete_time']
        fields = ['name', 'address', 'remark', 'is_active', 'extension_data', *read_only_fields]
        # validators = [
        #     UniqueTogetherValidatorEX(Warehouse.objects.filter(is_deleted=False), ['name'], '名称已存在'),
        # ]

    def validate(self, attrs):
        self.validate_unique(Warehouse.objects.filter(delete_time=None), ['name'], '名称已存在')

        return super().validate(attrs)

    # def validate_empty_values(self, data):
    #     return super().validate_empty_values(data)

    # def validate_unique_together(self):
    #     print(11)
    #     queryset = Warehouse.objects.filter(delete_time=None)
    #     if self.instance:
    #         queryset = queryset.exclude(pk=self.instance.pk)

    #     # if Warehouse.objects.filter(name=self.name, is_deleted=False).exists():
    #     #     raise ValidationError('名称已存在')

    def create(self, validated_data):
        total_count = Warehouse.objects.all().count() + 1
        validated_data['number'] = f'W{total_count:03d}'
        return super().create(validated_data)

    def save(self, **kwargs):
        return super().save(**kwargs)


class ModelFieldSerializer(ModelSerializerEx):
    model_display = serializers.CharField(source='get_model_display', read_only=True, label='模型')
    type_display = serializers.CharField(source='get_type_display', read_only=True, label='类型')

    class Meta:
        model = ModelField
        read_only_fields = ['id', 'number', 'model_display', 'type_display', 'update_time', 'create_time',
                            'is_deleted', 'delete_time']
        fields = ['name', 'model', 'type', 'priority', 'remark', 'property', *read_only_fields]
        validators = [
            UniqueTogetherValidatorEX(ModelField.objects.filter(is_deleted=False), ['name', 'model'], '名称和模型已存在'),
        ]

    def validate(self, attrs):
        type = attrs['type']
        property = attrs.get('property', {})

        if type == ModelField.DataType.TEXT:
            serializer = TextFieldProperty(data=property)
        elif type == ModelField.DataType.NUMBER:
            serializer = NumberFieldProperty(data=property)
        elif type == ModelField.DataType.DATE:
            serializer = DateFieldProperty(data=property)
        elif type == ModelField.DataType.TIME:
            serializer = TimeFieldProperty(data=property)
        elif type == ModelField.DataType.SINGLE_CHOICE:
            serializer = SingleChoiceFieldProperty(data=property)
        elif type == ModelField.DataType.MULTIPLE_CHOICE:
            serializer = MultipleChoiceFieldProperty(data=property)
        else:
            raise ValidationError('字段类型错误')

        serializer.is_valid(raise_exception=True)
        attrs['property'] = serializer.validated_data
        return super().validate(attrs)

    def create(self, validated_data):
        total_count = ModelField.objects.all().count() + 1
        validated_data['number'] = f'MF{total_count:03d}'
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.model != validated_data['model']:
            raise ValidationError('模型不可修改')
        if instance.type != validated_data['type']:
            raise ValidationError('类型不可修改')

        return super().update(instance, validated_data)


__all__ = [
    'RoleSerializer',
    'UserSerializer',
    'WarehouseSerializer',
    'ModelFieldSerializer',
]
