from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from .models import *


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, object):
        return object.first_name + " " + object.last_name

    class Meta:
        model = User
        fields = ('id', 'email', 'gender',
                  'phone', 'name', 'birth_day')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'gender',
                  'phone', 'first_name', 'last_name', 'birth_day', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if len(validated_data['password']) < 8:
            raise serializers.ValidationError(
                'Password must have at least 8 chars.')
        user = User.objects.create_user(validated_data['email'], phone=validated_data['phone'], first_name=validated_data[
            'first_name'], last_name=validated_data['last_name'], gender=validated_data['gender'],
            birth_day=validated_data['birth_day'], password=validated_data['password'])
        return user


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
