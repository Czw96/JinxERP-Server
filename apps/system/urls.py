from apps.system.views import *
from extensions.routers import SimpleRouterEx

router = SimpleRouterEx()
router.register('roles', RoleViewSet, 'role')
router.register('users', UserViewSet, 'user')
router.register('user', UserActionViewSet, 'user_action')
router.register('warehouses', WarehouseViewSet, 'warehouse')
router.register('model_fields', ModelFieldViewSet, 'model_field')
router.register('system_config', SystemConfigViewSet, 'system_config')
router.register('notifications', NotificationViewSet, 'notification')
urlpatterns = router.urls
