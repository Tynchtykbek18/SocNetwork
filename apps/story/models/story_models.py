from django.db import models
from django.utils import timezone

from apps.common import BaseModel, MediaService
from apps.user.models import User


class StoryModel(BaseModel, MediaService):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stories", blank=True, null=True)
    file = models.FileField(upload_to="stories/")
    expiration_time = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.owner.username}'s story"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.expiration_time:
            self.expiration_time = self.created_at + timezone.timedelta(hours=24)
            self.save(update_fields=["expiration_time"])
