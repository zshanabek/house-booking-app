from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import House
from reservation.models import Reservation


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


class IsGuestLived(permissions.BasePermission):
    """
    Custom permission to allow guests to see it.
    """

    def has_permission(self, request, view):
        # house = get_object_or_404(House, pk=view.kwargs['house_pk'])
        # Reservation
        return True

    def has_object_permission(self, request, view, obj):
        import pdb
        pdb.set_trace()
        return obj.user == request.user
