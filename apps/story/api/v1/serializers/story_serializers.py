from rest_framework.serializers import ModelSerializer

from apps.story.models.story_models import StoryModel
from apps.user.api.v1.serializers.user_serializer import UniversalUserSerializer


class StoryListSerializer(ModelSerializer):
    owner = UniversalUserSerializer()

    class Meta:
        model = StoryModel
        fields = "__all__"


class StoryCreateSerializer(ModelSerializer):

    class Meta:
        model = StoryModel
        fields = "__all__"
