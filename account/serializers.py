from rest_framework import serializers
from utils.sms import SMS
from .models import *
from django.contrib.auth import authenticate
from .models import *
from djoser.serializers import TokenSerializer


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'userpic', 'email')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'gender', 'phone',
                  'first_name', 'last_name', 'birth_day', 'userpic', 'is_active', 'user_type')


class LoginTokenSerializer(TokenSerializer):
    user = UserSerializer()

    class Meta(TokenSerializer.Meta):
        fields = ('auth_token', 'user')
