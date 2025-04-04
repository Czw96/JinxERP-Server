from apps.system.models import Notification
from extensions.consumers import AsyncJsonWebsocketConsumerEx


class NotificationConsumer(AsyncJsonWebsocketConsumerEx):
    consumer_code = 'notification'

    async def init_data(self):
        await self.handle_event({'data': []})

    async def handle_event(self, event):
        unread_count = await Notification.objects.filter(notifier=self.user, is_read=False).acount()
        await self.send_json({'status_code': 200, 'data': {
            'unread_count': unread_count,
            'notification_items': event['data'],
        }})


__all__ = [
    'NotificationConsumer',
]
