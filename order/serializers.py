from rest_framework import serializers
from .models import Order
from reservation.models import Reservation


class OrderSerializer(serializers.ModelSerializer):
    reservation_id = serializers.PrimaryKeyRelatedField(
        queryset=Reservation.objects.all(), source='reservation')

    class Meta:
        model = Order
        fields = ('id', 'amount', 'is_paid', 'payment_id', 'reservation_id')
        read_only_fields = ('id', 'amount', 'is_paid', 'payment_id')
