from __future__ import annotations

import json
import logging
import sys
import threading
from datetime import UTC, datetime
from typing import Any
from uuid import UUID


class CorrelationFilter(logging.Filter):
    """Injects correlation ID into log records."""

    def __init__(self) -> None:
        super().__init__()
        self._correlation_id: UUID | None = None
        self._context: dict[str, Any] = {}

    def set_correlation_id(self, correlation_id: UUID | None) -> None:
        self._correlation_id = correlation_id

    def set_context(self, **kwargs: Any) -> None:
        self._context.update(kwargs)

    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = str(self._correlation_id) if self._correlation_id else None  # type: ignore[attr-defined]
        record.extra_context = dict(self._context)  # type: ignore[attr-defined]
        return True


class StructuredFormatter(logging.Formatter):
    """Formats log records as structured JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        correlation_id = getattr(record, "correlation_id", None)
        if correlation_id:
            log_entry["correlation_id"] = correlation_id

        extra_context = getattr(record, "extra_context", {})
        if extra_context:
            log_entry["context"] = extra_context

        if record.exc_info and record.exc_info[1]:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]),
            }

        return json.dumps(log_entry, default=str)


class AuditHandler(logging.Handler):
    """Special handler for audit log entries."""

    def __init__(self) -> None:
        super().__init__()
        self._entries: list[dict[str, Any]] = []
        self._lock = threading.Lock()

    def emit(self, record: logging.LogRecord) -> None:
        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "action": getattr(record, "audit_action", ""),
            "subject": getattr(record, "audit_subject", ""),
            "actor": getattr(record, "audit_actor", ""),
            "result": getattr(record, "audit_result", ""),
            "details": getattr(record, "audit_details", {}),
        }
        with self._lock:
            self._entries.append(entry)

    def get_entries(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._entries[-limit:])

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()


class LoggingEngine:
    """Structured logging engine with correlation IDs and audit support."""

    def __init__(
        self,
        level: str = "INFO",
        output: str = "stdout",
        json_format: bool = True,
    ) -> None:
        self._logger = logging.getLogger("platform_core")
        self._correlation_filter = CorrelationFilter()
        self._audit_handler = AuditHandler()
        self._log_entries: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        self._json_format = json_format

        self._logger.addFilter(self._correlation_filter)

        if json_format:
            formatter: logging.Formatter = StructuredFormatter()
        else:
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

        if output == "stdout":
            handler: logging.Handler = logging.StreamHandler(sys.stdout)
        elif output == "stderr":
            handler = logging.StreamHandler(sys.stderr)
        else:
            handler = logging.FileHandler(output)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

        audit_handler = logging.Handler()
        audit_handler.setFormatter(formatter)
        self._logger.addHandler(self._audit_handler)

        self._logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    def debug(self, message: str, **kwargs: Any) -> None:
        self._log(logging.DEBUG, message, kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        self._log(logging.INFO, message, kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        self._log(logging.WARNING, message, kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        self._log(logging.ERROR, message, kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        self._log(logging.CRITICAL, message, kwargs)

    def _log(self, level: int, message: str, kwargs: dict[str, Any]) -> None:
        extra: dict[str, Any] = {}
        if kwargs:
            extra["extra_context"] = kwargs
        self._logger.log(level, message, extra=extra)

        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": logging.getLevelName(level),
            "message": message,
            "context": kwargs,
        }
        correlation_id = self._correlation_filter._correlation_id
        if correlation_id:
            entry["correlation_id"] = str(correlation_id)

        with self._lock:
            self._log_entries.append(entry)
            if len(self._log_entries) > 10000:
                self._log_entries = self._log_entries[-5000:]

    def audit(
        self,
        action: str,
        subject: str,
        actor: str = "",
        result: str = "",
        **kwargs: Any,
    ) -> None:
        record = self._logger.makeRecord(
            name="platform_core.audit",
            level=logging.INFO,
            fn="",
            lno=0,
            msg="",
            args=(),
            exc_info=None,
        )
        record.audit_action = action  # type: ignore[attr-defined]
        record.audit_subject = subject  # type: ignore[attr-defined]
        record.audit_actor = actor  # type: ignore[attr-defined]
        record.audit_result = result  # type: ignore[attr-defined]
        record.audit_details = kwargs  # type: ignore[attr-defined]
        self._audit_handler.emit(record)

    def with_correlation(self, correlation_id: UUID) -> LoggingEngine:
        new_engine = LoggingEngine.__new__(LoggingEngine)
        new_engine._logger = self._logger
        new_engine._correlation_filter = CorrelationFilter()
        new_engine._correlation_filter.set_correlation_id(correlation_id)
        new_engine._audit_handler = self._audit_handler
        new_engine._log_entries = self._log_entries
        new_engine._lock = self._lock
        new_engine._json_format = self._json_format
        return new_engine

    def with_context(self, **kwargs: Any) -> LoggingEngine:
        new_engine = LoggingEngine.__new__(LoggingEngine)
        new_engine._logger = self._logger
        new_engine._correlation_filter = CorrelationFilter()
        new_engine._correlation_filter._context = dict(kwargs)
        new_engine._audit_handler = self._audit_handler
        new_engine._log_entries = self._log_entries
        new_engine._lock = self._lock
        new_engine._json_format = self._json_format
        return new_engine

    def get_audit_entries(self, limit: int = 100) -> list[dict[str, Any]]:
        return self._audit_handler.get_entries(limit)

    def get_log_entries(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._log_entries[-limit:])
