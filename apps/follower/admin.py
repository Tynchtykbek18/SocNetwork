from django.contrib import admin

from apps.follower.models.models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "follower", "followed")
    list_display_links = ("id", "follower", "followed")
