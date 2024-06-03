from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.api.v1.serializers import (
    SendPasswordResetEmailSerializer,
    UserChangePasswordSerializer,
    UserPasswordResetSerializer,
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserChangePasswordAPI(generics.GenericAPIView):
    queryset = None
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        return Response({"msg": "Password Changed Successfully"}, status=status.HTTP_200_OK)


class SendPasswordResetEmailAPI(generics.GenericAPIView):
    queryset = None
    serializer_class = SendPasswordResetEmailSerializer

    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response({"msg": "Password Reset link send. Please check your Email"}, status=status.HTTP_200_OK)


class UserPasswordResetAPI(generics.GenericAPIView):
    queryset = None
    serializer_class = UserPasswordResetSerializer

    def post(self, request, uid, token):
        serializer = UserPasswordResetSerializer(data=request.data, context={"uid": uid, "token": token})
        serializer.is_valid(raise_exception=True)
        return Response({"msg": "Password Reset Successfully"}, status=status.HTTP_200_OK)
