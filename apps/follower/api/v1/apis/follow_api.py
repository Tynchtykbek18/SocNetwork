from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.follower.api.v1.serializers.follow_serializers import FollowSerializer
from apps.follower.models.models import Follow
from apps.user.models import User


class FollowAPIView(APIView):
    def post(self, request, user_id):
        try:
            followed_user = User.objects.get(pk=user_id)
            follower = request.user

            # Проверяем, подписан ли уже пользователь
            if not Follow.objects.filter(follower=follower, followed=followed_user).exists():
                follow = Follow(follower=follower, followed=followed_user)
                follow.save()
                serializer = FollowSerializer(follow)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Если уже подписан, то отписываемся
                Follow.objects.filter(follower=follower, followed=followed_user).delete()
                return Response({"detail": "Вы отписались от этого пользователя."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)


class FollowersListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Follow.objects.filter(followed_id=user_id)


class FollowingListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Follow.objects.filter(follower_id=user_id)
