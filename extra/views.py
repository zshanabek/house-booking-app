from django.shortcuts import render
from .models import Feedback
from .serializers import FeedbackSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
