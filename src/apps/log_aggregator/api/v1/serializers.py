from rest_framework import serializers
from apps.log_aggregator.models import NginxLogEntry


class NginxLogEntrySerializer(serializers.ModelSerializer):
    """Serializer для nginx логов"""

    class Meta:
        model = NginxLogEntry
        fields = '__all__'
