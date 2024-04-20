import traceback

from django.db import transaction
from django.conf import settings

from config.celery import BaseTask, app

from apps.log_aggregator.models import NginxLogEntry, ErrorLog


class SplitFileTask(BaseTask):
    name = 'split_file_task'

    def process(self, file_path):
        chunk_size = getattr(settings, 'CHUNK_SIZE', 1024 * 1024)
        chunks = []
        try:
            with open(file_path, 'r') as file:
                chunk = []
                for line in file:
                    chunk.append(line)
                    if len(chunk) >= chunk_size:
                        chunks.append(chunk)
                        chunk = []
                if chunk:
                    chunks.append(chunk)
        except Exception as exc:
            self.on_failure(exc, self.request.id, args=(file_path,), kwargs={}, einfo=None)
            raise
        return chunks

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        formatted_traceback = traceback.format_exc()
        ErrorLog.objects.create(
            process=self.name,
            error_message=str(exc),
            traceback=formatted_traceback
        )
        super().on_failure(exc, task_id, args, kwargs, einfo)


class ParseChunksTask(BaseTask):
    name = 'parse_chunks_task'

    def _parse_line(self, line):
        return {}

    def process(self, chunks):
        entries = []

        try:
            for chunk in chunks:
                for line in chunk:
                    data = self._parse_line(line)
                    entry = NginxLogEntry(**data)
                    entries.append(entry)

            with transaction.atomic():
                NginxLogEntry.objects.bulk_create(entries)

        except Exception as exc:
            self.on_failure(exc, self.request.id, args=(chunks,), kwargs={}, einfo=None)
            raise

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        formatted_traceback = traceback.format_exc()
        ErrorLog.objects.create(
            process=self.name,
            error_message=str(exc),
            traceback=formatted_traceback
        )
        super().on_failure(exc, task_id, args, kwargs, einfo)
