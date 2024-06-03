from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.post.api.v1.serializers.post_serializer import CommentSerializer
from apps.post.models.post_models import CommentModel, Post


class CommentAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, post_id):
        # Получаем все комментарии для данного поста
        comments = CommentModel.objects.filter(to_post=post_id)
        serializer_context = {"request": request}
        serializer = CommentSerializer(comments, many=True, context=serializer_context)
        return Response(serializer.data)

    def post(self, request, post_id):
        # Получаем пост, на который оставляется комментарий
        post = get_object_or_404(Post, pk=post_id)

        # Создаем новый комментарий
        # serializer_context = {'request': request}
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user, to_post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteAPIView(APIView):
    def get(sel, request, post_id, comment_id):
        comment = get_object_or_404(CommentModel, pk=comment_id, to_post=post_id, owner=request.user)
        serializer = CommentSerializer(comment)

        return Response(serializer.data)

    def delete(self, request, post_id, comment_id):
        # Получаем комментарий для удаления
        comment = get_object_or_404(CommentModel, pk=comment_id, to_post=post_id, owner=request.user)

        # Удаляем комментарий
        comment.delete()
        return Response({"message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)
