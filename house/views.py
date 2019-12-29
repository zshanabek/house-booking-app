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
from reservation.models import Reservation
from reservation.serializers import ReservationDatesSerializer


class HouseViewSet(ModelViewSet):
    queryset = house_models.House.objects.all()
    serializer_class = home_serializers.HouseDetailSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['address', ]
    filter_fields = ['floor', 'rooms', 'beds', 'guests',
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
        check_in = self.request.query_params.get('check_in', None)
        check_out = self.request.query_params.get('check_out', None)
        if check_in and check_out:
            check_in = datetime.strptime(check_in, '%Y-%m-%d')
            check_out = datetime.strptime(check_out, '%Y-%m-%d')
            queryset = queryset.filter(
                Q(blocked_dates__check_in__lte=check_in), Q(blocked_dates__check_out__lte=check_out))
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
            house_models.Photo.objects.create(image=photo, house_id=house.id)

        dserializer = home_serializers.BlockedDateIntervalSerializer(
            data=blocked_dates, many=True)
        dserializer.is_valid(raise_exception=True)
        dserializer.save(house=house)
        res['response'] = True
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        res = {}
        serializer = self.get_serializer(data=request.data, many=True)
        house = get_object_or_404(house_models.House, pk=kwargs['house_pk'])
        serializer.is_valid(raise_exception=True)
        serializer.save(house=house)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        house = get_object_or_404(house_models.House, pk=kwargs['house_pk'])
        queryset = house_models.BlockedDateInterval.objects.filter(house=house)
        rqueryset = Reservation.objects.filter(
            house=house, accepted_house=True)
        serializer = self.get_serializer(queryset, many=True)
        rserializer = ReservationDatesSerializer(rqueryset, many=True)
        dates = serializer.data + rserializer.data
        return Response(dates)
