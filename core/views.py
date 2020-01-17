from django.db.models import Q
from django.shortcuts import get_object_or_404
from account.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication
from akv import settings
from core.serializers import MessageModelSerializer, UserModelSerializer, ImageSerializer
from core.models import Message, Image
from rest_framework import permissions


def modify_data(message, image):
    l = {'message': message, 'image': image}
    return l


class MessagePagination(PageNumberPagination):
    page_size = settings.MESSAGES_TO_LOAD


class MessageModelViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageModelSerializer
    pagination_class = MessagePagination
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        recipient = self.request.data['recipient']
        res = {}
        if recipient == self.request.user.email:
            res['response'] = False
            res['errors'] = "User can't send message to himself"
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        images = dict((self.request.data).lists())['images']
        for name in images:
            modified_data = modify_data(message.id, name)
            file_serializer = ImageSerializer(data=modified_data)
            if file_serializer.is_valid(raise_exception=True):
                file_serializer.save()

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(Q(recipient=request.user) |
                                             Q(user=request.user))
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset = self.queryset.filter(
                Q(recipient=request.user, user__email=target) |
                Q(recipient__email=target, user=request.user))
        return super(MessageModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(Q(recipient=request.user) |
                                 Q(user=request.user),
                                 Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)
        return Response(serializer.data)


class ChatModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        messages = Message.objects.filter(Q(recipient=request.user) | Q(
            user=request.user))
        user_ids = messages.values_list('user_id', flat=True)
        recipient_ids = messages.values_list('recipient_id', flat=True)
        ids = list(user_ids) + list(recipient_ids)
        ids = list(set(ids))
        self.queryset = self.queryset.filter(id__in=ids)
        return super(ChatModelViewSet, self).list(request, *args, **kwargs)
