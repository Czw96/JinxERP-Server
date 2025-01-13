from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from django.utils import timezone
from django.http import FileResponse
from pathlib import Path

from extensions.permissions import IsAuthenticated
from extensions.exceptions import ValidationError
from extensions.viewsets import ModelViewSetEx
from apps.task.serializers import *
from apps.task.permissions import *
from apps.task.filters import *
from apps.task.schemas import *
from apps.task.models import *


class ExportTaskViewSet(ModelViewSetEx):
    serializer_class = ExportTaskSerializer
    permission_classes = [IsAuthenticated, ExportTaskPermission]
    filterset_class = ExportTaskFilter
    search_fields = ['number']
    ordering_fields = ['id', 'create_time']
    select_related_fields = ['creator']
    queryset = ExportTask.objects.all()

    def get_queryset(self):
        if ExportTaskQueryAllPermission.has_permission(self.request):
            return super().get_queryset()
        return super().get_queryset().filter(creator=self.user)

    def perform_destroy(self, instance):
        instance.export_file.delete()
        return super().perform_destroy(instance)

    @extend_schema(responses={200: ExportTaskSerializer})
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, ExportTaskCancelPermission])
    def cancel(self, request, *args, **kwargs):
        """取消"""

        export_task = self.get_object()
        if export_task.status != ExportTask.ExportStatus.EXPORTING:
            raise ValidationError(f'导出任务已结束, 无法取消')

        async_result = AsyncResult(export_task.celery_task_number)
        async_result.revoke(terminate=True)

        export_task.status = ExportTask.ExportStatus.CANCELLED
        export_task.duration = (timezone.localtime() - export_task.create_time).total_seconds()
        export_task.save(update_fields=['status', 'duration'])

        serializer = ExportTaskSerializer(instance=export_task, context=self.context)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: OpenApiTypes.BINARY})
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, ExportTaskDownloadPermission])
    def download(self, request, *args, **kwargs):
        """下载"""

        export_task = self.get_object()
        if export_task.status != ExportTask.ExportStatus.COMPLETED:
            raise ValidationError(f'导出任务未成功或正在进行中, 无法下载')

        file_path = export_task.export_file.path
        if not Path(file_path).exists():
            raise ValidationError(f'文件不存在')

        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=export_task.number)


class ImportTaskViewSet(ModelViewSetEx):
    serializer_class = ImportTaskSerializer
    permission_classes = [IsAuthenticated, ImportTaskPermission]
    filterset_class = ImportTaskFilter
    search_fields = ['number']
    ordering_fields = ['id', 'create_time']
    select_related_fields = ['creator']
    queryset = ImportTask.objects.all()

    def get_queryset(self):
        if ImportTaskQueryAllPermission.has_permission(self.request):
            return super().get_queryset()
        return super().get_queryset().filter(creator=self.user)

    def perform_destroy(self, instance):
        instance.import_file.delete()
        return super().perform_destroy(instance)


__all__ = [
    'ExportTaskViewSet',
    'ImportTaskViewSet',
]
