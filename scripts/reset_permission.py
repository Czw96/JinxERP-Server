from apps.system.models import PagePermission
from scripts.Permissions import PERMISSIONS


def run(*args):
    for page_permission_item in PERMISSIONS:
        PagePermission.objects.update_or_create(
            name=page_permission_item['name'], defaults={'permissions': page_permission_item['permissions']})
