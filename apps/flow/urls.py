from extensions.routers import SimpleRouterEx
from apps.flow.views import *


router = SimpleRouterEx()
router.register('export_tasks', ExportTaskViewSet, 'export_task')
router.register('import_tasks', ImportTaskViewSet, 'import_task')
urlpatterns = router.urls
