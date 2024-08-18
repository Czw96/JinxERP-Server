
from extensions.permissions import IsAuthenticated, IsManagerPermission
from extensions.viewsets import ListViewSet
from apps.option.serializers import *
from apps.option.permissions import *
from apps.option.filters import *
from apps.option.schemas import *
from apps.option.models import *
from apps.purchase.models import *
from apps.product.models import *
from apps.system.models import *
from apps.sales.models import *
from apps.data.models import *


# System
class RoleOptionViewSet(ListViewSet):
    serializer_class = RoleOptionSerializer
    permission_classes = [IsAuthenticated, IsManagerPermission]
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    ordering = ['name', '-id']
    queryset = Role.objects.all()


__all__ = [
    'RoleOptionViewSet',
]
