import json
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from house import serializers as home_serializers
from house import models as house_models
from url_filter.integrations.drf import DjangoFilterBackend
from datetime import datetime
from rest_framework.decorators import action
from reservation.models import Reservation
from reservation.serializers import ReservationDatesSerializer
from .permissions import IsOwnerOrReadOnly, IsGuest, IsHost, IsGuestLived
from rest_framework import permissions
from rest_framework import generics, mixins
from .helpers import get_names
from cities_light.models import City, Country, Region
from rest_framework.decorators import api_view
from django.db.models import Q


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
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class HouseSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'


class HouseViewSet(ModelViewSet):
    queryset = house_models.House.objects.filter(status=True)
    serializer_class = home_serializers.HouseDetailSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['address', 'name']
    filter_fields = ['floor', 'rooms', 'beds', 'guests',
                     'price', 'house_type', 'rating', 'city', 'user', 'verified']
    ordering_fields = ['rating', 'price']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    pagination_class = HouseSetPagination
    action_serializers = {
        'retrieve': home_serializers.HouseDetailSerializer,
        'list': home_serializers.HouseListSerializer,
        'update': home_serializers.HouseCreateSerializer,
        'create': home_serializers.HouseCreateSerializer
    }

    def get_queryset(self):
        dates = self.request.query_params.get('dates', None)
        accommodations = self.request.query_params.get('accommodations', None)
        queryset = house_models.House.objects.filter(status=True)
        check_in = self.request.query_params.get('check_in', None)
        check_out = self.request.query_params.get('check_out', None)
        if check_in and check_out:
            check_in = datetime.strptime(check_in, '%Y-%m-%d')
            check_out = datetime.strptime(check_out, '%Y-%m-%d')
            queryset = queryset.exclude(Q(
                reservations__check_in__lte=check_out) & Q(reservations__check_out__gte=check_in) | Q(blocked_dates__check_in__lte=check_out) & Q(blocked_dates__check_out__gte=check_in))
        if accommodations:
            accommodations = accommodations.split(',')
            queryset = queryset.filter(accommodations__id__in=accommodations)
        return queryset

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(HouseViewSet, self).get_serializer_class()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        res = {}
        instance.photos.all().delete()
        photos = self.request.data.getlist('photos')
        for name in photos:
            modified_data = get_names(instance.id, name)
            file_serializer = home_serializers.PhotoSerializer(
                data=modified_data)
            if file_serializer.is_valid(raise_exception=True):
                file_serializer.save()
        res['response'] = True
        res['message'] = 'Объявление было успешно изменено'
        return Response(res)

    def perform_update(self, serializer):
        serializer.save()

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
        house.status = True
        house.save()
        res = {'response': True, 'message': 'Статус объявления был успешно изменен'}
        return Response(res, status=status.HTTP_200_OK)

    @action(["post"], detail=True)
    def deactivate(self, request, *args, **kwargs):
        house = get_object_or_404(house_models.House, pk=kwargs['pk'])
        house.status = False
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
    permission_classes = (IsGuestLived,)

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

    def get_queryset(self):
        return City.objects.order_by('name')


class RegionViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = Region.objects.all()
    serializer_class = home_serializers.RegionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_fields = ('name', 'country')
    ordering_fields = ('name', )
    pagination_class = None

    def get_queryset(self):
        return Region.objects.order_by('name')


class CountryViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = Country.objects.all()
    serializer_class = home_serializers.CountrySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_fields = ('name', )
    ordering_fields = ('name', )
    pagination_class = None

    def get_queryset(self):
        return Country.objects.order_by('name')


class RuleViewSet(ModelViewSet):
    queryset = house_models.Rule.objects.all()
    serializer_class = home_serializers.RuleSerializer
    pagination_class = None


class FavouriteViewSet(ModelViewSet):
    queryset = house_models.Favourite.objects.all()
    serializer_class = home_serializers.HouseListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        favourites = house_models.Favourite.objects.filter(
            user=self.request.user.id).values_list('house', flat=True)
        return house_models.House.objects.filter(id__in=favourites)


@api_view(['POST'])
def favourites_create(request, pk):
    house = get_object_or_404(house_models.House, pk=pk)
    res = {}
    if house_models.Favourite.objects.filter(house=house.id,
                                             user=request.user).exists() == False:
        r = house_models.Favourite.objects.create(
            user=request.user, house=house)
        res['response'] = True
    else:
        res['response'] = False
    return Response(res, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def favourites_delete(request, pk):
    house = get_object_or_404(house_models.House, pk=pk)
    res = {}
    if house_models.Favourite.objects.filter(house=house.id).exists():
        house_models.Favourite.objects.filter(house=house.id).delete()
        res['response'] = True
    else:
        res['response'] = False
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
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
