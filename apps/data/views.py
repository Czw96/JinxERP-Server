from drf_spectacular.utils import extend_schema
from django_tenants.utils import get_tenant
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from extensions.permissions import IsAuthenticated
from extensions.exceptions import ValidationError
from extensions.viewsets import ModelViewSetEx, ArchiveViewSet, ExportModelMixin, ImportModelMixin
from extensions.schemas import InstanceListRequest
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
    filterset_fields = ['is_active', 'is_deleted']
    search_fields = ['number', 'name', 'remark']
    ordering_fields = ['id', 'number', 'name', 'update_time', 'delete_time']
    queryset = Account.objects.all()

    def perform_destroy(self, instance):
        if instance.is_exporting or instance.is_importing:
            raise ValidationError('数据被占用, 无法删除')
        return super().perform_destroy(instance)

    @extend_schema(responses={204: None})
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

        importing_account_list = Account.objects.filter(id__in=instance_ids, is_importing=True).values_list('name', flat=True)
        if len(importing_account_list) > 0:
            raise ValidationError(f'结算账户{importing_account_list} 正在导入中')

        export_task = ExportTask.objects.create(model=ExportTask.DataModel.ACCOUNT,
                                                export_id_list=instance_ids,
                                                export_count=len(instance_ids),
                                                creator=self.user)
        tenant = get_tenant(request)
        task_number = account_export_task.delay(tenant.id, export_task.id)
        export_task.number = task_number
        export_task.save(update_fields=['number'])

        Account.objects.filter(id__in=instance_ids).update(is_exporting=True)
        return Response(data={'task_number': task_number}, status=status.HTTP_204_NO_CONTENT)


__all__ = [
    'AccountViewSet',
]
