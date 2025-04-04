from apps.option.views import *
from extensions.routers import SimpleRouterEx

router = SimpleRouterEx()

# System
router.register('role_options', RoleOptionViewSet, 'role_option')
router.register('user_options', UserOptionViewSet, 'user_option')
router.register('warehouse_options', WarehouseOptionViewSet, 'warehouse_option')

urlpatterns = router.urls
