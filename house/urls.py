from django.urls import path, include
from rest_framework_nested import routers
from house import views as house_views


router = routers.SimpleRouter()
router.register(r'houses', house_views.HouseViewSet)
router.register(r'housetypes', house_views.HouseTypeViewSet)
router.register(r'cities', house_views.CityViewSet)
router.register(r'accommodations', house_views.AccommodationViewSet)
router.register(r'nearbuildings', house_views.NearBuildingViewSet)
router.register(r'rules', house_views.RuleViewSet)

houses_router = routers.NestedSimpleRouter(router, r'houses', lookup='house')
houses_router.register(r'reviews', house_views.ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(houses_router.urls))
]
