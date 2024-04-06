from rest_framework.pagination import PageNumberPagination


class PageNumberPaginationEx(PageNumberPagination):
    invalid_page_message = '未查询到数据'
    page_size_query_param = 'page_size'
    max_page_size = 60
    page_size = 15


__all__ = [
    'PageNumberPaginationEx',
]
