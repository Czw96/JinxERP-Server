from extensions.permissions import ModelPermission, QueryPermission, FunctionPermission


class ExportTaskPermission(ModelPermission):
    code = 'export_task'


class ExportTaskQueryAllPermission(QueryPermission):
    code = 'export_task.query_all'


class ExportTaskCancelPermission(FunctionPermission):
    code = 'export_task.cancel'


class ExportTaskDownloadPermission(FunctionPermission):
    code = 'export_task.wownload'


class ImportTaskPermission(ModelPermission):
    code = 'import_task'


class ImportTaskQueryAllPermission(QueryPermission):
    code = 'import_task.query_all'


class ImportTaskCancelPermission(FunctionPermission):
    code = 'import_task.cancel'


class ImportTaskDownloadPermission(FunctionPermission):
    code = 'import_task.wownload'


__all__ = [
    'ExportTaskPermission',
    'ExportTaskQueryAllPermission',
    'ExportTaskCancelPermission',
    'ExportTaskDownloadPermission',
    'ImportTaskPermission',
    'ImportTaskQueryAllPermission',
    'ImportTaskCancelPermission',
    'ImportTaskDownloadPermission',
]
