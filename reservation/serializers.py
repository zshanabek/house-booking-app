from rest_framework import serializers
from .models import Reservation
from house.models import House
from account.serializers import UserShortSerializer
from account.models import User
from house.serializers import HouseListSerializer


class ReservationDatesSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ('check_in', 'check_out', 'user')


class ReservationSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    house = HouseListSerializer(read_only=True)
    house_id = serializers.PrimaryKeyRelatedField(
        queryset=House.objects.all(), source='house', write_only=True)
    owner = UserShortSerializer(read_only=True, source='house.user')
    class Meta:
        model = Reservation
        fields = ('id', 'check_in', 'check_out',
                  'guests', 'status', 'created_at', 'accepted_house', 'user', 'house_id', 'house', 'owner')
        read_only_fields = ['status']
