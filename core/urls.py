from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from core.views import MessageViewSet, ChatModelViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet, base_name='message-api')
router.register(r'chat_sessions', ChatModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
