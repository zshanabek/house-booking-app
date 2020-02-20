from rest_framework import generics, serializers, exceptions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.db.models import Q
import pytz
import djoser
import datetime
from .models import *
from .serializers import *
from utils.sms import SMS

utc = pytz.timezone('Asia/Almaty')


class RegisterView(generics.GenericAPIView):
    serializer_class = djoser.serializers.UserCreatePasswordRetypeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True
            user.save()
            token = Token.objects.create(user=user)
            user = UserSerializer(
                user, context=self.get_serializer_context()).data
            response = {
                'auth_token': token.key,
                'user': user
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            errors = serializer.errors
            x = next(iter(errors))
            error = errors[x][0]
            data = {'response': False,
                    'error_message': error,
                    'field': x}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            User.objects.get(phone=request.data['phone'])
        except User.DoesNotExist:
            data = {'response': False,
                    'error_message': "Нет такого пользователя"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            user = UserSerializer(
                user, context=self.get_serializer_context()).data
            response = {
                'auth_token': token.key,
                'user': user
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            data = {'response': False,
                    'error_message': 'Неправильный логин или пароль'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


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
                {'response': False, 'message': 'Такого пользователя нет'},
                status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(
            {'response': False, 'message': 'Нет номера телефона'},
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
                    user.is_phone_confirmed = True
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
