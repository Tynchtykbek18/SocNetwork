import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, mixins, response, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common import IsAdminOrModerator, IsCurrentUser
from apps.user.api.v1.serializers import (
    ProfileSerializer,
    RegisterSerializer,
    UserSerializer,
)
from apps.user.api.v1.serializers.user_serializer import (
    EmailVerificationSerializer,
    UniversalUserSerializer,
)
from apps.user.models import Profile, User
from apps.user.tasks import send


class UserViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrModerator | IsCurrentUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "email"]

    def get_queryset(self):
        if self.action == "unblock":
            return self.queryset.filter(is_active=False)
        return self.queryset.filter(is_active=True).exclude(Q(status="Модератор") | Q(is_superuser=True))

    def get_permissions(self):
        if self.action == ["block", "unblock"]:
            return [IsAdminOrModerator()]
        return [(IsAdminOrModerator | IsCurrentUser)()]

    @action(methods=["GET"], detail=False)
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def _send_notification(self, request, instance, email_template):
        current_site = get_current_site(request).domain
        context = {"user": instance, "site_name": f"http://{current_site}"}
        html_message = render_to_string(email_template, context)

        send_mail(
            subject="Important Announcement from Manasgram",
            message=None,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            html_message=html_message,
            fail_silently=False,
        )

    @action(["POST"], detail=True)
    def block(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()

        self._send_notification(request, instance, "block_user.html")

        return Response({"detail": f"User with {instance.username} is BLOCKED"}, status=status.HTTP_200_OK)

    @action(["POST"], detail=True)
    def unblock(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.is_active:
            instance.is_active = True
            instance.save()

            self._send_notification(request, instance, "unblock_user.html")

            return Response({"detail": f"User with {instance.username} is UNBLOCKED"}, status=status.HTTP_200_OK)
        else:
            raise ValidationError({"detail": "The user is not blocked."})


class UserSearchAPIView(generics.ListAPIView):
    serializer_class = UniversalUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.request.query_params.get("username", "")
        return User.objects.filter(username__icontains=username).exclude(Q(status="Модератор") | Q(is_superuser=True))


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrModerator | IsCurrentUser]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


def create_response(serializer, refresh_token, access_token, status_code, error=None):
    response_data = {
        "user_data": serializer.data,
        "refresh_token": str(refresh_token),
        "access_token": str(access_token),
    }
    if error:
        response_data["error"] = error

    return Response(response_data, status=status_code)


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data

        user_email = User.objects.get(email=user["email"])
        access_token = RefreshToken.for_user(user_email).access_token
        refresh_token = RefreshToken.for_user(user_email)
        current_site = get_current_site(request).domain
        relative_link = reverse("api:users:email-verify")
        absurl = "http://" + current_site + relative_link + "?token=" + str(access_token)
        email_body = "Hi " + user["username"] + " Use the link below to verify your email \n" + absurl
        try:
            # send.delay(email=user["email"], message=email_body)
            send(email=user["email"], message=email_body)
            return create_response(serializer, refresh_token, access_token, status.HTTP_201_CREATED)
        except ConnectionRefusedError:
            return create_response(
                serializer, refresh_token, access_token, status.HTTP_400_BAD_REQUEST, error="Email not sent"
            )


class VerifyEmail(GenericAPIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        "token", in_=openapi.IN_QUERY, description="Description", type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            print(payload)
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return response.Response({"email": "Successfully activated"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return response.Response({"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return response.Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
