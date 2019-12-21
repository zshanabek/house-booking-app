from rest_framework import serializers
from .models import Reservation
from account.serializers import UserShortSerializer
from account.models import User
from house.serializers import HouseListSerializer

class ReservationSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    house = HouseListSerializer()

    class Meta:
        model = Reservation
        fields = ('id', 'check_in', 'check_out',
                  'guests', 'status', 'created_at', 'accepted_house', 'user', 'house')
        read_only_fields = ['status', 'accepted_house']
