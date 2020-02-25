from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from .models import *
from djoser.serializers import TokenSerializer


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'userpic', 'email')
