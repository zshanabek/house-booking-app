from rest_framework import serializers
from .models import Reservation
from house.models import House
from account.serializers import UserShortSerializer
from account.models import User
from house.serializers import HouseListSerializer
from datetime import datetime
from .tasks import send_email_task, set_reservation_as_inactive


class ReservationDatesSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    income = serializers.ReadOnlyField()

    class Meta:
        model = Reservation
        fields = ('check_in', 'check_out', 'user', 'income')


class ReservationSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    house = HouseListSerializer(read_only=True)
    house_id = serializers.PrimaryKeyRelatedField(
        queryset=House.objects.all(), source='house', write_only=True)
    owner = UserShortSerializer(read_only=True, source='house.user')

    class Meta:
        model = Reservation
        fields = ('id', 'check_in', 'check_out', 'days', 'guests', 'status', 'created_at',
                  'accepted_house', 'user', 'house_id', 'house', 'owner', 'message')
        read_only_fields = ('message', 'status', 'days',)
