from rest_framework import serializers
from .models import *


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ['image']


class AccommodationHouseSerialzer(serializers.ModelSerializer):
    class Meta:
        model = AccommodationHouse
        fields = ['accom']


class MySerialzer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    houseaccoms = serializers.SerializerMethodField()

    def get_photos(self, obj):
        return obj.photos.values_list('image', flat=True)

    def get_houseaccoms(self, obj):
        return obj.houseaccoms.values_list('accom', flat=True)

    class Meta:
        model = House
        fields = ['id', 'user', 'rooms', 'floor',
                  'address', 'longitude', 'latitude', 'city',
                  'house_type', 'price', 'status', 'status',  'photos', 'houseaccoms', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
