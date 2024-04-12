from extensions.serializers import ModelSerializerEx
from apps.system.models import *


class PagePermissionSerializer(ModelSerializerEx):

    class Meta:
        model = PagePermission
        fields = ['id', 'name', 'permissions']


__all__ = [
    'PagePermissionSerializer',
]
