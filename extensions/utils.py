from django.utils import timezone


def generate_number(prefix):
    now = timezone.localtime()
    date_part = now.strftime('%Y%m%d')
    time_part = now.strftime('%H%M%S')
    millisecond_part = now.strftime('%f')[:4]

    number = f"{prefix}{date_part}-{time_part}-{millisecond_part}"
    return number


__all__ = [
    'generate_number',
]
