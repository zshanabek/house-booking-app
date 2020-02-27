from rest_framework import serializers
from .models import Feedback
from account.serializers import UserShortSerializer
from account.models import User


class FeedbackSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ('id', 'message', 'created_at', 'updated_at', 'user')
        read_only_fields = ('id', 'created_at', 'updated_at')
