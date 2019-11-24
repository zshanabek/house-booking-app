from .views import *
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', MyViewSet, base_name='MyView')

urlpatterns = [
    path('', include(router.urls))
]
