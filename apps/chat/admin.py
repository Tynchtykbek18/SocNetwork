from django.contrib import admin

from .models.chat_models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "initiator", "receiver", "start_time")
    list_display_links = ("id", "initiator", "receiver")
    search_fields = ("id", "initiator__username", "receiver__username")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "text", "conversation_id", "attachment")
    list_display_links = ("id", "sender", "text", "conversation_id", "attachment")
    search_fields = ("sender__username", "conversation_id__initiator__username", "text")
