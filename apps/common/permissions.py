from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsCurrentUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.status == "Модератор")
