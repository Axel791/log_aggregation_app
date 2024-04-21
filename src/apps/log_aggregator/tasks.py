import json
import traceback

from datetime import datetime

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
                        pars_chunks_task.apply_async(args=(chunk,))
                        chunk = []
                if chunk:
                    pars_chunks_task.apply_async(args=(chunk,))
        except Exception as exc:
            self.on_failure(exc, self.request.id, args=(chunks,), kwargs={}, einfo=traceback.format_exc())
        return 'Все чанки были отправлен на обработку.'

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        ErrorLog.objects.create(
            process=self.name,
            error_message=str(exc),
            traceback=einfo
        )
        super().on_failure(exc, task_id, args, kwargs, einfo)


class ParseChunksTask(BaseTask):
    name = 'parse_chunks_task'

    @staticmethod
    def _extract_data(data):
        time_str = data.get("time", "")
        parsed_time = datetime.strptime(time_str, "%d/%b/%Y:%H:%M:%S %z") if time_str else None
        return {
            "time": parsed_time,
            "remote_ip": data.get("remote_ip", ""),
            "remote_user": data.get("remote_user", ""),
            "method": data.get("request", "").split()[0] if "request" in data else "",
            "uri": data.get("request", "").split()[1] if "request" in data and len(
                data["request"].split()) > 1 else "",
            "response": int(data.get("response", 0)),
            "bytes_sent": int(data.get("bytes", 0)),
            "referrer": data.get("referrer", ""),
            "agent": data.get("agent", "")
        }

    def _parse_line(self, line):
        if not line.strip():
            return None
        try:
            data = json.loads(line)
            return self._extract_data(data)
        except json.JSONDecodeError as e:
            self.on_failure(e, self.request.id, args=(line,), kwargs={}, einfo=traceback.format_exc())
            return None

    def process(self, chunk):
        entries = []
        for line in chunk:
            data = self._parse_line(line)
            if data:
                try:
                    entry = NginxLogEntry(**data)
                    entries.append(entry)
                except Exception as e:
                    self.on_failure(e, self.request.id, args=(line,), kwargs={}, einfo=traceback.format_exc())

        try:
            with transaction.atomic():
                NginxLogEntry.objects.bulk_create(entries)
        except Exception as exc:
            self.on_failure(exc, self.request.id, args=(chunk,), kwargs={}, einfo=traceback.format_exc())

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        ErrorLog.objects.create(
            process=self.name,
            error_message=str(exc),
            traceback=einfo
        )
        super().on_failure(exc, task_id, args, kwargs, einfo)


pars_chunks_task = app.register_task(ParseChunksTask())
split_file_task = app.register_task(SplitFileTask())
