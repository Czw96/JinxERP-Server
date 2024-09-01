from extensions.routers import SimpleRouterEx
from apps.data.views import *


router = SimpleRouterEx()
router.register('accounts', AccountViewSet, 'account')
urlpatterns = router.urls
