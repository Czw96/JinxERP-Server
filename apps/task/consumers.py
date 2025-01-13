from extensions.consumers import AsyncJsonWebsocketConsumerEx
from extensions.exceptions import ValidationError
from apps.task.models import ExportTask


class ExportTaskConsumer(AsyncJsonWebsocketConsumerEx):
    consumer_code = 'export_task'

    async def init_data(self):
        if not (export_task_number := self.scope['query_params'].get('number')):
            raise ValidationError('缺失任务编号')

        if not (export_task := await ExportTask.objects.filter(number=export_task_number, creator=self.user).afirst()):
            raise ValidationError('没有进行中的任务')

        if export_task.status != ExportTask.ExportStatus.EXPORTING:
            completed_count = export_task.export_count if export_task.status == ExportTask.ExportStatus.COMPLETED else 0
            await self.handle_event({'data': {
                'export_status': export_task.status,
                'total_count': export_task.export_count,
                'completed_count': completed_count,
            }})

    async def handle_event(self, event):
        data = event['data']
        is_close = data['export_status'] != ExportTask.ExportStatus.EXPORTING
        await self.send_json({'status_code': 200, 'data': data}, is_close)


__all__ = [
    'ExportTaskConsumer',
]
