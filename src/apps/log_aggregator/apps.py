from django.apps import AppConfig
from django.utils.translation import gettext_lazy as l_


class LogAggregatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.log_aggregator'

    verbose_name = l_('Агрегация логов Nginx')
