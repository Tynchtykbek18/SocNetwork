from rest_framework import serializers
from apps.user.models import User
from django.core.mail import send_mail
from django.conf import settings
from apps.user.models import PasswordResetCode


class SendPasswordResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def create(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        reset_code, created = PasswordResetCode.objects.get_or_create(user=user)
        send_mail(
            'Password Reset Code',
            f'Your password reset code is {reset_code.code}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        validated_data['code'] = reset_code.code
        return validated_data


class VerifyResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email address")

        try:
            PasswordResetCode.objects.get(user=user, code=data['code'])
        except PasswordResetCode.DoesNotExist:
            raise serializers.ValidationError("Invalid reset code")

        return data

    def save(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        user.set_password(validated_data['new_password'])
        user.save()
        PasswordResetCode.objects.filter(user=user).delete()
        return user
