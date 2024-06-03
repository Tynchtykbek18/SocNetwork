from django.contrib import admin

from apps.story.models.story_models import StoryModel


@admin.register(StoryModel)
class StoryModelAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "expiration_time", "is_active")
    list_display_links = ("id", "owner", "expiration_time", "is_active")
    search_fields = ("expiration_time", "is_active")
