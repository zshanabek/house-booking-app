from rest_framework import serializers
from house import models as house_models


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = house_models.Photo
        fields = ('image',)


class AccommodationHouseSerialzer(serializers.ModelSerializer):
    class Meta:
        model = house_models.AccommodationHouse
        fields = ('accom',)


class MySerialzer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    houseaccoms = serializers.SerializerMethodField()

    def get_photos(self, obj):
        return obj.photos.values_list('image', flat=True)

    def get_houseaccoms(self, obj):
        return obj.houseaccoms.values_list('accom', flat=True)

    class Meta:
        model = house_models.House
        fields = (
            'id', 'user', 'rooms', 'floor',
            'address', 'longitude', 'latitude', 'city',
            'house_type', 'price', 'status', 'status',
            'photos', 'houseaccoms'
        )
