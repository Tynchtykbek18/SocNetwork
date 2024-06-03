from rest_framework import serializers
from apps.chat.models.chat_models import Conversation, Message
from apps.user.api.v1.serializers.user_serializer import UniversalUserSerializer
from config import settings


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ("conversation_id",)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request', None)

        # Using a fallback URL for WebSocket context
        if request:
            base_url = request.build_absolute_uri('/')
        else:
            base_url = f"{settings.WEBSOCKET_BASE_URL}"

        if instance.attachment:
            ret['attachment'] = base_url + instance.attachment.url
        return ret


class ConversationListSerializer(serializers.ModelSerializer):
    initiator = UniversalUserSerializer()
    receiver = UniversalUserSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["id", "initiator", "receiver", "last_message"]

    def get_last_message(self, instance):
        message = instance.message_set.first()
        context = self.context
        return MessageSerializer(instance=message, context=context).data if message else None


class ConversationSerializer(serializers.ModelSerializer):
    initiator = UniversalUserSerializer()
    receiver = UniversalUserSerializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ["id", "initiator", "receiver", "message_set"]

    def to_representation(self, instance):
        context = self.context
        ret = super().to_representation(instance)
        ret['message_set'] = MessageSerializer(instance.message_set.all(), many=True, context=context).data
        return ret
