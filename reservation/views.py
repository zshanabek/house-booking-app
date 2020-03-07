from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.db.models import Q
import datetime
from house.permissions import IsGuest, IsHost
from house.models import House
from .serializers import ReservationSerializer
from .models import Reservation
from .tasks import *


class ReservationHostViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsHost]

    def get_queryset(self):
        houses = self.request.user.house_set.all()
        qs = Reservation.objects.filter(
            Q(house__in=houses) & ~Q(status=4) & ~Q(status=5))
        return qs

    @action(detail=True, methods=['PATCH'])
    def accept(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.status = 1
        booking.save()
        tomorrow = booking.created_at + datetime.timedelta(days=1)
        send_email_on_approve(booking.house.name, self.request.user.full_name(),
                              booking.house.user.full_name(), booking.house.user.email, booking.id)
        set_reservation_as_inactive_after_approve.apply_async(
            args=[booking.id], eta=tomorrow)
        res = {'response': True, 'message': 'Бронь была принята'}
        return Response(res, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PATCH'])
    def reject(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.status = 2
        booking.save()
        send_email_on_reject(booking.house.name, self.request.user.full_name(),
                             booking.house.user.full_name(), booking.house.user.email, booking.id)
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
        serializer.is_valid(raise_exception=True)
        if int(self.request.data['guests']) > house.guests:
            res['response'] = False
            res['errors'] = "The number of booking guests can't exceed the number of house guests"
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        if house.user == self.request.user:
            res['response'] = False
            res['errors'] = "User can't reserve own house"
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        check_in = serializer.validated_data['check_in']
        check_out = serializer.validated_data['check_out']
        reservs = Reservation.objects.check_reservation(
            check_in=check_in, check_out=check_out, house=house, user=self.request.user)
        if reservs.exists():
            res['response'] = False
            res['errors'] = "В эти даты жилье занято"
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        reserv = serializer.save(user=self.request.user)
        tomorrow = reserv.created_at + datetime.timedelta(days=1)
        send_email_on_request(house.name, self.request.user.full_name(),
                              house.user.full_name(), house.user.email, reserv.id)
        set_reservation_as_inactive_after_request.apply_async(
            args=[reserv.id], eta=tomorrow)

    @action(detail=True, methods=['PATCH'])
    def cancel(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.message = request.data['message']
        d = booking.check_in - datetime.date.today()
        if (booking.status == 3 and d.days <= 5):
            res = {'response': False, 'message': 'Оплаченную бронь нельзя отменить по правилам отмены бронирования. Надо отменять за 5 дней до начала проживания'}
            return Response(res, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        booking.status = Reservation.CANCELED
        booking.save()
        send_email_on_cancel(booking.house.name, self.request.user.full_name(),
                             booking.house.user.full_name(), booking.house.user.email, booking.id)
        res = {'response': True, 'message': 'Статус брони был успешно изменен'}
        return Response(res, status=status.HTTP_200_OK)
