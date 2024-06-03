from django.db import models

from apps.common.base_model import BaseModel
from apps.user.models import User


class Conversation(BaseModel):
    initiator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="convo_starter")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="convo_participant")
    start_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.initiator} to {self.receiver}"


class Message(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="message_sender")
    text = models.CharField(max_length=200, blank=True)
    attachment = models.FileField(blank=True)
    duration = models.CharField(default='', max_length=100, blank=True, null=True)
    conversation_id = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.sender.username
