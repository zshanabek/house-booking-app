from django.urls import path, include
from rest_framework_nested import routers
from house.views import HouseViewSet
from reservation.views import ReservationDetail, ReservationList, ReservationCreate

router = routers.SimpleRouter()
router.register(r'houses', HouseViewSet, 'House')
houses_router = routers.NestedSimpleRouter(router, r'houses', lookup='house')

urlpatterns = [
    path('reservations/', ReservationList.as_view()),
    path('reservations/<int:pk>/', ReservationDetail.as_view()),
    path('houses/<int:pk>/reserve/', ReservationCreate.as_view()),
    path('houses/<int:pk>/cancel_reservation/', ReservationDetail.as_view()),
    path('', include(router.urls)),
    path('', include(houses_router.urls))
]
