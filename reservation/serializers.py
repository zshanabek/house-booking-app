from rest_framework import serializers
from house import models as house_models
from account.serializers import UserShortSerializer
from account.models import User

class ReservationSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    house = serializers.ReadOnlyField(source='house.id')

    class Meta:
        model = house_models.Review
        fields = ('id', 'user', 'house', 'check_in', 'check_out', 'guests', 'status', 'created_at', 'accepted_house')
