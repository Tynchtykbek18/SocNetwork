from django.contrib import admin

from apps.post.models.post_models import CommentModel, LikeModel, Post, PostFileModel


class PostFileInline(admin.StackedInline):
    model = PostFileModel
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "location")
    list_display_links = ("id", "owner", "location")
    inlines = [PostFileInline]


@admin.register(CommentModel)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "to_post")
    list_display_links = ("id", "owner", "to_post")


@admin.register(LikeModel)
class LikeModelAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "to_post")
    list_display_links = ("id", "owner", "to_post")
