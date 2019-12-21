from django.shortcuts import render
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.response import Response
from house.models import House
from rest_framework import permissions, status, mixins, generics
from django.shortcuts import get_object_or_404


class ReservationList(mixins.ListModelMixin,
                      generics.GenericAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user.id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ReservationCreate(generics.CreateAPIView):

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        serializer = ReservationSerializer(data=request.data)
        res = {}
        house = get_object_or_404(House, pk=kwargs['pk'])
        if serializer.is_valid():
            r = serializer.save(house=house, user=self.request.user)
            res['response'] = True
        else:
            res['response'] = False
            res['errors'] = serializer.errors
        return Response(res, status=status.HTTP_200_OK)
        

class ReservationList(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data)


class ReservationList(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data)


class ReservationDetail(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user.id)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
