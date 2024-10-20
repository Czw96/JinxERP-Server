from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from django.utils import timezone
from django.core.cache import cache


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    consumer_code = 'notification'

    async def connect(self):
        await self.accept()

        if not (tenant := self.scope.get('tenant')):
            await self.send_json({'status_code': 400, 'detail': '账号不存在'}, close=True)
            return

        if tenant.expiry_time < timezone.now():
            await self.send_json({'status_code': 400, 'detail': '账号已到期'}, close=True)
            return

        if not (user := self.scope.get('user')):
            await self.send_json({'status_code': 401, 'detail': '令牌无效'}, close=True)
            return

        if not user.is_active:
            await self.send_json({'status_code': 400, 'detail': '账号未激活'}, close=True)
            return

        cache.set(f'{self.consumer_code}-{user.id}', self.channel_name)

    async def disconnect(self, close_code):
        if user := self.scope.get('user'):
            print(f'{self.consumer_code}-{user.id}')
            cache.delete(f'{self.consumer_code}-{user.id}')

    @classmethod
    async def send_notification(cls, user, data):
        channel_layer = get_channel_layer()
        if channel_name := cache.get(f'{cls.consumer_code}-{user.id}'):
            await channel_layer.send(channel_name, {"type": "handle.send", "data": data})

    async def handle_send(self, event):
        await self.send_json({'status_code': 200, 'results': event['data']})


__all__ = [
    'NotificationConsumer',
]
