from rest_framework import serializers
from house import models as house_models
from account.serializers import UserSerializer
from account.models import User


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
        fields = ('id', 'nearbuilding', 'house',)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.City
        fields = ('id', 'name',)


class HouseSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    houseaccoms = serializers.SerializerMethodField()

    user = UserSerializer(read_only=True) 

    city = CitySerializer(read_only=True) 
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=house_models.City.objects.all(), source='city', write_only=True)
    
    def get_photos(self, obj):
        return obj.photos.values_list('image', flat=True)

    def get_houseaccoms(self, obj):
        return obj.houseaccoms.values_list('accom', flat=True)

    class Meta:
        model = house_models.House
        fields = (
            'id', 'user', 'city_id', 'rooms', 'floor',
            'address', 'longitude', 'latitude', 'city',
            'house_type', 'price', 'status', 'status',
            'photos', 'houseaccoms'
        )
        


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    house = serializers.ReadOnlyField(source='house.id')

    class Meta:
        model = house_models.Review
        fields = ('id', 'user', 'house', 'body', 'rating', 'created_at')


class HouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.HouseType
        fields = ('id', 'name', 'description')
