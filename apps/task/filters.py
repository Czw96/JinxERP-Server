from django_filters import FilterSet
import django_filters

from apps.task.models import *


class ExportTaskFilter(FilterSet):
    start_date = django_filters.DateTimeFilter(field_name='create_time', lookup_expr='date__gte', label='开始日期')
    end_date = django_filters.DateTimeFilter(field_name='create_time', lookup_expr='date__lte', label='结束日期')

    class Meta:
        model = ExportTask
        fields = ['model', 'status', 'creator', 'start_date', 'end_date']


class ImportTaskFilter(FilterSet):
    start_date = django_filters.DateTimeFilter(field_name='create_time', lookup_expr='date__gte', label='开始日期')
    end_date = django_filters.DateTimeFilter(field_name='create_time', lookup_expr='date__lte', label='结束日期')

    class Meta:
        model = ImportTask
        fields = ['model', 'status', 'creator', 'start_date', 'end_date']


__all__ = [
    'ExportTaskFilter',
    'ImportTaskFilter',
]
