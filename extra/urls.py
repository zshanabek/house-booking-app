from django.urls import path, include
from rest_framework_nested import routers
from .views import FeedbackViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'feedback', FeedbackViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
