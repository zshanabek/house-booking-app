from django.urls import path, include
from rest_framework_nested import routers
from house.views import HouseViewSet
from reservation.views import ReservationHostViewSet, ReservationGuestViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'requests', ReservationHostViewSet)
router.register(r'reservations', ReservationGuestViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
