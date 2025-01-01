from drf_spectacular.utils import extend_schema
from django_tenants.utils import get_tenant
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone
from celery.result import AsyncResult
import uuid

from extensions.permissions import IsAuthenticated
from extensions.exceptions import ValidationError
from extensions.viewsets import ModelViewSetEx, ArchiveViewSet, ExportModelMixin, ImportModelMixin
from extensions.schemas import InstanceListRequest, ImportRequest, ExportTaskResponse, ImportTaskResponse
from extensions.utils import generate_number
from apps.data.serializers import *
from apps.data.permissions import *
from apps.data.filters import *
from apps.data.schemas import *
from apps.data.models import *
from apps.data.tasks import *
from apps.task.models import ExportTask, ImportTask


class AccountViewSet(ArchiveViewSet, ExportModelMixin, ImportModelMixin):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, AccountPermission]
    filterset_fields = ['is_enabled', 'is_deleted']
    search_fields = ['number', 'name', 'remark']
    ordering_fields = ['id', 'number', 'name', 'update_time', 'delete_time']
    queryset = Account.objects.all()

    @extend_schema(request=InstanceListRequest, responses={200: ExportTaskResponse})
    @action(detail=False, methods=['get', 'post'], permission_classes=[IsAuthenticated, AccountExportPermission])
    @transaction.atomic
    def export_data(self, request, *args, **kwargs):
        """导出数据"""

        if ExportTask.objects.filter(
                model=ExportTask.DataModel.ACCOUNT, status=ExportTask.ExportStatus.EXPORTING, creator=self.user).exists():
            raise ValidationError('导出任务正在进行中')

        queryset = self.get_queryset().filter(is_deleted=False)
        if request.method == 'GET':
            instance_ids = list(self.filter_queryset(queryset).values_list('id', flat=True))
        elif request.method == 'POST':
            serializer = InstanceListRequest(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            instance_ids = validated_data['ids']
            if queryset.filter(id__in=instance_ids).count() != len(instance_ids):
                raise ValidationError('导出数据不存在')
        else:
            raise ValidationError('导出数据错误')

        if Account.objects.filter(id__in=instance_ids).count() == 0:
            raise ValidationError('空数据无法导出')

        export_task_number = generate_number('EX')
        export_task = ExportTask.objects.create(number=export_task_number,
                                                model=ExportTask.DataModel.ACCOUNT,
                                                export_id_list=instance_ids,
                                                creator=self.user)
        tenant = get_tenant(request)
        account_export_task.apply_async(args=(tenant.id, export_task.id), task_id=export_task_number, countdown=3)
        return Response(data={'task_number': export_task_number}, status=status.HTTP_200_OK)

    @extend_schema(responses={204: None})
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, AccountExportPermission])
    @transaction.atomic
    def cancel_export(self, request, *args, **kwargs):
        """取消导出"""

        if not (export_task := ExportTask.objects.filter(
                model=ExportTask.DataModel.ACCOUNT, status=ExportTask.ExportStatus.EXPORTING, creator=self.user).first()):
            raise ValidationError('导出任务不存在')

        async_result = AsyncResult(export_task.number)
        async_result.revoke(terminate=True)

        export_task.status = ExportTask.ExportStatus.CANCELLED
        export_task.duration = (timezone.localtime() - export_task.create_time).total_seconds()
        export_task.save(update_fields=['status', 'duration'])

        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=ImportRequest, responses={200: ImportTaskResponse})
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, AccountImportPermission])
    @transaction.atomic
    def import_data(self, request, *args, **kwargs):
        """导入数据"""

        if ImportTask.objects.filter(
                model=ImportTask.DataModel.ACCOUNT, status=ImportTask.ImportStatus.IMPORTING, creator=self.user).exists():
            raise ValidationError('导入任务正在进行中')

        serializer = ImportRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        tenant = get_tenant(request)

        import_file = validated_data['import_file']
        import_task_number = generate_number('IM')
        import_task = ImportTask.objects.create(
            number=import_task_number, model=ImportTask.DataModel.ACCOUNT, creator=self.user)
        file_path = f'{tenant.number}/import_file/{import_task_number}.json'
        import_task.import_file.save(file_path, import_file, save=True)

        account_import_task.apply_async(args=(tenant.id, import_task.id), task_id=import_task_number, countdown=3)
        return Response(data={'task_number': import_task_number}, status=status.HTTP_200_OK)


__all__ = [
    'AccountViewSet',
]
