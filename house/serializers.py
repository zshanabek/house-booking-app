from rest_framework import serializers
from house import models as house_models
from account.serializers import UserShortSerializer
from account.models import User


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = house_models.Photo
        fields = ('image',)


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


class HouseListSerializer(serializers.ModelSerializer):
    city = serializers.ReadOnlyField(source='city.name')
    house_type = serializers.ReadOnlyField(source='house_type.name')
    is_favourite = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()

    def get_photos(self, obj):
        p_qs = house_models.Photo.objects.filter(house=obj)
        if len(p_qs) == 0:
            return None
        photos = PhotoSerializer(p_qs, many=True).data
        return photos

    def get_is_favourite(self, obj):
        if self.context['request'].user.id is not None:
            return house_models.Favourite.objects.filter(user=self.context['request'].user, house=obj).exists()
        return False

    class Meta:
        model = house_models.House
        fields = (
            'id', 'name', 'city', 'longitude', 'latitude', 'house_type', 'price', 'status', 'beds', 'rating', 'is_favourite', 'photos'
        )


class HouseDetailSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    city = serializers.ReadOnlyField(source='city.name')
    house_type = serializers.ReadOnlyField(source='house_type.name')
    is_favourite = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    rules = RuleSerializer(many=True)
    accommodations = AccommodationSerializer(many=True)
    near_buildings = NearBuildingSerializer(many=True)

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

    class Meta:
        model = house_models.House
        fields = (
            'id', 'name', 'description', 'rooms', 'floor',
            'address', 'longitude', 'latitude', 'house_type', 'price',
            'status', 'beds', 'guests', 'rating', 'city', 'is_favourite', 'photos',
            'accommodations', 'near_buildings', 'rules', 'user'
        )


class HouseCreateSerializer(serializers.ModelSerializer):
    house_type_id = serializers.PrimaryKeyRelatedField(
        queryset=house_models.HouseType.objects.all(), source='house_type', write_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=house_models.City.objects.all(), source='city', write_only=True)
    rules = serializers.PrimaryKeyRelatedField(
        many=True, queryset=house_models.Rule.objects.all())
    accommodations = serializers.PrimaryKeyRelatedField(
        many=True, queryset=house_models.Accommodation.objects.all())
    near_buildings = serializers.PrimaryKeyRelatedField(
        many=True, queryset=house_models.NearBuilding.objects.all())

    class Meta:
        model = house_models.House
        fields = (
            'id', 'name', 'description', 'city_id', 'rooms', 'floor',
            'address', 'longitude', 'latitude', 'house_type_id', 'price',
            'beds', 'guests', 'accommodations', 'near_buildings', 'rules'
        )


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.City
        fields = ('id', 'name',)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    house = serializers.ReadOnlyField(source='house.id')

    class Meta:
        model = house_models.Review
        fields = ('id', 'user', 'house', 'body', 'stars', 'created_at')


class HouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.HouseType
        fields = ('id', 'name')


class FavouriteSerializer(serializers.ModelSerializer):
    house = HouseListSerializer(read_only=True)

    class Meta:
        model = house_models.Favourite
        fields = ('house',)


class BlockedDateIntervalSerializer(serializers.ModelSerializer):

    class Meta:
        model = house_models.BlockedDateInterval
        fields = ('check_in', 'check_out')
