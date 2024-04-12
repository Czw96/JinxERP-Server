from extensions.permissions import ModelPermission, FunctionPermission


class WarehousePermission(ModelPermission):
    code = 'warehouse'


class WarehouseLockPermission(FunctionPermission):
    code = 'warehouse.lock'


class WarehouseUnlockPermission(FunctionPermission):
    code = 'warehouse.unlock'


__all__ = [
    'WarehousePermission',
    'WarehouseLockPermission',
    'WarehouseUnlockPermission',
]
