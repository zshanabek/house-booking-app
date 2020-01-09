from rest_framework import permissions


class IsHouseOwner(permissions.BasePermission):
    """
    Custom permission to allow owners of house to edit it.
    """

    def has_object_permission(self, request, view, obj):
        import pdb; pdb.set_trace()
        return obj.house.user == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow owners to see it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
