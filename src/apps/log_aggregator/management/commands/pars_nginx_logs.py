import os

from django.core.management.base import BaseCommand

from apps.log_aggregator.tasks import split_file_task


class Command(BaseCommand):
    help = 'Обработка файла с nginx логами.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь до файла с логами')

    def handle(self, *args, **options):
        file_path = options['file_path']

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR('Такого файла не существует.'))
            return

        result = split_file_task.apply_async(args=(file_path, ))
        self.stdout.write(self.style.SUCCESS('Цепочка запущена, ID: {}'.format(result.id)))
