# Generated by Django 5.0.4 on 2024-04-20 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='Время ошибки')),
                ('process', models.CharField(choices=[(1, 'Парсинг чанков'), (2, 'Запись чанков')], help_text='Процесс, в котором произошла ошибка', verbose_name='Процесс')),
                ('error_message', models.TextField(verbose_name='Сообщение об ошибке')),
                ('traceback', models.TextField(blank=True, null=True, verbose_name='Traceback')),
            ],
            options={
                'verbose_name': 'Лог ошибки',
                'verbose_name_plural': 'Логи ошибок',
                'ordering': ['-time'],
            },
        ),
        migrations.CreateModel(
            name='NginxLogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='Время запроса')),
                ('remote_ip', models.GenericIPAddressField(verbose_name='IP-адрес отправителя')),
                ('remote_user', models.CharField(blank=True, max_length=256, null=True, verbose_name='Пользователь')),
                ('method', models.CharField(max_length=10, verbose_name='HTTP метод')),
                ('uri', models.CharField(max_length=1024, verbose_name='URI запроса')),
                ('response', models.IntegerField(verbose_name='Код ответа HTTP')),
                ('bytes_sent', models.IntegerField(verbose_name='Количество отправленных байт')),
                ('referrer', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Источник перехода')),
                ('agent', models.CharField(max_length=256, verbose_name='Пользовательский агент')),
            ],
            options={
                'verbose_name': 'Nginx лог',
                'verbose_name_plural': 'Nginx логи',
                'ordering': ['-time'],
                'indexes': [models.Index(fields=['time', 'remote_ip'], name='index_time_ip')],
            },
        ),
    ]
