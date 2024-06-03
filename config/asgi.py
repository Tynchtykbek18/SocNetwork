import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Move django.setup() here
django_asgi_app = get_asgi_application()
django.setup()

from config.middleware import JWTAuthMiddleware
from apps.chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(JWTAuthMiddleware(URLRouter(websocket_urlpatterns))),
})
