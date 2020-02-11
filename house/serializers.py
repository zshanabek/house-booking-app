from rest_framework import serializers
from house import models as house_models
from account.serializers import UserShortSerializer
from account.models import User
from cities_light.models import City, Country, Region
from reservation.models import Reservation
import reservation.serializers as rserializers
from django.shortcuts import get_object_or_404


class ReviewSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    house = serializers.ReadOnlyField(source='house.id')

    class Meta:
        model = house_models.Review
        fields = ('id', 'user', 'house', 'body', 'stars', 'created_at')


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = house_models.Photo
        fields = ('house', 'image',)


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.Rule
        fields = ('id', 'name',)


class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.Accommodation
        fields = ('id', 'name',)


class NearBuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.NearBuilding
        fields = ('id', 'name',)


class HouseCoordinatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = house_models.House
        fields = ('id', 'name', 'longitude', 'latitude', 'city')


class HouseListSerializer(serializers.ModelSerializer):
    city = serializers.ReadOnlyField(source='city.name')
    house_type = serializers.ReadOnlyField(source='house_type.name')
    is_favourite = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    accommodations = AccommodationSerializer(many=True)

    def get_photos(self, obj):
        p_qs = house_models.Photo.objects.filter(house=obj)
        if len(p_qs) == 0:
            return None
        photos = PhotoSerializer(p_qs, many=True).data
        return photos

    def get_is_favourite(self, obj):
        if 'request' in self.context and self.context['request'].user.id is not None:
            return house_models.Favourite.objects.filter(user=self.context['request'].user, house=obj).exists()
        return False

    class Meta:
        model = house_models.House
        fields = (
            'id', 'name', 'city', 'longitude', 'latitude', 'house_type', 'price', 'status', 'beds', 'rooms', 'rating', 'is_favourite', 'photos', 'accommodations')


class HouseDetailSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    city = serializers.ReadOnlyField(source='city.name')
    house_type = serializers.ReadOnlyField(source='house_type.name')
    is_favourite = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    rules = RuleSerializer(many=True)
    accommodations = AccommodationSerializer(many=True)
    near_buildings = NearBuildingSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    recommendations = serializers.SerializerMethodField()
    reservations = serializers.SerializerMethodField()

    def get_is_favourite(self, obj):
        if self.context['request'].user.id is not None:
            return house_models.Favourite.objects.filter(user=self.context['request'].user, house=obj).exists()
        return False

    def get_photos(self, obj):
        p_qs = house_models.Photo.objects.filter(house=obj)
        if len(p_qs) == 0:
            return None
        photos = PhotoSerializer(p_qs, many=True).data
        return photos

    def get_reviews(self, obj):
        qs = house_models.Review.objects.filter(house=obj)
        reviews = ReviewSerializer(qs, many=True).data[:2]
        return reviews

    def get_recommendations(self, obj):
        qs = house_models.House.objects.filter(city=obj.city)
        houses = HouseListSerializer(qs, many=True).data[:2]
        return houses

    def get_reservations(self, obj):
        qs = Reservation.objects.filter(house=obj)
        reservs = rserializers.ReservationDatesSerializer(qs, many=True).data
        return reservs

    class Meta:
        model = house_models.House
        fields = (
            'id', 'name', 'description', 'rooms', 'floor',
            'address', 'longitude', 'latitude', 'house_type', 'price',
            'status', 'beds', 'guests', 'rating', 'city', 'is_favourite', 'discount7days', 'discount30days', 'available', 'photos', 'accommodations', 'near_buildings', 'rules', 'user', 'reviews', 'recommendations', 'reservations'
        )


class BlockedDateIntervalSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True, source='house.user')

    class Meta:
        model = house_models.BlockedDateInterval
        fields = ('check_in', 'check_out', 'user')
        read_only_fields = ('user',)


class HouseCreateSerializer(serializers.ModelSerializer):
    house_type_id = serializers.PrimaryKeyRelatedField(
        queryset=house_models.HouseType.objects.all(), source='house_type', write_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), source='city', write_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), source='country', write_only=True)
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(), source='region', write_only=True)
    rules = serializers.ListField(
        child=serializers.CharField(allow_blank=True), write_only=True, required=False
    )
    accommodations = serializers.ListField(
        child=serializers.CharField(allow_blank=True), write_only=True, required=False
    )
    near_buildings = serializers.ListField(
        child=serializers.CharField(allow_blank=True), write_only=True, required=False
    )
    blocked_dates = BlockedDateIntervalSerializer(many=True, required=False)

    def create(self, validated_data):
        rules_data = []
        accommodations_data = []
        near_buildings_data = []
        dates_data = []
        if 'rules' in validated_data:
            rules_data = validated_data.pop('rules')
        if 'accommodations' in validated_data:
            accommodations_data = validated_data.pop('accommodations')
        if 'near_buildings' in validated_data:
            near_buildings_data = validated_data.pop('near_buildings')
        if 'blocked_dates' in validated_data:
            dates_data = validated_data.pop('blocked_dates')
        house = house_models.House.objects.create(**validated_data)
        for date in dates_data:
            house_models.BlockedDateInterval.objects.create(
                house=house, **date)
        for rule in rules_data:
            try:
                obj = get_object_or_404(house_models.Rule, name=rule)
            except:
                obj = house_models.Rule.objects.create(name=rule)
            house.rules.add(obj)
        for acco in accommodations_data:
            try:
                obj = get_object_or_404(house_models.Accommodation, name=acco)
            except:
                obj = house_models.Accommodation.objects.create(name=acco)
            house.accommodations.add(obj)
        for near in near_buildings_data:
            try:
                obj = get_object_or_404(house_models.NearBuilding, name=near)
            except:
                obj = house_models.NearBuilding.objects.create(name=near)
            house.near_buildings.add(obj)
        return house

    def update(self, instance, validated_data):
        rules = validated_data.pop('rules', None)
        accoms = validated_data.pop('accommodations', None)
        nears = validated_data.pop('near_buildings', None)
        instance = super().update(instance, validated_data)
        if rules is not None:
            instance.rules.clear()
            for rule in rules:
                try:
                    obj = get_object_or_404(house_models.Rule, name=rule)
                except:
                    obj = house_models.Rule.objects.create(name=rule)
                instance.rules.add(obj)
        if accoms is not None:
            instance.accommodations.clear()
            for acco in accoms:
                try:
                    obj = get_object_or_404(
                        house_models.Accommodation, name=acco)
                except:
                    obj = house_models.Accommodation.objects.create(name=acco)
                instance.accommodations.add(obj)
        if nears is not None:
            instance.nears.clear()
            for near in nears:
                try:
                    obj = get_object_or_404(
                        house_models.NearBuilding, name=near)
                except:
                    obj = house_models.NearBuilding.objects.create(name=near)
                instance.nears.add(obj)
        instance.save()
        return instance

    class Meta:
        model = house_models.House
        fields = (
            'id', 'name', 'description', 'city_id', 'region_id', 'country_id', 'rooms', 'floor',
            'address', 'longitude', 'latitude', 'house_type_id', 'price',
            'beds', 'guests', 'discount7days', 'discount30days', 'rules', 'accommodations', 'near_buildings', 'blocked_dates'
        )


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class HouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.HouseType
        fields = ('id', 'name')


class FavouriteSerializer(serializers.ModelSerializer):
    house = HouseListSerializer(read_only=True)

    class Meta:
        model = house_models.Favourite
        fields = ('house',)
