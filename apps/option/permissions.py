from extensions.permissions import OptionPermission


# System
class UserOptionPermission(OptionPermission):
    code_set = {'export_task.query_all', 'import_task.query_all'}


__all__ = [
    'UserOptionPermission',
]
