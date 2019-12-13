from rest_framework import serializers
from house import models as house_models
from account.serializers import UserShortSerializer
from account.models import User


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.City
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
    photos = serializers.SerializerMethodField()
    house_accoms = serializers.SerializerMethodField()
    house_rules = serializers.SerializerMethodField()
    house_near_buildings = serializers.SerializerMethodField()

    def get_photos(self, obj):
        return obj.photos.values_list('image', flat=True)

    def get_house_accoms(self, obj):
        return obj.house_accoms.values_list('accom', flat=True)

    def get_house_rules(self, obj):
        return obj.house_rules.values_list('rule', flat=True)

    def get_house_near_buildings(self, obj):
        return obj.house_near_buildings.values_list('near_building', flat=True)

    class Meta:
        model = house_models.House
        fields = (
            'id', 'name', 'description', 'city_id', 'rooms', 'floor',
            'address', 'longitude', 'latitude', 'house_type', 'house_type_id', 'price',
            'status', 'beds', 'guests', 'rating', 'city', 'photos',
            'house_accoms', 'house_rules', 'house_near_buildings', 'user'
        )


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = house_models.Photo
        fields = ('image',)


class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.Accommodation
        fields = ('id', 'name',)


class AccommodationHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.AccommodationHouse
        fields = ('id', 'accom', 'house',)


class NearBuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.NearBuilding
        fields = ('id', 'name',)


class NearBuildingHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.NearBuildingHouse
        fields = ('id', 'near_building', 'house',)


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.Rule
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
    house = serializers.ReadOnlyField(source='house.id')
    house_id = serializers.PrimaryKeyRelatedField(
        queryset=house_models.House.objects.all(), source='house', write_only=True)

    class Meta:
        model = house_models.Review
        fields = ('id', 'house')

class FreeDateIntervalSerializer(serializers.ModelSerializer):

    class Meta:
        model = house_models.FreeDateInterval
        fields = ('date_start', 'date_end')
