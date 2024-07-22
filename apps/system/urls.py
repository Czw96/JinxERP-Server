from extensions.routers import SimpleRouterEx
from apps.system.views import *


router = SimpleRouterEx()
router.register('roles', RoleViewSet, 'role')
router.register('users', UserViewSet, 'user')
router.register('user', UserActionViewSet, 'user_action')
router.register('warehouses', WarehouseViewSet, 'warehouse')
router.register('field_configs', FieldConfigViewSet, 'field_config')
urlpatterns = router.urls
