from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from house.serializers import HouseSerializer, ReviewSerializer, \
AccommodationHouseSerializer, AccommodationSerializer,\
HouseTypeSerializer, CitySerializer, NearBuildingSerializer, NearBuildingHouseSerializer
from house.models import (
    House, Photo, Accommodation, AccommodationHouse, HouseType, Review, Favourite, City, NearBuilding, NearBuildingHouse
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
                AccommodationHouse.objects.create(
                    house_id=house.id, accom_id=accom
                )
            res['response'] = True
        else:
            res['response'] = False
            res['errors'] = serializer.errors

        return Response(res, status=status.HTTP_200_OK)


class AccommodationViewSet(ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    pagination_class = None


class AccommodationHouseViewSet(ModelViewSet):
    queryset = AccommodationHouse.objects.all()
    serializer_class = AccommodationHouseSerializer
    pagination_class = None


class NearBuildingViewSet(ModelViewSet):
    queryset = NearBuilding.objects.all()
    serializer_class = NearBuildingSerializer
    pagination_class = None


class NearBuildingHouseViewSet(ModelViewSet):
    queryset = NearBuildingHouse.objects.all()
    serializer_class = NearBuildingHouseSerializer
    pagination_class = None


class HouseTypeViewSet(ModelViewSet):
    queryset = HouseType.objects.all()
    serializer_class = HouseTypeSerializer
    pagination_class = None


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


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = None
