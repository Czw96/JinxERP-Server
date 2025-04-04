from django_filters.rest_framework import DjangoFilterBackend
from django_tenants.utils import get_tenant, schema_context
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from extensions.exceptions import ValidationError
from extensions.paginations import PageNumberPaginationEx
from extensions.schemas import InstanceListRequest


class FunctionViewSet(ViewSet):
    """功能视图"""

    @property
    def user(self):
        return self.request.user

    @property
    def tenant(self):
        return get_tenant(self.request)

    @property
    def context(self):
        return {'request': self.request, 'format': self.format_kwarg, 'view': self}


class GenericViewSetEx(GenericViewSet):
    pagination_class = PageNumberPaginationEx
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['id']
    ordering = ['-id']
    select_related_fields = []
    prefetch_related_fields = []

    @property
    def user(self):
        return self.request.user

    @property
    def tenant(self):
        return get_tenant(self.request)

    @property
    def context(self):
        return self.get_serializer_context()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related(*self.select_related_fields)
        queryset = queryset.prefetch_related(*self.prefetch_related_fields)
        return queryset


class ListViewSet(GenericViewSetEx, ListModelMixin):
    """列表视图"""

    pagination_class = None


class QueryViewSet(GenericViewSetEx, RetrieveModelMixin, ListModelMixin):
    """查询视图"""


class BatchDestroyModelMixin:

    @extend_schema(request=InstanceListRequest, responses={204: None})
    @action(detail=False, methods=['delete'])
    def batch_destroy(self, request, *args, **kwargs):
        serializer = InstanceListRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        instance_set = self.get_queryset().filter(id__in=validated_data['ids'])
        self.perform_batch_destroy(instance_set)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_batch_destroy(self, instance_set):
        instance_set.delete()


class ModelViewSetEx(QueryViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, BatchDestroyModelMixin):
    """模型视图"""


class ArchiveViewSet(QueryViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, BatchDestroyModelMixin):
    """归档视图"""

    def perform_update(self, serializer):
        if serializer.instance.is_deleted:
            raise ValidationError('已删除无法编辑')
        return super().perform_update(serializer)

    @extend_schema(responses={204: None})
    @action(detail=True, methods=['delete'])
    def undo_destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_deleted:
            serializer = self.get_serializer(instance)
            serializer.validate_unique(serializer.data)
            instance.undo_delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ExportModelMixin:
    """"""

    @extend_schema(responses={204: None})
    @action(detail=False, methods=['get', 'post'])
    def export_data(self, request, *args, **kwargs):
        """导出数据"""

        if request.methods == 'GET':
            instance_ids = self.filter_queryset(self.get_queryset()).values_list('id', flat=True)
        elif request.methods == 'POST':
            serializer = InstanceListRequest(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            instance_ids = validated_data['ids']
            if self.get_queryset().filter(id__in=instance_ids).count() != len(instance_ids):
                raise ValidationError('导出数据不存在')
        else:
            raise ValidationError('导出数据错误')
        # 导出中能否进行增删改
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImportModelMixin:
    """"""


__all__ = [
    'FunctionViewSet',
    'GenericViewSetEx',
    'ListViewSet',
    'QueryViewSet',
    'ModelViewSetEx',
    'BatchDestroyModelMixin',
    'ArchiveViewSet',
    'ExportModelMixin',
    'ImportModelMixin',
]
