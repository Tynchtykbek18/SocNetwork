from rest_framework import serializers

from apps.post.models.post_models import (
    CommentModel,
    HashTagModel,
    LikeModel,
    Post,
    PostFileModel,
)
from apps.user.api.v1.serializers.user_serializer import (
    UniversalUserSerializer,
    UserSerializer,
)


class PostFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = PostFileModel
        fields = "__all__"

    # def validate(self, value):
    #     # Проверяем формат файла
    #     allowed_formats = [
    #         "image/jpeg",
    #         "image/png",
    #         "image/gif",
    #         "video/mp4",
    #         "video/avi",
    #         "video/x-msvideo",
    #         "video/x-matroska",
    #         "video/quicktime",
    #         "video/x-ms-wmv",
    #     ]
    #     if value.content_type not in allowed_formats:
    #         raise serializers.ValidationError("Недопустимый формат файла. Разрешены только изображения и видео.")
    #     return value


class CommentSerializer(serializers.ModelSerializer):
    owner = UniversalUserSerializer(read_only=True)

    class Meta:
        model = CommentModel
        fields = ("id", "owner", "text")


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = "__all__"


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTagModel
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    owner = UniversalUserSerializer(read_only=True)
    files = PostFileSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)
    hashtags = HashTagSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    tagged_users = UserSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ["id", "owner", "description", "location", "tagged_users", "files", "hashtags", "comments", "likes"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Добавляем поле likes_count, представляющее количество лайков поста
        representation["likes_count"] = instance.likes.count()
        return representation
