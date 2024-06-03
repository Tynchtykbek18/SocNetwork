from django.db import models

from apps.user.models import User


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return self.follower.username

    class Meta:
        unique_together = ["follower", "followed"]
