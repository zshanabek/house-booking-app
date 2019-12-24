from .views import *
from django.urls import path, include

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('send_code', code_view),
    path('verify', verify_view)
]
