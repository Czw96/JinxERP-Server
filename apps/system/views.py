from extensions.permissions import IsAuthenticated
from extensions.viewsets import ListViewSet
from apps.system.serializers import *
from apps.system.models import *


class PagePermissionViewSet(ListViewSet):
    """页面权限"""

    serializer_class = PagePermissionSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['id']
    queryset = PagePermission.objects.all()


__all__ = [
    'PagePermissionViewSet',
]
