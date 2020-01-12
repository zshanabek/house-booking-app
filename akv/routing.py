from channels.routing import ProtocolTypeRouter
from core import routing as core_routing
from core.middlewares import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    "websocket": TokenAuthMiddlewareStack(core_routing.websocket_urlpatterns)
})

