from django.urls import path, include
from rest_framework_nested import routers
from house import views as house_views

reservations_list = house_views.ReservationViewSet.as_view({
    'get': 'list'
})

reservations_create = house_views.ReservationViewSet.as_view({
    'post': 'create'
})

reservations_delete = house_views.ReservationViewSet.as_view({
    'delete': 'destroy'
})

router = routers.SimpleRouter()

houses_router = routers.NestedSimpleRouter(router, r'houses', lookup='house')
houses_router.register(r'reviews', house_views.ReviewViewSet)

urlpatterns = [
    path('reservations/', reservations_list),
    path('houses/<int:pk>/reserve/', reservations_create),
    path('houses/<int:pk>/cancel_reservation/', reservations_delete),
    path('', include(router.urls)),
    path('', include(houses_router.urls))
]
