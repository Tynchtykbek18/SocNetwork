from django.db.models import Q
from django.shortcuts import redirect, reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.chat.api.v1.serializers.chat_serializers import (
    ConversationListSerializer,
    ConversationSerializer,
)
from apps.chat.models.chat_models import Conversation, Message
from apps.common.exceptions import ExceptionHandlerMixin
from apps.user.models import User


class StartConvoView(ExceptionHandlerMixin, APIView):
    def post(self, request):
        data = request.data.copy()
        username = data.pop("username")
        try:
            participant = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "You cannot chat with a non-existent user"})

        conversation = Conversation.objects.filter(
            Q(initiator=request.user, receiver=participant) | Q(initiator=participant, receiver=request.user)
        )
        if conversation.exists():
            return redirect(reverse("api:chats:get_conversation", args=(conversation[0].id,)))
        else:
            conversation = Conversation.objects.create(initiator=request.user, receiver=participant)
            serializer = ConversationSerializer(instance=conversation, context={'request': request})
            return Response(serializer.data)


class GetConversationView(ExceptionHandlerMixin, APIView):
    def get(self, request, convo_id):
        conversation = Conversation.objects.filter(id=convo_id)
        if not conversation.exists():
            return Response({"message": "Conversation does not exist"})
        else:
            serializer = ConversationSerializer(instance=conversation[0], context={'request': request})
            return Response(serializer.data)


class ConversationsView(ExceptionHandlerMixin, APIView):
    def get(self, request):
        conversation_list = Conversation.objects.filter(Q(initiator=request.user) | Q(receiver=request.user))
        serializer = ConversationListSerializer(instance=conversation_list, many=True, context={'request': request})
        return Response(serializer.data)


class DeleteMessageView(APIView):
    def delete(self, request, *args, **kwargs):
        message_id = kwargs.get("id")
        if not message_id:
            return Response({"message": "Message ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            message = Message.objects.get(id=message_id)
            if message.sender and message.receiver:
                message.delete()
                return Response({"message": "Message deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Message does not have users"}, status=status.HTTP_400_BAD_REQUEST)
        except Message.DoesNotExist:
            return Response({"message": "Message does not exist"}, status=status.HTTP_404_NOT_FOUND)


class DeleteConversationView(APIView):
    def delete(self, request, *args, **kwargs):
        conversation_id = kwargs.get("id")
        if not conversation_id:
            return Response({"message": "Conversation ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            if conversation.initiator or conversation.receiver:
                conversation.delete()
                return Response({"message": "Conversation deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Conversation does not have users"}, status=status.HTTP_400_BAD_REQUEST)
        except Conversation.DoesNotExist:
            return Response({"message": "Conversation does not exist"}, status=status.HTTP_404_NOT_FOUND)
