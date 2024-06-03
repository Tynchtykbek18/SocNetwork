from django.contrib import admin
from django.contrib.auth.hashers import make_password

from apps.user.models import Profile, User


class CustomUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password)
        obj.save()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    exec = 1


@admin.register(User)
class UserAdmin(CustomUserAdmin):
    list_display = ("id", "username", "email", "status", "is_staff", "is_active")
    list_display_links = ("id", "username", "email")
    search_fields = ("username", "email", "status")
    list_filter = ("status", "is_staff", "is_active")
    inlines = (ProfileInline,)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "fullname", "stud_number", "faculty", "major", "course")
    list_display_links = ("id", "fullname", "stud_number", "faculty", "major", "course")
    search_fields = ("fullname", "stud_number")
    list_filter = ("major", "course", "faculty")
