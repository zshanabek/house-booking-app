from rest_framework import serializers
from .models import Reservation
from house.models import House, Photo
from account.serializers import UserShortSerializer
from account.models import User
from datetime import datetime
from .tasks import set_reservation_as_inactive


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ('house', 'image',)


class HouseShortSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    def get_photos(self, obj):
        p_qs = Photo.objects.filter(house=obj)
        if len(p_qs) == 0:
            return None
        photos = PhotoSerializer(p_qs, many=True).data
        return photos

    class Meta:
        model = House
        fields = ('id', 'name', 'photos')


class ReservationDatesSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    income = serializers.ReadOnlyField()

    class Meta:
        model = Reservation
        fields = ('check_in', 'check_out', 'user', 'income')


class ReservationSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    house = HouseShortSerializer(read_only=True)
    house_id = serializers.PrimaryKeyRelatedField(
        queryset=House.objects.all(), source='house', write_only=True)
    owner = UserShortSerializer(read_only=True, source='house.user')
    status_name = serializers.CharField(
        source='get_status_display', read_only=True)

    class Meta:
        model = Reservation
        fields = ('id', 'check_in', 'check_out', 'days', 'guests', 'status',
                  'status_name', 'created_at', 'user', 'house', 'house_id', 'owner', 'message')
        read_only_fields = ('message', 'status', 'days', 'status_name')
