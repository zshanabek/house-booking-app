from core import consumers

from django.urls import path
from channels.routing import URLRouter

websocket_urlpatterns = URLRouter([
    path("ws/messages/", consumers.ChatConsumer),
    path("ws/reservations/", consumers.ReservationConsumer),
])
