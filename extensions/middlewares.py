from django_tenants.utils import get_tenant_domain_model, remove_www
from channels.db import database_sync_to_async
from django.utils import timezone
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from apps.system.models import User


class TimezoneMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request_timezone := request.META.get('HTTP_X_TIMEZONE'):
            timezone.activate(request_timezone)
        response = self.get_response(request)
        return response


class WebSocketAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    async def get_tenant(self, scope):
        if not (hostname := scope['headers'].get('host')):
            return None

        try:
            domain_model = get_tenant_domain_model()
            hostname = remove_www(hostname.split(':')[0])
            domain = await domain_model.objects.select_related('tenant').aget(domain=hostname)
            return domain.tenant
        except domain_model.DoesNotExist:
            return None

    @database_sync_to_async
    def get_user(self, scope):
        if not (raw_token := scope['query_params'].get('token')):
            return None

        try:
            print(raw_token)
            access_token = AccessToken(raw_token)
            payload = access_token.payload
        except (InvalidToken, TokenError):
            return None

        if not (user_id := payload.get('user_id')):
            return None

        if not (tenant := scope.get('tenant')):
            return None

        try:
            tenant.activate()
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    async def __call__(self, scope, receive, send):
        scope['headers'] = {key.decode(): value.decode() for key, value in scope['headers']}
        scope['query_params'] = {key: values[0] for key, values in parse_qs(scope['query_string'].decode()).items()}
        scope['tenant'] = await self.get_tenant(scope)
        scope['user'] = await self.get_user(scope)
        return await self.inner(scope, receive, send)


__all__ = [
    'TimezoneMiddleware',
    'WebSocketAuthMiddleware',
]
