from django.urls import path, include
from rest_framework_nested import routers
from house.views import HouseViewSet
from reservation.views import ReservationViewSet, ReservationOwnerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders', ReservationViewSet)
router.register(r'reservations', ReservationOwnerViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
