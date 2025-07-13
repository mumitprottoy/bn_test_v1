import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, RoomMate, MessageMetaData, MessageTextContent
from player.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data['text']
        username = data['username']

        metadata = await self.save_message(username, self.room_name, text)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': text,
                'username': username,
                'timestamp': str(metadata.sent_at)
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, username, room_name, text):
        user = User.objects.get(username=username)
        room = Room.objects.get(name=room_name)
        metadata = MessageMetaData.objects.create(room=room, sender=user)
        MessageTextContent.objects.create(metadata=metadata, text=text)
        return metadata
