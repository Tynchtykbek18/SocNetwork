import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from celery import shared_task
from django.utils import timezone
from apps.story.models.story_models import StoryModel


@shared_task
def update_story_statuses():
    stories = StoryModel.objects.filter(is_active=True, expiration_time__lt=timezone.now())
    for story in stories:
        story.is_active = False
        story.save(update_fields=['is_active'])
