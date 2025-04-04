
from apps.data.models import *
from apps.option.filters import *
from apps.option.models import *
from apps.option.permissions import *
from apps.option.schemas import *
from apps.option.serializers import *
from apps.product.models import *
from apps.purchase.models import *
from apps.sales.models import *
from apps.system.models import *
from extensions.permissions import IsAuthenticated, IsManagerPermission
from extensions.viewsets import ListViewSet


# System
class RoleOptionViewSet(ListViewSet):
    serializer_class = RoleOptionSerializer
    permission_classes = [IsAuthenticated, IsManagerPermission]
    ordering = ['name']
    queryset = Role.objects.all()


class UserOptionViewSet(ListViewSet):
    serializer_class = UserOptionSerializer
    permission_classes = [IsAuthenticated, UserOptionPermission]
    filterset_fields = ['is_enabled']
    ordering = ['name']
    queryset = User.objects.filter(is_deleted=False)


class WarehouseOptionViewSet(ListViewSet):
    serializer_class = WarehouseOptionSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['name']

    def get_queryset(self):
        return self.user.get_warehouse_set()


__all__ = [
    'RoleOptionViewSet',
    'UserOptionViewSet',
    'WarehouseOptionViewSet',
]
