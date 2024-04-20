from django.db import models
from django.utils.translation import gettext_lazy as l_


class NginxLogEntry(models.Model):
    """Модель логов Nginx"""

    time = models.DateTimeField(verbose_name=l_('Время запроса'))
    remote_ip = models.GenericIPAddressField(verbose_name=l_('IP-адрес отправителя'))
    remote_user = models.CharField(max_length=256, blank=True, null=True, verbose_name=l_('Пользователь'))
    method = models.CharField(max_length=10, verbose_name=l_('HTTP метод'))
    uri = models.CharField(max_length=1024, verbose_name=l_('URI запроса'))
    response = models.IntegerField(verbose_name=l_('Код ответа HTTP'))
    bytes_sent = models.IntegerField(verbose_name=l_('Количество отправленных байт'))
    referrer = models.CharField(max_length=1024, blank=True, null=True, verbose_name=l_('Источник перехода'))
    agent = models.CharField(max_length=256, verbose_name=l_('Пользовательский агент'))

    class Meta:
        verbose_name = l_("Nginx лог")
        verbose_name_plural = l_("Nginx логи")

        ordering = ['-time']

        indexes = [models.Index(fields=['time', 'remote_ip'], name='index_time_ip')]

    def __str__(self):
        return f"{self.time} - {self.remote_ip}"


class ProcessTypes(models.IntegerChoices):
    PARSING_CHUNKS = 1, l_('Парсинг чанков')
    WRITING_CHUNKS = 2, l_('Запись чанков')


class ErrorLog(models.Model):
    """Модель ошибок при обработке файла."""

    time = models.DateTimeField(auto_now_add=True, verbose_name=l_('Время ошибки'))
    process = models.CharField(
        choices=ProcessTypes.choices,
        verbose_name=l_('Процесс'),
        help_text=l_('Процесс, в котором произошла ошибка')
    )
    error_message = models.TextField(verbose_name=l_('Сообщение об ошибке'))
    traceback = models.TextField(verbose_name=l_('Traceback'), blank=True, null=True)

    class Meta:
        verbose_name = l_('Лог ошибки')
        verbose_name_plural = l_('Логи ошибок')
        ordering = ['-time']

    def __str__(self):
        return f"{self.time} - {self.process} - {self.error_message[:50]}"
