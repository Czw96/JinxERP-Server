from extensions.routers import SimpleRouterEx
from apps.option.views import *


router = SimpleRouterEx()

# System
router.register('role_options', RoleOptionViewSet, 'role_option')
router.register('user_options', UserOptionViewSet, 'user_option')
router.register('warehouse_options', WarehouseOptionViewSet, 'warehouse_option')

urlpatterns = router.urls
