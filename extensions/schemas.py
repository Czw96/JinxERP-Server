from rest_framework import serializers
from rest_framework.serializers import Serializer


class MakeNumberResponse(Serializer):
    number = serializers.CharField(label='编号')


class InstanceListRequest(Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        error_messages={'min_length': '列表不能为空, 请至少提供一个 ID'},
        label='实例ID',
    )


class ImportRequest(Serializer):
    import_file = serializers.FileField(label='导入文件')


class ExportTaskResponse(Serializer):
    task_number = serializers.CharField(label='任务编号')


class ImportTaskResponse(Serializer):
    task_number = serializers.CharField(label='任务编号')


__all__ = [
    'MakeNumberResponse',
    'InstanceListRequest',
    'ImportRequest',
    'ExportTaskResponse',
    'ImportTaskResponse',
]
