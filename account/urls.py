from .views import *
from django.urls import path, include

urlpatterns = [
    # path('auth/users/', RegisterView.as_view()),
    # path('auth/token/login/', LoginView.as_view()),
    path('auth/send_code', code_view),
    path('auth/verify', verify_view)
]
