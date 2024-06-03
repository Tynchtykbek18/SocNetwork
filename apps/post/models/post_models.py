from django.db import models

from apps.common import BaseModel, MediaService
from apps.user.models import User


class HashTagModel(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    hashtags = models.ManyToManyField(HashTagModel, related_name="posts", blank=True)
    tagged_users = models.ManyToManyField(User, related_name="tagged_posts", blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.owner.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Сначала сохраняем пост

        # Затем добавляем хэштеги
        for tag in self.description.split():
            if tag.startswith("#"):
                hashtag, created = HashTagModel.objects.get_or_create(name=tag)
                self.hashtags.add(hashtag)

    # @property
    # def complaint_count(self):
    #     return self.complaints.count()  # Подсчет жалоб на этот пост


class PostFileModel(BaseModel, MediaService):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="post_files/")

    def __str__(self):
        return f"{self.post.owner.username} post file"

    def save(self, *args, **kwargs):
        # try:
        #     if self.file:
        #         self.compress_media("file", delete_source=True, max_width=600, max_height=600)
        # except Exception as e:
        #     logging.error(f"An error occurred: {e}")
        super().save(*args, **kwargs)


# @receiver(pre_delete, sender=PostFileModel)
# def user_avatar(sender, instance, **kwargs):
#     instance.file.delete(False)


class CommentModel(BaseModel):
    to_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=255)

    def __str__(self):
        return f"{self.owner.username} to {self.to_post.owner.username} post"


class LikeModel(BaseModel):
    to_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.owner.username} to {self.to_post.owner.username} post"
