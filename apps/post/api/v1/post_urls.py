from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.post.api.v1.apis.comment_api import CommentAPIView, CommentDeleteAPIView
from apps.post.api.v1.apis.like_api import LikeAPIView
from apps.post.api.v1.apis.post_api import PostFeed, PostViewSet

app_name = "post"

router = DefaultRouter()

router.register("", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
    path("feed/", PostFeed.as_view()),
    path("<int:post_id>/like/", LikeAPIView.as_view()),
    path("<int:post_id>/comments/", CommentAPIView.as_view()),
    path("<int:post_id>/comment/<int:comment_id>/", CommentDeleteAPIView.as_view()),
]
