import json
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from house import serializers as home_serializers
from house import models as house_models
from url_filter.integrations.drf import DjangoFilterBackend
from django.db.models import Q
from datetime import datetime
from rest_framework.decorators import action
from reservation.models import Reservation
from reservation.serializers import ReservationDatesSerializer
from .permissions import IsOwnerOrReadOnly, IsGuest, IsHost
from rest_framework import permissions
from rest_framework import generics, mixins
from .helpers import get_names
from cities_light.models import City, Country, Region


class HouseUserList(mixins.ListModelMixin,
                    generics.GenericAPIView):

    serializer_class = home_serializers.HouseListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        qs = house_models.House.objects.filter(user=self.request.user.id)
        return qs

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class HouseCoordinatesList(mixins.ListModelMixin,
                           generics.GenericAPIView):
    queryset = house_models.House.objects.all()
    serializer_class = home_serializers.HouseCoordinatesSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_fields = ['city', ]
    search_fields = ['address', ]
    ordering_fields = ['rating', 'price']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class HouseViewSet(ModelViewSet):
    queryset = house_models.House.objects.all()
    serializer_class = home_serializers.HouseDetailSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['address', 'name']
    filter_fields = ['floor', 'rooms', 'beds', 'guests',
                     'price', 'house_type', 'rating', 'city', 'user', 'verified']
    ordering_fields = ['rating', 'price']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
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
        accommodations = self.request.query_params.get('accommodations', None)
        queryset = house_models.House.objects.all()
        check_in = self.request.query_params.get('check_in', None)
        check_out = self.request.query_params.get('check_out', None)
        if check_in and check_out:
            check_in = datetime.strptime(check_in, '%Y-%m-%d')
            check_out = datetime.strptime(check_out, '%Y-%m-%d')
            queryset = queryset.filter(
                Q(blocked_dates__check_in__lte=check_in), Q(blocked_dates__check_out__lte=check_out))
        if accommodations:
            accommodations = accommodations.split(',')
            queryset = queryset.filter(accommodations__id__in=accommodations)
        return queryset

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        house = serializer.save(user=self.request.user)
        if 'blocked_dates' in self.request.data:
            blocked_dates = json.loads(self.request.data['blocked_dates'])
            dserializer = home_serializers.BlockedDateIntervalSerializer(
                data=blocked_dates, many=True)
            dserializer.is_valid(raise_exception=True)
            dserializer.save(house=house)
        photos = self.request.data.getlist('photos')
        for name in photos:
            modified_data = get_names(house.id, name)
            file_serializer = home_serializers.PhotoSerializer(
                data=modified_data)
            if file_serializer.is_valid(raise_exception=True):
                file_serializer.save()

    @action(["post"], detail=True)
    def activate(self, request, *args, **kwargs):
        house = get_object_or_404(house_models.House, pk=kwargs['pk'])
        house.status = 1
        house.save()
        res = {'response': True, 'message': 'Статус объявления был успешно изменен'}
        return Response(res, status=status.HTTP_200_OK)

    @action(["post"], detail=True)
    def deactivate(self, request, *args, **kwargs):
        house = get_object_or_404(house_models.House, pk=kwargs['pk'])
        house.status = 0
        house.save()
        res = {'response': True, 'message': 'Статус объявления был успешно изменен'}
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
            reviews = house.reviews
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
    http_method_names = ['get']
    queryset = City.objects.all()
    serializer_class = home_serializers.CitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_fields = ('name', 'region')
    ordering_fields = ('name', )
    pagination_class = None


class RegionViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = Region.objects.all()
    serializer_class = home_serializers.RegionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_fields = ('name', 'country')
    ordering_fields = ('name', )
    pagination_class = None


class CountryViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = Country.objects.all()
    serializer_class = home_serializers.CountrySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_fields = ('name', )
    ordering_fields = ('name', )
    pagination_class = None


class RuleViewSet(ModelViewSet):
    queryset = house_models.Rule.objects.all()
    serializer_class = home_serializers.RuleSerializer
    pagination_class = None


class FavouriteViewSet(ModelViewSet):
    queryset = house_models.Favourite.objects.all()
    serializer_class = home_serializers.FavouriteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return house_models.Favourite.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        house = get_object_or_404(house_models.House, pk=self.kwargs['pk'])
        res = {}
        if serializer.is_valid():
            if house_models.Favourite.objects.filter(house=house.id,
                                                     user=self.request.user).exists() == False:
                r = serializer.save(user=self.request.user, house=house)
            res['response'] = True
        else:
            res['response'] = False
            res['errors'] = serializer.errors
        return Response(res, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        serializer = home_serializers.FavouriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        return house_models.BlockedDateInterval.objects.filter(house=self.kwargs['house_pk'])

    def create(self, request, *args, **kwargs):
        res = {}
        house = get_object_or_404(house_models.House, pk=kwargs['house_pk'])
        if house.user != request.user:
            res['response'] = False
            res['errors'] = "Only ad owner can create blocked dates"
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(house=house)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        house = get_object_or_404(house_models.House, pk=kwargs['house_pk'])
        queryset = house_models.BlockedDateInterval.objects.filter(house=house)
        rqueryset = Reservation.objects.filter(
            house=house, accepted_house=True, status=0)
        serializer = self.get_serializer(queryset, many=True)
        rserializer = ReservationDatesSerializer(rqueryset, many=True)
        dates = serializer.data + rserializer.data
        return Response(dates)
