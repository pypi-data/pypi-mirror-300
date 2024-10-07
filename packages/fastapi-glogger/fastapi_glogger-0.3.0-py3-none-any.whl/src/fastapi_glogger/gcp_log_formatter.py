import logging
from typing import Any
from starlette_context import context
import json


class GcpLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        """Get the JSON-encoded log format for structured logging.

        See https://cloud.google.com/logging/docs/structured-logging"""
        record.message = record.getMessage()
        record.asctime = self.formatTime(record, self.datefmt)
        log_entry = {
            "severity": "%(levelname)s",
            "timestamp": "%(asctime)s",
            # "commit": env.commit(),
            "pathname": "%(pathname)s",
            "logger_name": "%(name)s",
            "logging.googleapis.com/sourceLocation": {
                "file": "%(filename)s",
                "line": "%(lineno)d",
                "function": "%(funcName)s",
            },
        }

        def _format_dict(d: dict[str, Any], record: logging.LogRecord) -> None:
            for k, v in d.items():
                if isinstance(v, dict):
                    _format_dict(v, record)
                    continue
                d[k] = v % record.__dict__

        _format_dict(log_entry, record)

        if context.exists():
            audit_info = {}
            if "span_id" in context.data:
                log_entry["logging.googleapis.com/spanId"] = context.data["span_id"]
                del context.data["span_id"]

            for key in context.data.keys():
                if isinstance(key, str):
                    # process the key
                    audit_info[key] = context.data[key]
                else:
                    logging.error(f"Unexpected key type: {type(key)} for key: {key}")

            if audit_info:
                log_entry["auditInfo"] = audit_info

        # We call super to grab the main message, so we get things like exception
        # handling for free.
        log_entry["message"] = super().format(record)

        return json.dumps(log_entry)
