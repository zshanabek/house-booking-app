from django.db.models import Q
from django.shortcuts import get_object_or_404
from account.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication
from akv import settings
from core.serializers import MessageSerializer, MessageListSerializer, ImageSerializer
from core.models import Message, Image
from rest_framework import permissions
from account.serializers import UserShortSerializer
from slugify import slugify
import re
from rest_framework import status


def modify_data(message, image):
    l = {'message': message, 'image': image}
    return l


class MessagePagination(PageNumberPagination):
    page_size = settings.MESSAGES_TO_LOAD


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageListSerializer
    pagination_class = MessagePagination
    permission_classes = (permissions.IsAuthenticated,)

    action_serializers = {
        'retrieve': MessageListSerializer,
        'list': MessageListSerializer,
        'create': MessageSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(MessageViewSet, self).get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipient = int(self.request.data['recipient'])
        res = {}
        data = self.request.data['body']
        if recipient == self.request.user.id:
            res['response'] = False
            res['errors'] = "User can't send message to himself"
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', data)
        phones = re.findall(
            r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', data)
        if len(emails) or len(phones) > 0:
            res['response'] = False
            res['errors'] = "User can't send message with email or phone"
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        message = serializer.save()
        images = self.request.data.getlist('images')
        for image in images:
            names = image.name.split('.')
            image.name = slugify(names[0]) + '.' + names[-1]
            modified_data = modify_data(message.id, image)
            file_serializer = ImageSerializer(data=modified_data)
            if file_serializer.is_valid(raise_exception=True):
                file_serializer.save()
        message.notify_ws_clients()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(Q(recipient=request.user) |
                                             Q(user=request.user))
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset = self.queryset.filter(
                Q(recipient=request.user, user__id=target) |
                Q(recipient__id=target, user=request.user))
        return super(MessageViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(Q(recipient=request.user) |
                                 Q(user=request.user),
                                 Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)
        return Response(serializer.data)


class ChatModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserShortSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        messages = Message.objects.filter(Q(recipient=request.user) | Q(
            user=request.user))
        user_ids = messages.values_list('user_id', flat=True)
        recipient_ids = messages.values_list('recipient_id', flat=True)
        ids = list(user_ids) + list(recipient_ids)
        ids = list(set(ids))
        if request.user.id in ids:
            ids.remove(request.user.id)
        self.queryset = self.queryset.filter(id__in=ids)
        return super(ChatModelViewSet, self).list(request, *args, **kwargs)
