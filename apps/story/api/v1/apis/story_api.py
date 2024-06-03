from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.story.api.v1.serializers.story_serializers import (
    StoryCreateSerializer,
    StoryListSerializer,
)
from apps.story.models.story_models import StoryModel


class StoryCreate(generics.CreateAPIView):
    serializer_class = StoryCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, is_active=True)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            response.data["message"] = "Story created successfully"
        return response


class StoryList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Получаем queryset всех сторисов, упорядоченных сначала по пользователю, а затем по времени создания
        stories = StoryModel.objects.filter(is_active=True).order_by("owner", "-created_at")

        # Создаем сериализатор и сериализуем данные
        serializer = StoryListSerializer(stories, many=True, context={"request": request})

        # Возвращаем данные в виде JSON
        return Response(serializer.data)


class UserStoryList(generics.ListAPIView):
    serializer_class = StoryListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        queryset = StoryModel.objects.filter(owner=user_id, is_active=True)

        return queryset


class StoryDetail(generics.RetrieveAPIView):
    queryset = StoryModel.objects.filter(is_active=True)
    serializer_class = StoryListSerializer
    permission_classes = [IsAuthenticated]
