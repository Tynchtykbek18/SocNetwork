from rest_framework import generics, status, permissions
from rest_framework.response import Response
from ..serializers.reset_password import SendPasswordResetCodeSerializer, VerifyResetCodeSerializer


class SendPasswordResetCodeAPI(generics.GenericAPIView):
    queryset = None
    serializer_class = SendPasswordResetCodeSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SendPasswordResetCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.save()
        return Response({
            "msg": "Password reset code sent. Please check your email.",
            "code": validated_data['code']
        }, status=status.HTTP_200_OK)


class VerifyResetCodeAPI(generics.GenericAPIView):
    queryset = None
    serializer_class = VerifyResetCodeSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = VerifyResetCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(validated_data=serializer.validated_data)
        return Response({"msg": "Password reset successfully."}, status=status.HTTP_200_OK)
