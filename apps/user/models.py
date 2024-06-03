from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common import BaseModel, MediaService
import random


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    class Status(models.TextChoices):
        user = "Пользователь", "Пользователь"
        head_st = "Староста", "Староста"
        moderator = "Модератор", "Модератор"

    status = models.CharField(choices=Status.choices, default=Status.user, max_length=20)

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        ordering = ("-id",)
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "refresh": str(refresh.access_token),
        }

    def __str__(self):
        return self.email


class Profile(BaseModel, MediaService):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    fullname = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    stud_number = models.CharField(max_length=10, unique=True)
    faculty = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    course = models.PositiveIntegerField(default=1)
    more = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # try:
        #     # if advertisement new added
        #     if self.avatar:
        #         # image compress
        #         self.compress_media("avatar", delete_source=True, max_width=300, max_height=300)
        # except Exception as e:
        #     logging.error(f"An error occurred: {e}")
        if not self.pk:
            self.pk = self.owner.pk

        super().save(*args, **kwargs)

    def __str__(self):
        return self.owner.username


# @receiver(pre_delete, sender=Profile)
# def user_avatar(sender, instance, **kwargs):
#     instance.avatar.delete(False)


class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(1000, 9999))
        super().save(*args, **kwargs)
