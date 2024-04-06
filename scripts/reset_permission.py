from apps.system.models import Team, PagePermission
from scripts.Permissions import PERMISSIONS


def run(*args):
    for team in Team.objects.all():
        for page_permission_item in PERMISSIONS:
            PagePermission.objects.update_or_create(
                name=page_permission_item['name'], team=team, defaults={'permissions': page_permission_item['permissions']})
