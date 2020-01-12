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
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework import generics, mixins


class HouseUserList(mixins.ListModelMixin,
                    generics.GenericAPIView):

    serializer_class = home_serializers.HouseListSerializer

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
    search_fields = ['address', ]
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

    def create(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        res = {}
        serializer.is_valid(raise_exception=True)
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
        serializer = self.get_serializer(data=request.data)
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
            house=house, accepted_house=True, status=0)
        serializer = self.get_serializer(queryset, many=True)
        rserializer = ReservationDatesSerializer(rqueryset, many=True)
        dates = serializer.data + rserializer.data
        return Response(dates)
