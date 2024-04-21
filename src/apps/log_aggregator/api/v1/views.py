from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from apps.log_aggregator.models import NginxLogEntry
from apps.log_aggregator.api.v1.serializers import NginxLogEntrySerializer
from apps.log_aggregator.api.v1.pagination import CachedPageNumberPagination


class NginxLogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для получения nginx логов с пагинацией"""

    queryset = NginxLogEntry.objects.all()
    serializer_class = NginxLogEntrySerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ('time', 'remote_ip', 'method', 'response', 'uri', 'referrer', 'agent')
    search_fields = ('remote_ip', 'uri', 'referrer', 'agent')

    pagination_class = CachedPageNumberPagination
