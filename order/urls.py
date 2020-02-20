from django.urls import path, include
from rest_framework_nested import routers
from .views import *
from rest_framework.routers import DefaultRouter
from .models import Order

router = DefaultRouter()
router.register(r'payments', OrderViewSet, basename='Order')

urlpatterns = [
    path('', include(router.urls)),
    path('pay', create_payment),
    path('payments_paybox/<int:pk>/', get_payment),
    path('payment_status', payment_status_webhook)
]
