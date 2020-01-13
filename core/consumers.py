
# chat/consumers.py

import json
from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'] == AnonymousUser():
            raise DenyConnection("Invalid User")
        user = self.scope["user"]
        user_id = user.id
        self.group_name = "{}".format(user_id)
        # Join room group

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'recieve_group_message',
                'message': message,
                'user': user
            }
        )

    async def recieve_group_message(self, event):
        message = event['message']
        user = event['user']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message, 'user': user}))
