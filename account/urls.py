from .views import *
from django.urls import path, include

urlpatterns = [
    path('auth/send_code', code_view),
    path('auth/verify', verify_view)
]
