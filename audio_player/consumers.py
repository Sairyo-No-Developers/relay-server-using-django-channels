import json
import uuid
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *

class AudioSession(AsyncWebsocketConsumer):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.room_name = self.scope['url_route']['kwargs']['room_name']
    #     self.room_group_name = 'chat_%s' % self.room_name
    #     if len(Session.objects.filter(session_name = self.room_name)) > 0:
    #         self.msg = {"host": False}
    #     else:
    #         ses = Session.objects.create(session_name = self.room_name)
    #         ses.save()
    #         self.msg = {"host": True}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer_ID = str(uuid.uuid4())

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        self.msg = await self.first_connect()
        await self.send(text_data=json.dumps(self.msg))

    @database_sync_to_async
    def first_connect(self):
        if len(Session.objects.filter(session_name = self.room_name)) > 0:
            return {"host": False}
        else:
            ses = Session.objects.create(session_name = self.room_name, consumer_name = self.consumer_ID)
            ses.save()
            return {"host": True}

    @database_sync_to_async
    def first_disconnect(self):
        obj = Session.objects.filter(consumer_name = self.consumer_ID)
        if len(obj) > 0:
            obj[0].delete()  

    async def disconnect(self, close_code):
        # Leave room group
        await self.first_disconnect()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        message = text_data
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=message)
