from django.utils import timezone


class TimezoneMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request_timezone := request.META.get('HTTP_X_TIMEZONE'):
            timezone.activate(request_timezone)
        response = self.get_response(request)
        return response


__all__ = [
    'TimezoneMiddleware',
]
