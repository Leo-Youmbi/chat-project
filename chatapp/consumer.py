import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from chatapp.models import Messages, Conversation

Users = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message_content = text_data_json["message"]
        room_id = text_data_json["room_id"]
        sender_username = text_data_json["sender_username"]
        print(sender_username)
        user = await database_sync_to_async(Users.objects.get)(username=sender_username)
        convo = await database_sync_to_async(Conversation.objects.get)(room_name=room_id)
        message = await database_sync_to_async(Messages.objects.create)(conversation=convo, content=message_content, user=user)
        await self.channel_layer.group_send(
            self.room_name, {
                "type": "sendMessage",
                "message": message.content,
                "sender_username": message.user.username,
                "timestamp": message.timestamp.strftime("%I:%M %p"),
                "room_name": room_id
            }
        )

        # Receive message from room group
    async def sendMessage(self, event):
        message = event["message"]
        sender_username = event["sender_username"]
        room_name = event["room_name"]
        timestamp = event["timestamp"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "sender_username": sender_username,
            "timestamp": timestamp,
            "room_name": room_name
        }))
