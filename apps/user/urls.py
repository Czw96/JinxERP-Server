from extensions.routers import SimpleRouterEx
from apps.user.views import *


router = SimpleRouterEx()
router.register('roles', RoleViewSet, 'role')
router.register('users', UserViewSet, 'user')
router.register('user', UserActionViewSet, 'user_action')
router.register('warehouses', WarehouseViewSet, 'warehouse')
urlpatterns = router.urls
