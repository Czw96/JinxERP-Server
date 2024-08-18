from extensions.serializers import ModelSerializerEx

from apps.system.models import *


# System
class RoleOptionSerializer(ModelSerializerEx):

    class Meta:
        model = Role
        fields = ['id', 'name']


__all__ = [
    'RoleOptionSerializer',
]
