from account.models import User
from django.shortcuts import get_object_or_404
from core.models import Message, Image
from rest_framework import serializers
from account.serializers import UserShortSerializer
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField, IntegerField


class MessageListSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    recipient = UserShortSerializer()
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        qs = Image.objects.filter(message=obj)
        if len(qs) == 0:
            return None
        images = ImageSerializer(qs, many=True).data
        return images

    class Meta:
        model = Message
        fields = ('id', 'user', 'recipient', 'body', 'images',
                  'created_at', 'updated_at')


class MessageSerializer(serializers.ModelSerializer):
    user = IntegerField(source='user.id', read_only=True)
    recipient = IntegerField(source='recipient.id')
    images = SerializerMethodField()

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            User, id=validated_data['recipient']['id'])
        msg = Message(recipient=recipient,
                      body=validated_data['body'], user=user)
        msg.save()
        return msg

    def get_images(self, obj):
        qs = Image.objects.filter(message=obj)
        if len(qs) == 0:
            return None
        images = ImageSerializer(qs, many=True).data
        return images

    class Meta:
        model = Message
        fields = ('id', 'user', 'recipient', 'body', 'images',
                  'created_at', 'updated_at')


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('message', 'image',)
