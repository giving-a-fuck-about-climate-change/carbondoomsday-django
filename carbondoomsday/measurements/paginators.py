"""Custom pagination classes."""

from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Page number pagination with custom options."""
    page_query_param = 'page'
    page_size_query_param = 'limit'
