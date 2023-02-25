from rest_framework import permissions


class is_owner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
