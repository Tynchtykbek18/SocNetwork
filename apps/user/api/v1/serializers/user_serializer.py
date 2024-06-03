from rest_framework import serializers

from apps.follower.models.models import Follow
from apps.user.models import Profile, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "owner", "fullname", "avatar", "faculty", "major", "stud_number", "more", "course")


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    has_story = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "status",
            "profile",
            "following_count",
            "followers_count",
            "is_following",
            "has_story",
        )

    def get_followers_count(self, obj):
        return Follow.objects.filter(followed=obj).count()

    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj).count()

    def get_is_following(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Follow.objects.filter(follower=request.user, followed=obj).exists()
        return False

    def get_has_story(self, obj):
        return obj.stories.exists()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, data):
        email = data.get("email")
        username = data.get("username")

        errors = {}

        if User.objects.filter(email=email).exists():
            errors["email"] = ["Пользователь с таким email существует."]

        if User.objects.filter(username=username).exists():
            errors["username"] = ["Пользователь с таким username существует."]

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user


class UniversalUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    has_story = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "avatar", "has_story", "status"]

    def get_avatar(self, obj):
        request = self.context.get("request")
        if request and obj.profile.avatar:
            return request.build_absolute_uri(obj.profile.avatar.url)
        return None

    def get_has_story(self, obj):
        return obj.stories.filter(is_active=True).exists()


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]
