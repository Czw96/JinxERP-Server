from rest_framework import serializers

from extensions.serializers import ModelSerializerEx
from extensions.exceptions import ValidationError
from apps.data.models import *
from apps.system.models import ModelField
from extensions.field_configs import validate_custom_data


class AccountSerializer(ModelSerializerEx):

    class Meta:
        model = Account
        read_only_fields = ['id', 'number', 'update_time', 'create_time', 'is_deleted', 'delete_time']
        fields = ['name', 'remark', 'is_enabled', 'extension_data', *read_only_fields]

    def validate_unique(self, attrs):
        self.check_unique(Account.objects.filter(delete_time=None), {'name': attrs['name']}, '该名称已被使用')

    def validate(self, attrs):
        extension_data = attrs.get('extension_data', {})
        attrs['extension_data'] = validate_custom_data(ModelField.DataModel.ACCOUNT, extension_data)
        return super().validate(attrs)

    def create(self, validated_data):
        total_count = Account.objects.all().count() + 1
        validated_data['number'] = f'A{total_count:03d}'
        return super().create(validated_data)


__all__ = [
    'AccountSerializer',
]
