from django.urls import path

from ..v1.apis.follow_api import FollowAPIView, FollowersListView, FollowingListView

app_name = "follower"

urlpatterns = [
    path("follow/<int:user_id>/", FollowAPIView.as_view()),
    path("followers/<int:user_id>/", FollowersListView.as_view(), name="followers-list"),
    path("following/<int:user_id>/", FollowingListView.as_view(), name="following-list"),
]
