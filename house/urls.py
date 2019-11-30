from django.urls import path, include

from rest_framework import routers

from house import views as house_views


router = routers.DefaultRouter()
router.register('', house_views.MyViewSet, base_name='MyView')
urlpatterns = [
    path('', include(router.urls))
]
