from rest_framework import serializers

from extensions.serializers import ModelSerializerEx
from extensions.exceptions import ValidationError
from apps.task.models import *
from apps.system.items import *


class ExportTaskSerializer(ModelSerializerEx):
    model_display = serializers.CharField(source='get_model_display', read_only=True, label='模型')
    status_display = serializers.CharField(source='get_status_display', read_only=True, label='状态')
    creator_item = UserItemSerializer(source='creator', read_only=True, label='创建人')

    class Meta:
        model = ExportTask
        fields = ['id', 'number', 'model', 'model_display', 'export_count', 'status', 'status_display',
                  'error_message', 'duration', 'creator', 'creator_item', 'create_time']


class ImportTaskSerializer(ModelSerializerEx):
    model_display = serializers.CharField(source='get_model_display', read_only=True, label='模型')
    status_display = serializers.CharField(source='get_status_display', read_only=True, label='状态')
    creator_item = UserItemSerializer(source='creator', read_only=True, label='创建人')

    class Meta:
        model = ImportTask
        fields = ['id', 'number', 'model', 'model_display', 'import_count', 'status', 'status_display',
                  'error_message_list', 'duration', 'creator', 'creator_item', 'create_time']


__all__ = [
    'ExportTaskSerializer',
    'ImportTaskSerializer',
]
