from apps.data.views import *
from extensions.routers import SimpleRouterEx

router = SimpleRouterEx()
router.register('accounts', AccountViewSet, 'account')
urlpatterns = router.urls
