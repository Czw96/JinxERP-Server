from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("connect:")

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):

        if text_data:
            print("Received text message:", text_data)
            await self.send(text_data=text_data)
        elif bytes_data:

            print("Received bytes message of length:", len(bytes_data))
            # 注意：回发二进制消息需要确保客户端可以处理它
            # await self.send(bytes_data=bytes_data)  # 如果有需要的话，可以取消注释这行

    async def disconnect(self, close_code):

        print("WebSocket disconnected:", close_code)


__all__ = [
    'NotificationConsumer',
]
