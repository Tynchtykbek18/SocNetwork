from channels.exceptions import DenyConnection
from django.db.models import Q
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.core.files.base import ContentFile
import base64
import json
import secrets
from django.conf import settings

from apps.chat.api.v1.serializers.chat_serializers import MessageSerializer
from apps.chat.models.chat_models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Проверка, является ли пользователь участником чата
        try:
            conversation = Conversation.objects.get(id=int(self.room_name))
            if not (self.scope["user"] == conversation.initiator or self.scope["user"] == conversation.receiver):
                raise DenyConnection("Not a participant of the chat.")
        except Conversation.DoesNotExist:
            raise DenyConnection("Chat does not exist.")

        # Подключение к группе
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Отключение от группы
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Получение сообщения от WebSocket
    def receive(self, text_data=None, bytes_data=None):
        # Обработка полученного сообщения
        text_data_json = json.loads(text_data)
        text_data_json["sender"] = self.scope["user"].id

        # Сохранение сообщения в базе данных
        conversation = Conversation.objects.get(id=int(self.room_name))
        sender = self.scope["user"]
        duration = text_data_json.get('duration', '') # Получаем duration из JSON

        message, attachment = text_data_json["message"], text_data_json.get("attachment")
        if attachment:
            file_str, file_ext = attachment["data"], attachment["format"]
            file_data = ContentFile(base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}")
            _message = Message.objects.create(
                sender=sender,
                attachment=file_data,
                text=message,
                conversation_id=conversation,
                duration=duration,
            )
        else:
            _message = Message.objects.create(
                sender=sender,
                text=message,
                conversation_id=conversation,
                duration=duration,
            )

        # Adding base URL to context for the serializer
        context = {'base_url': settings.WEBSOCKET_BASE_URL}
        serializer = MessageSerializer(instance=_message, context=context)

        # Отправка сообщения отправителю
        self.send(text_data=json.dumps(serializer.data))

        # Отправка сообщения в группу
        chat_type = {"type": "chat_message"}
        return_dict = {**chat_type, **serializer.data, "sender_id": sender.id}
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )

    # Получение сообщения от группы
    def chat_message(self, event):
        sender_id = event.get("sender_id")
        current_user_id = self.scope["user"].id

        # Отправка сообщения другим пользователям
        if sender_id != current_user_id:
            self.send(text_data=json.dumps(event))
