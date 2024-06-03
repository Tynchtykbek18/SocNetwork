from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.user.api.v1.apis import (
    SendPasswordResetEmailAPI,
    UserChangePasswordAPI,
    UserPasswordResetAPI,
)
from apps.user.api.v1.apis.user_apis import (
    ProfileViewSet,
    RegisterView,
    UserSearchAPIView,
    UserViewSet,
    VerifyEmail,
)
from apps.user.api.v1.apis.reset_password import SendPasswordResetCodeAPI, VerifyResetCodeAPI

app_name = "users"

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet)

urlpatterns = [
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path("register/", RegisterView.as_view(), name="user-register"),
    path("search-user/", UserSearchAPIView.as_view(), name="search-user"),
    # path("change-password/", UserChangePasswordAPI.as_view(), name="user-change-password"),
    # path("send-reset-password-email/", SendPasswordResetEmailAPI.as_view(), name="user-send-reset-password-email"),
    # path("reset-password/<uid>/<token>/", UserPasswordResetAPI.as_view(), name="user-reset-password"),
    path('send-reset-code/', SendPasswordResetCodeAPI.as_view(), name='send-reset-code'),
    path('verify-reset-code/', VerifyResetCodeAPI.as_view(), name='verify-reset-code'),
]

router.register("", UserViewSet)

urlpatterns += router.urls
