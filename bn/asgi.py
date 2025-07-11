# with Channels

import django.core
import django.core.asgi
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bn.settings")
django.setup()

application = ProtocolTypeRouter({
    "http": django.core.asgi.get_asgi_application(),
    # "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
})
