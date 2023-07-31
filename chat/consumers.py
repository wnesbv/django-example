
from datetime import datetime, timedelta
from collections import defaultdict

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
from .img import update_file


def get_username(username):
    user_name = get_object_or_404(User.objects, username=username)
    return user_name

def get_pr_user(username):
    username = get_object_or_404(UserPrivileged.objects, username=username)
    return username

def get_or_user(mail):
    mail = get_object_or_404(UserOrdinary.objects, mail=mail)
    return mail


class ChatConsumer(AsyncWebsocketConsumer):

    who_there = defaultdict(set)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = None
        self.user = None
        self.privileged = None
        self.ordinary = None

    async def connect(self):

        self.group_name = self.scope["url_route"]["kwargs"]["uustr"]
        print(" group_name..", self.group_name)

        if self.scope["user"] != AnonymousUser() and "privileged" not in self.scope["cookies"]:

            self.user = self.scope["user"]
            user_id = self.scope["session"]["_auth_user_id"]

            print(" user..", self.user)
            print(" _auth_user_id..", user_id)

        if "privileged" in self.scope["cookies"]:

            token = self.scope["cookies"]["privileged"]
            payload = jwt.decode(token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
            username = payload["username"]

            self.privileged = username
            print(" privileged..", self.privileged)

        if "ordinary" in self.scope["cookies"]:
            token = self.scope["cookies"]["ordinary"]
            payload = jwt.decode(token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
            mail = payload["mail"]

            self.ordinary = mail
            print(" ordinary..", self.ordinary)


        # Принимаем подключаем
        await self.accept()

        # Добавляем новую комнату
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        quantity = len(
            self.channel_layer.groups.get(self.group_name, {}).items()
        )
        print(" len..", quantity)


        # ..
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.scope["user"] != AnonymousUser() and "privileged" not in self.scope["cookies"]:

            self.who_there[self.group_name].add(str(self.user))

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'user_connect',
                    'username': list(self.who_there[self.group_name]),
                    'message': quantity,
                    "created_at": created_at,
                }
            )
        if "privileged" in self.scope["cookies"]:

            self.who_there[self.group_name].add(self.privileged)

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'user_connect',
                    'username': list(self.who_there[self.group_name]),
                    'message': quantity,
                    "created_at": created_at,
                }
            )
        if "ordinary" in self.scope["cookies"]:

            self.who_there[self.group_name].add(self.ordinary)

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'user_connect',
                    'username': list(self.who_there[self.group_name]),
                    'message': quantity,
                    "created_at": created_at,
                }
            )


    # ..
    async def disconnect(self, close_code):

        # Отключаем пользователя
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

        if self.scope["user"] != AnonymousUser() and "privileged" not in self.scope["cookies"]:
            self.who_there[self.group_name].remove(self.user)

        if "privileged" in self.scope["cookies"]:
            self.who_there[self.group_name].remove(self.privileged)

        if "ordinary" in self.scope["cookies"]:
            self.who_there[self.group_name].remove(self.ordinary)


    async def user_connect(self, event):
        username = event["username"]
        message = event["message"]
        created_at = event["created_at"]

        await self.send(text_data=json.dumps({
            'type': 'player_connect',
            "username": username,
            "message": message,
            "created_at": created_at,
        }))


    # ..
    @database_sync_to_async
    # Создания нового сообщения в БД
    def new_file(self, file):

        # Создаём сообщение в БД
        username = self.scope["user"]
        if username != AnonymousUser() and "privileged" not in self.scope["cookies"]:

            user_chat = get_username(username)

            UserChat.objects.create(
                nick=username,
                user_chat=user_chat,
                file=update_file(self.group_name, file),
                recipient=self.group_name,
                created_at=datetime.now(),
            )
        if "privileged" in self.scope["cookies"]:

            username = self.privileged
            pr_chat = get_pr_user(username)

            UserChat.objects.create(
                nick=username,
                pr_chat=pr_chat,
                file=update_file(self.group_name, file),
                recipient=self.group_name,
                created_at=datetime.now(),
            )
        if "ordinary" in self.scope["cookies"]:

            mail = self.ordinary
            or_chat = get_or_user(mail)

            UserChat.objects.create(
                nick=mail,
                or_chat=or_chat,
                file=update_file(self.group_name, file),
                recipient=self.group_name,
                created_at=datetime.now(),
            )

    # ..
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

            username = self.privileged
            pr_chat = get_pr_user(username)

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

    # ..
    # Принимаем сообщение от пользователя

    async def receive(self, text_data=None, bytes_data=None):

        # Форматируем сообщение из JSON
        text_data_json = json.loads(text_data)
        print("text_data..", text_data)

        # Получаем текст сообщения

        message = text_data_json.get("message")
        file = text_data_json.get("file")

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self.scope["user"] != AnonymousUser() and "privileged" not in self.scope["cookies"]:

            # Отправляем сообщение
            username = str(self.scope["user"])
            if file:
                # Добавляем сообщение в БД
                await self.new_file(file=file)
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "chat_message",
                        "username": username,
                        "file": file,
                        "created_at": created_at,
                    },
                )
            if message:
                await self.new_message(message=message)
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "chat_message",
                        "username": username,
                        "message": message,
                        "created_at": created_at,
                    },
                )

        if "privileged" in self.scope["cookies"]:

            # Отправляем сообщение
            username = self.privileged
            if file:
                # Добавляем сообщение в БД
                await self.new_file(file=file)
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "chat_message",
                        "username": username,
                        "file": file,
                        "created_at": created_at,
                    },
                )
            if message:
                await self.new_message(message=message)
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "chat_message",
                        "username": username,
                        "message": message,
                        "created_at": created_at,
                    },
                )


        if "ordinary" in self.scope["cookies"]:

            # Отправляем сообщение
            username = self.ordinary
            if file:
                # Добавляем сообщение в БД
                await self.new_file(file=file)
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "chat_message",
                        "username": username,
                        "file": file,
                        "created_at": created_at,
                    },
                )
            if message:
                await self.new_message(message=message)
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "chat_message",
                        "username": username,
                        "message": message,
                        "created_at": created_at,
                    },
                )

    # ..
    # Метод для отправки сообщения клиентам
    async def chat_message(self, event):
        #print(" event..", event)

        # Получаем сообщение от receive
        username = event["username"]
        message = event.get("message")
        file = event.get("file")
        created_at = event["created_at"]

        if self.scope["user"] != AnonymousUser() and "privileged" not in self.scope["cookies"]:

            # Отправляем сообщение клиентам
            await self.send(
                text_data=json.dumps(
                    {
                        "username": username,
                        "message": message,
                        "file": file,
                        "created_at": created_at,
                    },
                    ensure_ascii=False,
                )
            )
        if "privileged" in self.scope["cookies"]:

            await self.send(
                text_data=json.dumps(
                    {
                        "username": username,
                        "message": message,
                        "file": file,
                        "created_at": created_at,
                    },
                    ensure_ascii=False,
                )
            )

        if "ordinary" in self.scope["cookies"]:

            await self.send(
                text_data=json.dumps(
                    {
                        "username": username,
                        "message": message,
                        "file": file,
                        "created_at": created_at,
                    },
                    ensure_ascii=False,
                )
            )
