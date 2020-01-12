from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from core.api import MessageModelViewSet, ChatModelViewSet

router = DefaultRouter()
router.register(r'messages', MessageModelViewSet, base_name='message-api')
router.register(r'chats', ChatModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
