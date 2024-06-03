from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.post.api.v1.serializers.post_serializer import LikeSerializer
from apps.post.models.post_models import LikeModel, Post


class LikeAPIView(APIView):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        likes = LikeModel.objects.filter(to_post=post)

        serializer = LikeSerializer(likes, many=True)  # Создаем сериализатор для данных лайков
        return Response(serializer.data)

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)

        try:
            like = LikeModel.objects.get(owner=request.user, to_post=post)
            like.delete()  # Unlike the post
            return Response({"message": "Unliked"}, status=status.HTTP_204_NO_CONTENT)
        except LikeModel.DoesNotExist:
            LikeModel.objects.create(owner=request.user, to_post=post)  # Like the post
            return Response({"message": "Liked"}, status=status.HTTP_201_CREATED)
