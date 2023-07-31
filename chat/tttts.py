import json
import pytz
from urllib.parse import unquote
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import Message, ConnectionEstablished


class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def save_message(
        self,
        content,
        uploaded_file_url,
        author_pk,
    ):

        author = User.objects.get(pk=author_pk)
        if uploaded_file_url:
            uploaded_file_url = unquote(uploaded_file_url)

        message = Message.objects.create(
            author=author,
            content=content,
            upload=uploaded_file_url,
        )
        message.save()


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        content = text_data_json["content"]
        uploaded_file_url = text_data_json["uploaded_file_url"]
        author = text_data_json["author"]

        # Send message to room group
        user_timezone = pytz.timezone(self.scope["user"].timezone)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "content": content,
                "uploaded_url": uploaded_file_url,
                "author": author,
                "timestamp": timezone.localtime(timezone.now(), user_timezone).strftime(
                    "%Y-%m-%d %H:%M"
                ),
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "content": event["content"],
                    "uploaded_url": event["uploaded_url"],
                    "author": event["author"],
                    "timestamp": event["timestamp"],
                }
            )
        )
