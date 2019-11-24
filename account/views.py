from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from knox.models import AuthToken
from .serializers import *

from .models import *


# Register


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = serializer.save()
            _, token = AuthToken.objects.create(user)
            user = UserSerializer(
                user, context=self.get_serializer_context()).data
            user['name'] = user.pop('first_name') + " " + user.pop("last_name")
            response = {
                'response': True,
                'token': token,
                'user': user
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            errors = serializer.errors
            x = next(iter(errors))
            error = errors[x][0]
            data = {'response': False,
                    'error_message': error, }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


# Login
class LoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = serializer.validated_data
            _, token = AuthToken.objects.create(user)
            user = UserSerializer(
                user, context=self.get_serializer_context()).data
            user['name'] = user.pop('first_name') + " " + user.pop("last_name")
            response = {
                'response': True,
                'token': token,
                'user': user
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            data = {'response': False,
                    'error_message': 'Invalid login or password'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UserView(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = UserSerializer

    def get_object(self):
        print(self.request.user)
        return self.request.user
