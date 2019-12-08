from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from house.serializers import HouseSerializer, ReviewSerializer
from house.models import (
    House, Photo, AccommodationHouse, Review, Favourite
)


class HouseViewSet(ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('address', 'city')
    filterset_fields = ('floor', 'rooms')

    def create(self, request):
        serializer = HouseSerializer(data=request.data)
        res = {}
        if serializer.is_valid():
            house = serializer.save(user=self.request.user)
            photos = list(request.data['photos'])
            accoms = list(request.data['accoms'])
            for photo in photos:
                Photo.objects.create(
                    image=photo, house_id=house.id
                )
            for accom in accoms:
                AccommodationHouse.ModelViewSetobjects.create(
                    house_id=house.id, accom_id=accom
                )
            res['response'] = True
        else:
            res['response'] = False
            res['errors'] = serializer.errors

        return Response(res, status=status.HTTP_200_OK)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(house=self.kwargs['house_pk'])

    def create(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data)
        res = {}
        house = get_object_or_404(House, pk=kwargs['house_pk'])
        if serializer.is_valid():
            r = serializer.save(house=house, user=self.request.user)
            res['response'] = True
        else:
            res['response'] = False
            res['errors'] = serializer.errors

        return Response(res, status=status.HTTP_200_OK)
