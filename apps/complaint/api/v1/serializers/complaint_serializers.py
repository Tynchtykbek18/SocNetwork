from rest_framework import serializers

from apps.complaint.models.complaint_models import Complaint
from apps.post.api.v1.serializers.post_serializer import (
    CommentSerializer,
    HashTagSerializer,
    LikeSerializer,
    PostFileSerializer,
)
from apps.post.models.post_models import Post
from apps.user.api.v1.serializers.user_serializer import (
    UniversalUserSerializer,
    UserSerializer,
)


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = "__all__"


class PostWithComplaintsSerializer(serializers.ModelSerializer):
    owner = UniversalUserSerializer(read_only=True)
    files = PostFileSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)
    hashtags = HashTagSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    tagged_users = UserSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["complaints_count"] = instance.complaints.count()
        return representation
