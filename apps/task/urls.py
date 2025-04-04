from apps.task.views import *
from extensions.routers import SimpleRouterEx

router = SimpleRouterEx()
router.register('export_tasks', ExportTaskViewSet, 'export_task')
router.register('import_tasks', ImportTaskViewSet, 'import_task')
urlpatterns = router.urls
