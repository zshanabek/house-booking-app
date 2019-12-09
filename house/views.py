from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from house import serializers as home_serializers
from house import models as house_models


class HouseViewSet(ModelViewSet):
    queryset = house_models.House.objects.all()
    serializer_class = home_serializers.HouseSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('address', 'city')
    filterset_fields = ('floor', 'rooms')

    def create(self, request):
        serializer = home_serializers.HouseSerializer(data=request.data)
        res = {}
        if serializer.is_valid():
            house = serializer.save(user=self.request.user)
            photos = list(request.data['photos'])
            accoms = list(request.data['accoms'])
            rules = list(request.data['rules'])
            for photo in photos:
                house_models.Photo.objects.create(
                    image=photo, house_id=house.id
                )
            for accom in accoms:
                house_models.AccommodationHouse.objects.create(
                    house_id=house.id, accom_id=accom
                )
            for rule in rules:
                house_models.RuleHouse.objects.create(
                    house_id=house.id, rule_id=rule
                )
            res['response'] = True
        else:
            res['response'] = False
            res['errors'] = serializer.errors

        return Response(res, status=status.HTTP_200_OK)


class AccommodationViewSet(ModelViewSet):
    queryset = house_models.Accommodation.objects.all()
    serializer_class = home_serializers.AccommodationSerializer
    pagination_class = None


class AccommodationHouseViewSet(ModelViewSet):
    queryset = house_models.AccommodationHouse.objects.all()
    serializer_class = home_serializers.AccommodationHouseSerializer
    pagination_class = None


class NearBuildingViewSet(ModelViewSet):
    queryset = house_models.NearBuilding.objects.all()
    serializer_class = home_serializers.NearBuildingSerializer
    pagination_class = None


class NearBuildingHouseViewSet(ModelViewSet):
    queryset = house_models.NearBuildingHouse.objects.all()
    serializer_class = home_serializers.NearBuildingHouseSerializer
    pagination_class = None


class HouseTypeViewSet(ModelViewSet):
    queryset = house_models.HouseType.objects.all()
    serializer_class = home_serializers.HouseTypeSerializer
    pagination_class = None


class ReviewViewSet(ModelViewSet):
    queryset = house_models.Review.objects.all()
    serializer_class = home_serializers.ReviewSerializer

    def get_queryset(self):
        return house_models.Review.objects.filter(house=self.kwargs['house_pk'])

    def create(self, request, *args, **kwargs):
        serializer = home_serializers.ReviewSerializer(data=request.data)
        res = {}
        house = get_object_or_404(house_models.House, pk=kwargs['house_pk'])
        if serializer.is_valid():
            r = serializer.save(house=house, user=self.request.user)
            res['response'] = True
        else:
            res['response'] = False
            res['errors'] = serializer.errors

        return Response(res, status=status.HTTP_200_OK)


class CityViewSet(ModelViewSet):
    queryset = house_models.City.objects.all()
    serializer_class = home_serializers.CitySerializer
    pagination_class = None


class RuleViewSet(ModelViewSet):
    queryset = house_models.Rule.objects.all()
    serializer_class = home_serializers.RuleSerializer
    pagination_class = None
