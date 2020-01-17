from account.models import User
from django.shortcuts import get_object_or_404
from core.models import Message, Image
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField


class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.email', read_only=True)
    recipient = CharField(source='recipient.email')
    images = SerializerMethodField()

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            User, email=validated_data['recipient']['email'])
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


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'userpic')


class ImageSerializer(ModelSerializer):

    class Meta:
        model = Image
        fields = ('message', 'image',)
