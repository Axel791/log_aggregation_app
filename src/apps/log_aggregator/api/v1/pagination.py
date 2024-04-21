import hashlib

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from django.core.cache import cache


class CachedPageNumberPagination(PageNumberPagination):
    """Класс с пагинацией и кэшированием данных для более быстрой загрузки."""

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        query_params = self.request.query_params.copy()
        base_url = self.request.build_absolute_uri()

        query_string = '&'.join([f"{key}={value}" for key, value in sorted(query_params.items())])
        key_hash = hashlib.md5(query_string.encode('utf-8')).hexdigest()
        cache_key = f"{base_url}:{key_hash}"

        cached_data = cache.get(cache_key)
        if cached_data:
            response_data = cached_data
        else:
            response_data = {
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'count': self.page.paginator.count,
                'results': data
            }
            cache.set(cache_key, response_data, timeout=1000)

        return Response(response_data)
