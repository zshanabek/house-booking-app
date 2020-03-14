from account.models import User
from django.shortcuts import get_object_or_404
from core.models import Message, Image
from rest_framework import serializers
from account.serializers import UserShortSerializer
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField, IntegerField
from reservation.tasks import send_email_on_message_send


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
        body = ''
        if 'body' in validated_data:
            body = validated_data['body']
        else:
            body = None
        msg = Message(recipient=recipient,
                      body=body, user=user)
        send_email_on_message_send(msg)
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
