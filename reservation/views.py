from django.shortcuts import render
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.response import Response
from house.models import House
from rest_framework import viewsets
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        house = get_object_or_404(House, pk=request.data['house_id'])
        res = {}
        if request.data['guests'] >= house.guests:
            res['response'] = False
            res['errors'] = "The number of booking guests can't exceed the number of house guests"
            return Response(res, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        res['response'] = True
        return Response(res, status=status.HTTP_201_CREATED)
