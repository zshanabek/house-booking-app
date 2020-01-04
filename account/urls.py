from .views import *
from django.urls import path, include

urlpatterns = [
    path('auth/register', RegisterView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('auth/logout', LoginView.as_view()),
    path('auth/send_code', code_view),
    path('auth/verify', verify_view),
    path('users/<int:pk>/', user_list, name='user-detail'),
    path('users/', user_list, name='user-list'),
    path('profile', UserView.as_view()),
]
