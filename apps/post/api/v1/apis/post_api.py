from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common import IsAdminOrModerator, IsCurrentUser
from apps.follower.models.models import Follow
from apps.post.api.v1.serializers.post_serializer import (
    PostFileSerializer,
    PostSerializer,
)
from apps.post.models.post_models import Post
from apps.user.models import User


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrModerator | IsCurrentUser]

    def create(self, request, *args, **kwargs):
        try:
            if request.data.get("owner") != str(request.user.id):
                return Response(
                    {"error": "Вы не можете создать пост для другого пользователя."}, status=status.HTTP_403_FORBIDDEN
                )
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                post = serializer.save(owner=request.user)
                tagged_users = request.data.getlist("tagged_users")
                for user_id in tagged_users:
                    tagged_user = User.objects.get(pk=user_id)
                    post.tagged_users.add(tagged_user)
                files_data = request.FILES.getlist("files")
                for file_data in files_data:
                    file_serializer = PostFileSerializer(data={"post": post.pk, "file": file_data})
                    if file_serializer.is_valid():
                        file_serializer.save(post=post)
                    else:
                        post.delete()
                        raise serializers.ValidationError(file_serializer.errors)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=kwargs["pk"])
            if instance.owner != request.user:
                return Response({"error": "У вас нет прав доступа к такому запросу."}, status=status.HTTP_403_FORBIDDEN)
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=kwargs["pk"])
            if instance.owner != request.user:
                return Response({"error": "У вас нет прав доступа к этому запросу."}, status=status.HTTP_403_FORBIDDEN)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=kwargs["pk"])
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            user_id = request.query_params.get("user_id", None)
            hashtag = request.query_params.get("hashtag", None)

            if user_id:
                queryset = self.queryset.filter(owner_id=user_id)
            elif hashtag:
                queryset = self.queryset.filter(hashtags__name=hashtag)
            else:
                queryset = self.queryset.all()

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PostFeed(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        followed_users = Follow.objects.filter(follower=user).values_list("followed", flat=True)

        queryset = Post.objects.filter(owner__in=followed_users)

        serializer = PostSerializer(queryset, many=True)

        return Response(serializer.data)
