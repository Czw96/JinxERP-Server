from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from django_filters.rest_framework import DjangoFilterBackend

from extensions.paginations import PageNumberPaginationEx


class FunctionViewSet(ViewSet):
    """功能视图"""

    @property
    def user(self):
        return self.request.user

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


class ModelViewSetEx(QueryViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    """模型视图"""


__all__ = [
    'FunctionViewSet', 'GenericViewSetEx', 'ListViewSet', 'QueryViewSet', 'ModelViewSetEx',
]
