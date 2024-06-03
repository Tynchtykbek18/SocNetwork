from django.db import models

from apps.post.models.post_models import Post


class Complaint(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="complaints", null=True, blank=True)
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
