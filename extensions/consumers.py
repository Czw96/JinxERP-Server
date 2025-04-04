from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from django.utils import timezone

from apps.tenant.models import ErrorLog
from extensions.exceptions import NotAuthenticated, ValidationError


class AsyncJsonWebsocketConsumerEx(AsyncJsonWebsocketConsumer):
    consumer_code = None

    @property
    def tenant(self):
        return self.scope.get('tenant')

    @property
    def user(self):
        return self.scope.get('user')

    async def init_data(self):
        ...

    async def connect(self):
        await self.accept()

        try:
            if not self.tenant:
                raise ValidationError('账号不存在')

            if self.tenant.expiry_time < timezone.now():
                raise ValidationError('账号已到期')

            if not self.user:
                raise NotAuthenticated('身份识别失败')

            if not self.user.is_enabled:
                raise ValidationError('账号已禁用')

            await self.init_data()
            await self.channel_layer.group_add(f'{self.consumer_code}.{self.user.id}', self.channel_name)

        except NotAuthenticated as error:
            await self.send_json({'status_code': 401, 'detail': str(error)}, close=True)
        except ValidationError as error:
            await self.send_json({'status_code': 400, 'detail': str(error)}, close=True)
        except Exception as error:
            await ErrorLog.objects.acreate(module='通知系统', content=str(error))
            await self.send_json({'status_code': 500, 'detail': str(error)}, close=True)

    async def disconnect(self, close_code):
        if self.user:
            await self.channel_layer.group_discard(f'{self.consumer_code}.{self.user.id}', self.channel_name)

    @classmethod
    async def send_data(cls, user, data):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(f'{cls.consumer_code}.{user.id}', {'type': 'handle.event', 'data': data})

    async def handle_event(self, event):
        ...


__all__ = [
    'AsyncJsonWebsocketConsumerEx',
]
