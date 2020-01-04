from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .serializers import *
import datetime
from django.shortcuts import get_object_or_404
from .models import *
import pytz
utc = pytz.timezone('Asia/Almaty')


# Register
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        user = UserSerializer(
            user, context=self.get_serializer_context()).data
        response = {
            'response': True,
            'token': token.key,
            'user': user
        }
        return Response(response, status=status.HTTP_200_OK)


# Login and Logout
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)
        user = UserSerializer(
            user, context=self.get_serializer_context()).data
        response = {
            'response': True,
            'token': token.key,
            'user': user
        }
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserView(GenericAPIView, UpdateModelMixin, RetrieveModelMixin):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# Decorator to make the view csrf excempt.
@csrf_exempt
def user_list(request, pk=None):
    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all()
        serializer = UserSerializer(
            users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def code_view(request):
    phone = request.data.get('phone')
    if phone:
        user = User.objects.filter(phone__iexact=phone)
        if user.exists():
            sms = SMS(phone=phone)
            code = sms.generate_code()
            otp = OTP.objects.filter(phone__iexact=phone)
            if otp.exists():
                otp = otp.first()
                if otp.attempts > 0:
                    message, sms_status = sms.send_message(code)
                    if message['response']:
                        otp.code = code
                        otp.attempts -= 1
                        otp.save()
                        if otp.attempts == 0:
                            otp.ban_date = datetime.datetime.now() + datetime.timedelta(minutes=15)
                            otp.save()
                    return Response(message, status=sms_status)
                else:
                    if otp.ban_date < datetime.datetime.now().replace(tzinfo=utc):
                        message, sms_status = sms.send_message(code)
                        if message['response']:
                            otp.attempts = 3
                            otp.code = code
                            otp.ban_date = None
                            otp.save()
                        return Response(message, status=sms_status)

                    return Response(
                        {'response': False, 'message': otp.ban_date}
                    )
            else:
                message, sms_status = sms.send_message(code)
                if message['response']:
                    OTP.objects.create(phone=phone, code=code)
                return Response(message, status=sms_status)
        else:
            return Response(
                {'response': False, 'message': 'Такого пользователя нету'},
                status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(
            {'response': False, 'message': 'Нету номера телефона'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def verify_view(request):
    code = request.data.get('code')
    phone = request.data.get('phone')
    if code and phone:
        otp = OTP.objects.filter(phone__iexact=phone)
        if otp.exists():
            otp = otp.first()
            if otp.code == code:
                user = User.objects.filter(phone__iexact=phone)
                if user.exists():
                    user = user.first()
                    user.is_active = True
                    user.save()
                    return Response(
                        {'response': True, 'message': 'Успешно введен'},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'response': False, 'message': 'Такого пользователя нету'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                otp.attempts -= 1
                otp.save()
                return Response(
                    {'response': False,
                        'message': "Осталось попыток {}".format(otp.attempts)}
                )
