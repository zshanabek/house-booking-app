from django.conf import settings
from rest_framework import serializers
from chat.models import Message
from account.models import User


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        many=False, slug_field='first_name', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(
        many=False, slug_field='first_name', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']
