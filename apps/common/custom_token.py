from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class CustomTokenObtainPairSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username_or_email = attrs.get("username_or_email")
        password = attrs.get("password")

        user = None
        if "@" in username_or_email:
            user = User.objects.filter(email=username_or_email).first()
        else:
            user = User.objects.filter(username=username_or_email).first()

        if user and user.check_password(password):
            attrs["user"] = user
            return attrs

        raise serializers.ValidationError("Invalid credentials")


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        user_status = "Админ" if user.is_superuser else user.status

        data = {"refresh": str(refresh), "access": str(refresh.access_token), "status": user_status}
        return Response(data, status=status.HTTP_200_OK)
