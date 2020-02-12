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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'gender', 'phone',
                  'first_name', 'last_name', 'birth_day', 'userpic', 'is_active', 'is_phone_confirmed', 'user_type')


class LoginTokenSerializer(TokenSerializer):
    user = UserSerializer()

    class Meta(TokenSerializer.Meta):
        fields = ('auth_token', 'user')


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        raise serializers.ValidationError('Incorrect Credentials')
