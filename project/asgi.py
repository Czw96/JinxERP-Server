"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django_asgi_app = get_asgi_application()


def get_websocket_application():
    from apps.system.consumers import NotificationConsumer
    from apps.task.consumers import ExportTaskConsumer
    from extensions.middlewares import WebSocketAuthMiddleware

    return AllowedHostsOriginValidator(
        WebSocketAuthMiddleware(
            URLRouter([
                path("ws/notifications/", NotificationConsumer.as_asgi()),
                path("ws/export_tasks/", ExportTaskConsumer.as_asgi()),
            ])
        )
    )


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": get_websocket_application(),
})
