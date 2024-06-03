from rest_framework.serializers import ModelSerializer

from apps.follower.models.models import Follow
from apps.user.api.v1.serializers.user_serializer import UniversalUserSerializer


class FollowSerializer(ModelSerializer):
    followed = UniversalUserSerializer()
    follower = UniversalUserSerializer()

    class Meta:
        model = Follow
        fields = "__all__"
