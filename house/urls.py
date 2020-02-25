from django.urls import path, include
from rest_framework_nested import routers
from house import views as hviews
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'houses', hviews.HouseViewSet, 'House')
router.register(r'house_types', hviews.HouseTypeViewSet)
router.register(r'cities', hviews.CityViewSet)
router.register(r'regions', hviews.RegionViewSet)
router.register(r'countries', hviews.CountryViewSet)
router.register(r'accommodations', hviews.AccommodationViewSet)
router.register(r'near_buildings', hviews.NearBuildingViewSet)
router.register(r'rules', hviews.RuleViewSet)
router.register(r'favourites', hviews.FavouriteViewSet)


houses_router = routers.NestedSimpleRouter(router, r'houses', lookup='house')
houses_router.register(r'reviews', hviews.ReviewViewSet)
houses_router.register(r'blocked_dates', hviews.BlockedDateIntervalViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(houses_router.urls)),
    path('houses/<int:pk>/save_favourite/', hviews.favourites_create),
    path('houses/<int:pk>/cancel_favourite/', hviews.favourites_delete),
    path('my_houses/', hviews.HouseUserList.as_view()),
    path('coordinates/', hviews.HouseCoordinatesList.as_view())
]
