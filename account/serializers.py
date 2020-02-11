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
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        temp = data['email']
        if self.check_numbers(temp):
            try:
                obj = User.objects.get(phone=temp)
                data['email'] = obj.email
            except Exception:
                raise serializers.ValidationError('Incorrect Credentials')
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials')

    def check_numbers(self, data):
        counter = 0
        for d in data:
            if d == '@':
                return False
            if d.isdigit():
                counter += 1
        if counter == 11:
            return True
        return False
