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
from rest_framework.decorators import action


class HouseViewSet(ModelViewSet):
    queryset = house_models.House.objects.all()
    serializer_class = home_serializers.HouseDetailSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['address', ]
    filter_fields = ['floor', 'rooms', 'beds',
                     'price', 'house_type', 'rating', 'city', 'user']
    ordering_fields = ['rating', 'price']

    action_serializers = {
        'retrieve': home_serializers.HouseDetailSerializer,
        'list': home_serializers.HouseListSerializer,
        'create': home_serializers.HouseCreateSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(HouseViewSet, self).get_serializer_class()

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
                Q(blocked_dates__date_start__lte=date_start), Q(blocked_dates__date_end__lte=date_end))
        if rules:
            rules = rules.split(',')
            queryset = queryset.filter(rules__id__in=rules)
        return queryset

    def create(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        res = {}

        serializer.is_valid(raise_exception=True)
        if (self.request.user.user_type != 1):
            res['response'] = False
            res['errors'] = 'Forbidden to create. Only hosts can create houses'
            return Response(res, status=status.HTTP_403_FORBIDDEN)

        house = serializer.save(user=self.request.user)
        photos = request.data.getlist('photos')
        blocked_dates = json.loads(request.data['blocked_dates'])

        for photo in photos:
            house_models.Photo.objects.create(
                image=photo, house_id=house.id
            )

        for d in blocked_dates:
            house_models.BlockedDateInterval.objects.create(
                house_id=house.id, date_start=d['date_start'],
                date_end=d['date_end']
            )
        res['response'] = True
        return Response(res, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def my(self, request, *args, **kwargs):
        queryset = house_models.House.objects.filter(user=request.user.id)
        serializer = home_serializers.HouseListSerializer(queryset, many=True)
        return Response(serializer.data)


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


class BlockedDateIntervalViewSet(ModelViewSet):
    queryset = house_models.BlockedDateInterval.objects.all()
    serializer_class = home_serializers.BlockedDateIntervalSerializer
    pagination_class = None

    def get_queryset(self):
        return house_models.BlockedDateInterval.objects.filter(house=self.kwargs['house_pk'])

    def create(self, request, *args, **kwargs):
        serializer = home_serializers.BlockedDateIntervalSerializer(
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
