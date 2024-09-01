from rest_framework import serializers

from extensions.serializers import ModelSerializerEx
from extensions.exceptions import ValidationError
from apps.data.models import *


class AccountSerializer(ModelSerializerEx):

    class Meta:
        model = Account
        read_only_fields = ['id', 'number', 'update_time', 'create_time', 'is_deleted', 'delete_time']
        fields = ['name', 'remark', 'is_active', 'extension_data', *read_only_fields]

    def validate_unique(self, attrs):
        self.check_unique(Account.objects.filter(delete_time=None), {'name': attrs['name']}, '名称已存在')

    def create(self, validated_data):
        total_count = Account.objects.all().count() + 1
        validated_data['number'] = f'A{total_count:03d}'
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.is_exporting or instance.is_importing:
            raise ValidationError('数据被占用, 无法编辑')
        return super().update(instance, validated_data)


__all__ = [
    'AccountSerializer',
]
