from extensions.routers import SimpleRouterEx
from apps.option.views import *


router = SimpleRouterEx()

# System
router.register('role_options', RoleOptionViewSet, 'role_option')

urlpatterns = router.urls
