from django.contrib import admin
from django.utils.translation import gettext_lazy as l_

from apps.log_aggregator.models import NginxLogEntry, ErrorLog


class BaseLogAdmin(admin.ModelAdmin):
    """Базовый клас для админки с логами"""

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(NginxLogEntry)
class NginxLogEntryAdmin(BaseLogAdmin):
    """AdminView для логов nginx"""

    # region Настройка листинга
    list_display = ('time', 'remote_ip', 'method', 'uri', 'response', 'bytes_sent')
    list_filter = ('time', 'method', 'response')

    search_fields = ('remote_ip', 'uri', 'agent')
    date_hierarchy = 'time'

    ordering = ('-time',)
    # endregion

    # region Настройки детальной страницы
    fieldsets = (
        (l_('Основная информация'), {
            'fields': ('time', 'remote_ip', 'remote_user')
        }),
        (l_('Детали запроса'), {
            'fields': ('method', 'uri', 'agent')
        }),
        (l_('Информация о ответе'), {
            'fields': ('response', 'bytes_sent', 'referrer')
        }),
    )
    # endregion


@admin.register(ErrorLog)
class ErrorLogAdmin(BaseLogAdmin):
    """AdminView для просмотра логов при ошибке парсинга."""

    # region Настройки листинга
    list_display = ('time', 'get_process_display', 'error_message')
    list_filter = ('process', 'time')
    search_fields = ('error_message', 'traceback')
    date_hierarchy = 'time'
    ordering = ('-time',)
    # endregion

    # region Настройки детальной страницы
    fieldsets = (
        (l_('Детали ошибки'), {
            'fields': ('time', 'process', 'error_message')
        }),
        (l_('Traceback'), {
            'fields': ('traceback',),
            'classes': ('collapse',)
        }),
    )
    # endregion

    def get_process_display(self, obj):
        return obj.get_process_display()

    get_process_display.admin_order_field = 'process'
    get_process_display.short_description = 'Процесс'
