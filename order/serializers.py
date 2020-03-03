from rest_framework import serializers
from .models import Order
from reservation.models import Reservation
from account.serializers import UserShortSerializer


class OrderSerializer(serializers.ModelSerializer):
    reservation_id = serializers.PrimaryKeyRelatedField(
        queryset=Reservation.objects.all(), source='reservation')
    user = UserShortSerializer(read_only=True, source='reservation.house.user')

    class Meta:
        model = Order
        fields = ('id', 'amount', 'is_paid',
                  'payment_id', 'reservation_id', 'user')
        read_only_fields = ('id', 'amount', 'is_paid', 'payment_id', 'user')
