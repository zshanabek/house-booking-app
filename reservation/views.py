from django.shortcuts import render
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.response import Response
from house.models import House
from rest_framework import viewsets
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        qs = Reservation.objects.all()
        if (self.request.user.user_type == 0):
            qs = qs.filter(user=self.request.user.id)
        else:
            houses = self.request.user.house_set.all()
            qs = qs.filter(house__in=houses)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        house = get_object_or_404(House, pk=request.data['house_id'])
        res = {}
        if request.data['guests'] >= house.guests:
            res['response'] = False
            res['errors'] = "The number of booking guests can't exceed the number of house guests"
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        if request.user.user_type != 0:
            res['response'] = False
            res['errors'] = "Forbidden to reserve. Only usual users can reserve house"
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        res['response'] = True
        return Response(res, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['PUT'])
    def accept(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.accepted_house = True
        booking.save()
        res = {}
        res['response'] = True
        return Response(res, status=status.HTTP_204_NO_CONTENT)
