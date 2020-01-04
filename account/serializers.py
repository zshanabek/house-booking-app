from rest_framework import serializers
from utils.sms import SMS
from .models import *
from django.contrib.auth import authenticate
from .models import *


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'userpic', 'email', 'is_active')

