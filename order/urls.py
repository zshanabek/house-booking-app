from .views import *
from django.urls import path, include

urlpatterns = [
    path('pay', create_payment),
    path('payments/<int:pk>/', get_payment),
    path('payment_status', get_payment_status)
]
