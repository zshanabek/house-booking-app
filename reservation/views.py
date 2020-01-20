from django.shortcuts import render
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.response import Response
from house.models import House
from rest_framework import viewsets
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from .permissions import IsGuest, IsHost


class ReservationHostViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsHost]

    def get_queryset(self):
        houses = self.request.user.house_set.all()
        qs = Reservation.objects.filter(house__in=houses)
        return qs

    @action(detail=True, methods=['PATCH'])
    def accept(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.accepted_house = True
        booking.save()
        return Response(res, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['PATCH'])
    def reject(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.accepted_house = False
        booking.save()
        return Response(res, status=status.HTTP_204_NO_CONTENT)


class ReservationGuestViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsGuest]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        house = get_object_or_404(House, pk=request.data['house_id'])
        res = {}
        if request.data['guests'] >= house.guests:
            res['response'] = False
            res['errors'] = "The number of booking guests can't exceed the number of house guests"
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        if house.user == request.user:
            res['response'] = False
            res['errors'] = "User can't reserve own house"
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        res['response'] = True
        return Response(res, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['PATCH'])
    def cancel(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.status = Reservation.CANCELED
        booking.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
