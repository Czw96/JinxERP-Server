import json
import time

from asgiref.sync import async_to_sync
from celery import shared_task
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone
from django_tenants.utils import tenant_context

from apps.data.models import *
from apps.data.serializers import *
from apps.system.consumers import NotificationConsumer
from apps.system.models import ModelField, Notification
from apps.system.serializers import NotificationSerializer
from apps.task.consumers import ExportTaskConsumer
from apps.task.models import ExportTask, ImportTask
from apps.tenant.models import ErrorLog, Tenant
from extensions.field_configs import export_extension_data


@shared_task
@transaction.atomic
def account_export_task(tenant_id, export_task_id):
    tenant = Tenant.objects.get(id=tenant_id)
    with tenant_context(tenant):
        export_task = ExportTask.objects.get(id=export_task_id)
        completed_count = 0

        try:
            queryset = Account.objects.filter(id__in=export_task.export_id_list)
            total_count = queryset.count()

            items = []
            for instance in queryset:
                async_to_sync(ExportTaskConsumer.send_data)(
                    export_task.creator,
                    {
                        'export_status': export_task.status,
                        'total_count': total_count,
                        'completed_count': completed_count,
                    }
                )

                items.append({
                    '编号': instance.number,
                    '名称': instance.name,
                    '备注': instance.remark,
                    '启用状态': '启用' if instance.is_enabled else '禁用',
                    **export_extension_data(ModelField.DataModel.ACCOUNT, instance.extension_data)
                })

                completed_count += 1
                time.sleep(0.1)

            json_data = json.dumps(items, ensure_ascii=False)
            content_file = ContentFile(json_data.encode('utf-8'))
            file_path = f'{tenant.number}/export_file/{export_task.number}.json'
            export_task.export_file.save(file_path, content_file, save=True)

            export_task.export_count = completed_count
            export_task.status = ExportTask.ExportStatus.COMPLETED
            export_task.duration = (timezone.localtime() - export_task.create_time).total_seconds()
            export_task.save(update_fields=['export_count', 'status', 'duration'])

            notification = Notification.objects.create(title='导出结算账户',
                                                       type=Notification.NotificationType.SUCCESS,
                                                       content=f'结算账户导出成功, 共导出 {export_task.export_count} 条数据.',
                                                       attachment_name='结算账户列表',
                                                       attachment_format=Notification.AttachmentFormat.EXCEL,
                                                       has_attachment=True,
                                                       notifier=export_task.creator)
            file_path = f'{tenant.number}/notification_file/{export_task.number}.json'
            notification.attachment.save(file_path, content_file, save=True)

            async_to_sync(ExportTaskConsumer.send_data)(
                export_task.creator,
                {
                    'export_status': export_task.status,
                    'total_count': export_task.export_count,
                    'completed_count': completed_count,
                }
            )
        except Exception as error:
            export_task.status = ExportTask.ExportStatus.FAILED
            export_task.duration = (timezone.localtime() - export_task.create_time).total_seconds()
            export_task.error_message = str(error)
            export_task.save(update_fields=['status', 'duration', 'error_message'])

            notification = Notification.objects.create(title='导出结算账户',
                                                       type=Notification.NotificationType.ERROR,
                                                       content=f'结算账户导出失败.',
                                                       notifier=export_task.creator)
            async_to_sync(ExportTaskConsumer.send_data)(
                export_task.creator,
                {
                    'export_status': export_task.status,
                    'total_count': export_task.export_count,
                    'completed_count': completed_count,
                }
            )
            ErrorLog.objects.create(module='结算账户导出', content=str(error))

        try:
            serializer = NotificationSerializer(instance=notification)
            async_to_sync(NotificationConsumer.send_data)(export_task.creator, [serializer.data])
        except Exception as error:
            ErrorLog.objects.create(module='结算账户导出', content=str(error))


@shared_task
@transaction.atomic
def account_import_task(tenant_id, import_task_id):
    tenant = Tenant.objects.get(id=tenant_id)
    with tenant_context(tenant):
        import_task = ImportTask.objects.get(id=import_task_id)
        completed_count = 0

        try:
            with import_task.import_file as file:
                import_file_content = file.read().decode('utf-8')

            # 数据验证
            import_data = json.loads(import_file_content)
            serializer_list = []
            error_message_list = []
            for index, item in enumerate(import_data['data']):
                serializer = AccountSerializer(data=item)
                if number := item.get('number'):
                    instance = Account.objects.filter(number=number).first()
                    if not instance:
                        raise Exception(f'第 {index + 1} 行数据编号不存在')

                    if instance.is_deleted:
                        raise Exception(f'第 {index + 1} 行数据已删除')

                    serializer.instance = instance

                serializer.is_valid(raise_exception=False)
                serializer_list.append(serializer)

            if len(error_message_list) == 0:
                ...

        except json.JSONDecodeError as json_error:
            ...
            # 处理 JSON 解析错误
            # logger.error("Failed to decode JSON: %s", json_error)
        except UnicodeDecodeError as unicode_error:
            ...
            # 处理文件解码错误
            # logger.error("Failed to decode file content: %s", unicode_error)
        except Exception as error:
            ...


__all__ = [
    'account_export_task',
    'account_import_task',
]
