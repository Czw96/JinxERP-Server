from django.core.files.base import ContentFile
from django_tenants.utils import tenant_context
from django.utils import timezone
from celery import shared_task
import time
import json

from extensions.exceptions import ServerError
from apps.data.models import *
from apps.data.serializers import *
from apps.flow.models import ExportTask, ImportTask
from apps.tenant.models import Tenant, ErrorLog
from apps.system.models import ModelField


@shared_task
def account_export_task(tenant_id, export_task_id):
    tenant = Tenant.objects.get(id=tenant_id)
    with tenant_context(tenant):
        export_task = ExportTask.objects.get(id=export_task_id)
        time.sleep(5)

        try:
            model_field_set = ModelField.objects.filter(
                model=ModelField.DataModel.ACCOUNT, is_deleted=False).order_by('-priority')

            items = []
            for instance in Account.objects.filter(id__in=export_task.export_id_list):
                extension_item = {model_field.name: instance.extension_data.get(
                    model_field.number) for model_field in model_field_set}

                instance.extension_data
                items.append({
                    '编号': instance.number,
                    '名称': instance.name,
                    '备注': instance.remark,
                    '激活状态': '激活' if instance.is_active else '冻结',
                    **extension_item,
                })

            json_data = json.dumps(items, ensure_ascii=False)
            content_file = ContentFile(json_data.encode('utf-8'))
            file_path = f'{tenant.number}/export_file/{export_task.number}.json'
            export_task.export_file.save(file_path, content_file, save=True)

            export_task.status = ExportTask.ExportStatus.SUCCESS
            export_task.duration = (timezone.localtime() - export_task.create_time).total_seconds()
            export_task.save(update_fields=['status', 'duration'])
        except Exception as error:
            export_task.status = ExportTask.ExportStatus.FAILED
            export_task.duration = (timezone.localtime() - export_task.create_time).total_seconds()
            export_task.error_message = str(error)
            export_task.save(update_fields=['status', 'duration', 'error_message'])
            ErrorLog.objects.create(tenant=tenant, module='结算账户导出', content=str(error))


__all__ = [
    'account_export_task',
]