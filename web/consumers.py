from channels.generic.websocket import AsyncWebsocketConsumer
import json

class QRLoginConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user'].id
        self.group_name = f"qr_login_{self.user_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def login_successful(self, event):
        await self.send(text_data=json.dumps({
            'status': 'authenticated'
        }))
