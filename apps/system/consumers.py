from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils import timezone


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()

        if not (tenant := self.scope.get('tenant')):
            await self.send_json({'status_code': 400, 'detail': '账号不存在'})
            await self.close()

        if tenant.expiry_time < timezone.now():
            await self.send_json({'status_code': 400, 'detail': '账号已到期'})
            await self.close()

        if not (user := self.scope.get('user')):
            await self.send_json({'status_code': 401, 'detail': '令牌无效'})
            await self.close()

        if not user.is_active:
            await self.send_json({'status_code': 400, 'detail': '账号未激活'})
            await self.close()


__all__ = [
    'NotificationConsumer',
]
