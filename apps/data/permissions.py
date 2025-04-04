from extensions.permissions import FunctionPermission, ModelPermission


class AccountPermission(ModelPermission):
    code = 'account'


class AccountExportPermission(FunctionPermission):
    code = 'account.export'


class AccountImportPermission(FunctionPermission):
    code = 'account.import'


__all__ = [
    'AccountPermission',
    'AccountExportPermission',
    'AccountImportPermission',
]
