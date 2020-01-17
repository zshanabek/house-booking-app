from rest_framework import permissions


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
