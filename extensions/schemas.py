from rest_framework.serializers import Serializer
from rest_framework import serializers


class MakeNumberResponse(Serializer):
    number = serializers.CharField(label='编号')


__all__ = [
    'MakeNumberResponse',
]
