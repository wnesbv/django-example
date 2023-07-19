
from datetime import datetime, timedelta
import json, jwt

from asgiref.sync import sync_to_async

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, AnonymousUser

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from user_ordinary.models import UserOrdinary
from user_privileged.models import UserPrivileged

from .models import UserChat


def get_username(username):
    user_name = get_object_or_404(User.objects, username=username)
    return user_name


def get_pr_user(mail):
    mail = get_object_or_404(UserPrivileged.objects, mail=mail)
    return mail


def get_or_user(mail):
    mail = get_object_or_404(UserOrdinary.objects, mail=mail)
    return mail


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        username = self.scope["user"]
        if username != AnonymousUser() and "privileged" not in self.scope["cookies"]:
            self.user = self.scope["user"]

            user_id = self.scope["session"]["_auth_user_id"]
            self.group_name = f"{user_id}"

            print(" user..", self.user)
            print(" _auth_user_id..", user_id)

        if "privileged" in self.scope["cookies"]:
            token = self.scope["cookies"]["privileged"]
            payload = jwt.decode(token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
            mail = payload["mail"]
            self.pr_user = mail
            user_id = payload["id"]
            self.group_name = f"{user_id}"

            print(" pr_user..", self.pr_user)

        if "ordinary" in self.scope["cookies"]:
            token = self.scope["cookies"]["ordinary"]
            payload = jwt.decode(token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
            mail = payload["mail"]
            self.ordinary = mail
            user_id = payload["id"]
            self.group_name = f"{user_id}"

            print(self.ordinary)

        # Добавляем новую комнату
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # Принимаем подключаем
        await self.accept()

    async def disconnect(self, close_code):
        # Отключаем пользователя
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    @database_sync_to_async
    # Создания нового сообщения в БД
    def new_message(self, message):

        # Создаём сообщение в БД
        username = self.scope["user"]
        if username != AnonymousUser() and "privileged" not in self.scope["cookies"]:
            user_chat = get_username(username)

            UserChat.objects.create(
                nick=username,
                user_chat=user_chat,
                remark=message,
                recipient=self.group_name,
                created_at=datetime.now(),
            )
        if "privileged" in self.scope["cookies"]:
            mail = self.pr_user
            pr_chat = get_pr_user(mail)

            UserChat.objects.create(
                nick=username,
                pr_chat=pr_chat,
                remark=message,
                recipient=self.group_name,
                created_at=datetime.now(),
            )
        if "ordinary" in self.scope["cookies"]:
            mail = self.ordinary
            or_chat = get_or_user(mail)

            UserChat.objects.create(
                nick=mail,
                or_chat=or_chat,
                remark=message,
                recipient=self.group_name,
                created_at=datetime.now(),
            )

    # Принимаем сообщение от пользователя

    async def receive(self, text_data=None, bytes_data=None):

        # Форматируем сообщение из JSON
        text_data_json = json.loads(text_data)

        # Получаем текст сообщения
        message = text_data_json["message"]
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        username = self.scope["user"]
        if username != AnonymousUser() and "privileged" not in self.scope["cookies"]:

            # Добавляем сообщение в БД
            await self.new_message(message=message)

            # Отправляем сообщение
            nick = str(self.scope["user"])
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_message",
                    "nick": nick,
                    "message": message,
                    "created_at": created_at,
                },
            )
        if "privileged" in self.scope["cookies"]:
            # Добавляем сообщение в БД
            await self.new_message(message=message)

            # Отправляем сообщение
            nick = self.pr_user
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_message",
                    "nick": nick,
                    "message": message,
                    "created_at": created_at,
                },
            )

        if "ordinary" in self.scope["cookies"]:

            # Добавляем сообщение в БД
            await self.new_message(message=message)

            # Отправляем сообщение
            nick = self.ordinary
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_message",
                    "nick": nick,
                    "message": message,
                    "created_at": created_at,
                },
            )

    # Метод для отправки сообщения клиентам
    async def chat_message(self, event):
        # Получаем сообщение от receive
        nick = event["nick"]
        message = event["message"]
        created_at = event["created_at"]

        # Отправляем сообщение клиентам
        await self.send(
            text_data=json.dumps(
                {
                    "nick": nick,
                    "message": message,
                    "created_at": created_at,
                },
                ensure_ascii=False,
            )
        )
