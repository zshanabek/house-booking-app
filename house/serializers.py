from rest_framework import serializers
from house import models as house_models
from account.serializers import UserShortSerializer
from account.models import User


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.City
        fields = ('id', 'name',)


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


class HouseSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    city = serializers.ReadOnlyField(source='city.name')
    house_type_id = serializers.PrimaryKeyRelatedField(
        queryset=house_models.HouseType.objects.all(), source='house_type', write_only=True)
    house_type = serializers.ReadOnlyField(source='house_type.name')
    rating = serializers.ReadOnlyField()
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=house_models.City.objects.all(), source='city', write_only=True)
    is_favourite = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    rules = serializers.PrimaryKeyRelatedField(
        many=True, queryset=house_models.Rule.objects.all())
    accommodations = serializers.PrimaryKeyRelatedField(
        many=True, queryset=house_models.Accommodation.objects.all())
    near_buildings = serializers.PrimaryKeyRelatedField(
        many=True, queryset=house_models.NearBuilding.objects.all())

    def get_is_favourite(self, obj):
        return house_models.Favourite.objects.filter(user=obj.user, house=obj).exists()

    def get_photos(self, obj):
        return obj.photos.values_list('image', flat=True)

    class Meta:
        model = house_models.House
        fields = (
            'id', 'name', 'description', 'city_id', 'rooms', 'floor',
            'address', 'longitude', 'latitude', 'house_type', 'house_type_id', 'price',
            'status', 'beds', 'guests', 'rating', 'city', 'is_favourite', 'photos',
            'accommodations', 'near_buildings', 'rules', 'user'
        )


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = house_models.Photo
        fields = ('image',)


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
    house = HouseSerializer(read_only=True)

    class Meta:
        model = house_models.Favourite
        fields = ('house',)


class FreeDateIntervalSerializer(serializers.ModelSerializer):

    class Meta:
        model = house_models.FreeDateInterval
        fields = ('date_start', 'date_end')
