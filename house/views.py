from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from house import serializers as home_serializers
from house import models as house_models
import json
from url_filter.integrations.drf import DjangoFilterBackend
from django.db.models import Q
from datetime import datetime


class HouseViewSet(ModelViewSet):
    queryset = house_models.House.objects.all()
    serializer_class = home_serializers.HouseSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ('address',)
    filter_fields = ['floor', 'rooms', 'beds',
                     'price', 'house_type', 'rating', 'city']
    ordering_fields = ['rating', 'price']

    def get_queryset(self):
        dates = self.request.query_params.get('dates', None)
        rules = self.request.query_params.get('rules', None)
        queryset = house_models.House.objects.all()
        date_start = self.request.query_params.get('date_start', None)
        date_end = self.request.query_params.get('date_end', None)
        if date_start and date_end:
            date_start = datetime.strptime(date_start, '%Y-%m-%d')
            date_end = datetime.strptime(date_end, '%Y-%m-%d')
            queryset = queryset.filter(
                Q(free_dates__date_start__lte=date_start), Q(free_dates__date_end__lte=date_end))
        if rules:
            rules = rules.split(',')
            queryset = queryset.filter(rules__id__in=rules)
        return queryset

    def create(self, request):
        serializer = home_serializers.HouseSerializer(data=request.data)
        res = {}
        if serializer.is_valid():
            house = serializer.save(user=self.request.user)
            photos = request.data.getlist('photos')
            free_dates = json.loads(request.data['free_dates'])

            for photo in photos:
                house_models.Photo.objects.create(
                    image=photo, house_id=house.id
                )

            for d in free_dates:
                house_models.FreeDateInterval.objects.create(
                    house_id=house.id, date_start=d['date_start'],
                    date_end=d['date_end']
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


class NearBuildingViewSet(ModelViewSet):
    queryset = house_models.NearBuilding.objects.all()
    serializer_class = home_serializers.NearBuildingSerializer
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
            summ = 0
            reviews = house.review_set
            for review in reviews.all():
                summ += review.stars
            house.rating = round(summ/reviews.count() * 2) / 2
            house.save()
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


class FavouriteViewSet(ModelViewSet):
    queryset = house_models.Favourite.objects.all()
    serializer_class = home_serializers.FavouriteSerializer
    pagination_class = None

    def get_queryset(self):
        return house_models.Favourite.objects.filter(user=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = home_serializers.FavouriteSerializer(data=request.data)
        house = get_object_or_404(house_models.House, pk=kwargs['pk'])
        res = {}
        if serializer.is_valid():
            if house_models.Favourite.objects.filter(house=house.id, user=self.request.user).exists() == False:
                r = serializer.save(user=self.request.user, house=house)
            res['response'] = True
        else:
            res['response'] = False
            res['errors'] = serializer.errors
        return Response(res, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        serializer = home_serializers.FavouriteSerializer(data=request.data)
        house = get_object_or_404(house_models.House, pk=kwargs['pk'])
        res = {}
        if house_models.Favourite.objects.filter(house=house.id).exists():
            house_models.Favourite.objects.filter(house=house.id).delete()
            res['response'] = True
        else:
            res['response'] = False
            res['errors'] = serializer.errors
        return Response(res, status=status.HTTP_200_OK)


class FreeDateIntervalViewSet(ModelViewSet):
    queryset = house_models.FreeDateInterval.objects.all()
    serializer_class = home_serializers.FreeDateIntervalSerializer
    pagination_class = None

    def get_queryset(self):
        return house_models.FreeDateInterval.objects.filter(house=self.kwargs['house_pk'])

    def create(self, request, *args, **kwargs):
        serializer = home_serializers.FreeDateIntervalSerializer(
            data=request.data)
        res = {}
        house = get_object_or_404(house_models.House, pk=kwargs['house_pk'])
        if serializer.is_valid():
            r = serializer.save(house=house)
            res['response'] = True
        else:
            res['response'] = False
            res['errors'] = serializer.errors
        return Response(res, status=status.HTTP_200_OK)
