from django.urls import path, include
from rest_framework_nested import routers
from house import views as house_views

favourites_list = house_views.FavouriteViewSet.as_view({
    'get': 'list'
})

favourites_create = house_views.FavouriteViewSet.as_view({
    'post': 'create'
})

favourites_delete = house_views.FavouriteViewSet.as_view({
    'delete': 'destroy'
})

router = routers.SimpleRouter()
router.register(r'houses', house_views.HouseViewSet, 'House')
router.register(r'house_types', house_views.HouseTypeViewSet)
router.register(r'cities', house_views.CityViewSet)
router.register(r'accommodations', house_views.AccommodationViewSet)
router.register(r'near_buildings', house_views.NearBuildingViewSet)
router.register(r'rules', house_views.RuleViewSet)

houses_router = routers.NestedSimpleRouter(router, r'houses', lookup='house')
houses_router.register(r'reviews', house_views.ReviewViewSet)
houses_router.register(r'free_dates', house_views.FreeDateIntervalViewSet)

urlpatterns = [
    path('favourites/', favourites_list),
    path('houses/<int:pk>/save_favourite/', favourites_create),
    path('houses/<int:pk>/cancel_favourite/', favourites_delete),
    path('', include(router.urls)),
    path('', include(houses_router.urls))
]
