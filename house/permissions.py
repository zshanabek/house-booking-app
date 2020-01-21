from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsHost(permissions.BasePermission):
    """
    Custom permission to allow owners of house to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.house.user == request.user


class IsGuest(permissions.BasePermission):
    """
    Custom permission to allow guests to see it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
