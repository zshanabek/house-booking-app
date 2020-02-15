from django.shortcuts import render
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.response import Response
from house.models import House
from rest_framework import viewsets
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from house.permissions import IsGuest, IsHost
from .tasks import set_reservation_as_inactive, send_email_task


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
        res = {'response': True, 'message': 'Бронь была принята'}
        return Response(res, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PATCH'])
    def reject(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.accepted_house = False
        booking.save()
        res = {'response': True, 'message': 'Бронь была отказана'}
        return Response(res, status=status.HTTP_200_OK)


class ReservationGuestViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsGuest]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        house = get_object_or_404(House, pk=self.request.data['house_id'])
        res = {}
        if int(self.request.data['guests']) > house.guests:
            res['response'] = False
            res['errors'] = "The number of booking guests can't exceed the number of house guests"
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        if house.user == self.request.user:
            res['response'] = False
            res['errors'] = "User can't reserve own house"
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        serializer.is_valid(raise_exception=True)
        reserv = serializer.save(user=self.request.user)
        # send_email_task(house.name, self.request.user.full_name(),
        #                       house.user.full_name(), house.user.email, reserv.id)
        # set_reservation_as_inactive.apply_async(args=[reserv.id], eta=reserv.check_out)

    @action(detail=True, methods=['PATCH'])
    def cancel(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.message = request.data['message']
        booking.status = Reservation.CANCELED
        booking.save()
        res = {'response': True, 'message': 'Статус брони был успешно изменен'}
        return Response(res, status=status.HTTP_200_OK)
