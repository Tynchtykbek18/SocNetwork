from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from ..common.custom_token import CustomTokenObtainPairView

app_name = "api"

urlpatterns = [
    path("users/", include("apps.user.api.v1.user_url", namespace="users")),
    path("posts/", include("apps.post.api.v1.post_urls", namespace="posts")),
    path("menus/", include("apps.menu.urls", namespace="menus")),
    path("timetables/", include("apps.timetable.api.v1.urls", namespace="timetable")),
    path("", include("apps.follower.api.v1.follower_urls", namespace="subscribe")),
    path("stories/", include("apps.story.api.v1.story_urls", namespace="stories")),
    path("complaints/", include("apps.complaint.api.v1.complaint_urls", namespace="complaint")),
    path("chats/", include("apps.chat.api.v1.chat_urls", namespace="chats")),
]

# token
urlpatterns += [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
