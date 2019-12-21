from django.urls import path, include
from rest_framework_nested import routers
from house import views as hviews

favourites_list = hviews.FavouriteViewSet.as_view({
    'get': 'list'
})

favourites_create = hviews.FavouriteViewSet.as_view({
    'post': 'create'
})

favourites_delete = hviews.FavouriteViewSet.as_view({
    'delete': 'destroy'
})

router = routers.SimpleRouter()
router.register(r'houses', hviews.HouseViewSet, 'House')
router.register(r'house_types', hviews.HouseTypeViewSet)
router.register(r'cities', hviews.CityViewSet)
router.register(r'accommodations', hviews.AccommodationViewSet)
router.register(r'near_buildings', hviews.NearBuildingViewSet)
router.register(r'rules', hviews.RuleViewSet)

houses_router = routers.NestedSimpleRouter(router, r'houses', lookup='house')
houses_router.register(r'reviews', hviews.ReviewViewSet)
houses_router.register(r'free_dates', hviews.FreeDateIntervalViewSet)

urlpatterns = [
    path('favourites/', favourites_list),
    path('houses/<int:pk>/save_favourite/', favourites_create),
    path('houses/<int:pk>/cancel_favourite/', favourites_delete),
    path('', include(router.urls)),
    path('', include(houses_router.urls))
]
