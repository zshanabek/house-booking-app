from account.models import User
from .models import (ChatSession, ChatSessionMessage, deserialize_user)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from notifications.signals import notify
from django.db.models import Q


class ChatSessionView(APIView):
    """Manage Chat sessions."""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        chat_sessions = ChatSession.objects.filter(
            Q(user1=user) | Q(user2=user))

        sessions = [session.to_json() for session in chat_sessions]
        return Response(sessions)

    def post(self, request, *args, **kwargs):
        """create a new chat session."""
        email = request.data['email']
        user1 = request.user
        user2 = User.objects.get(email=email)

        chat_session = ChatSession.objects.create(user1=user1, user2=user2)

        return Response({
            'status': 'Success', 'uri': chat_session.uri,
            'message': 'New chat session created'
        })


class ChatSessionMessageView(APIView):
    """Create/Get Chat session messages."""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """return all messages in a chat session."""
        uri = kwargs['uri']

        chat_session = ChatSession.objects.get(uri=uri)
        messages = [chat_session_message.to_json()
                    for chat_session_message in chat_session.messages.all()]

        return Response({
            'id': chat_session.id, 'uri': chat_session.uri,
            'messages': messages
        })

    def post(self, request, *args, **kwargs):
        """create a new message in a chat session."""
        uri = kwargs['uri']
        message = request.data['message']

        user = request.user
        chat_session = ChatSession.objects.get(uri=uri)

        chat_session_message = ChatSessionMessage.objects.create(
            user=user, chat_session=chat_session, message=message
        )
        notif_args = {
            'source': user,
            'source_display_name': user.full_name(),
            'category': 'chat',
            'action': 'Sent',
            'obj': chat_session_message.id,
            'short_description': 'You have a new message',
            'silent': True,
            'extra_data': {
                'uri': chat_session.uri,
                'message': message,
                'user': deserialize_user(user),
            }
        }
        notify.send(
            sender=self.__class__, **notif_args, channels=['websocket']
        )

        return Response({
            'status': 'Success', 'uri': chat_session.uri, 'message': message,
            'user': deserialize_user(user)
        })
