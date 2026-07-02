from __future__ import annotations

import threading
import time
from collections import defaultdict
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any


class TimerContext:
    """Context manager for timing operations."""

    def __init__(self, name: str, collector: MetricsCollector) -> None:
        self._name = name
        self._collector = collector
        self._start: float = 0.0

    def __enter__(self) -> TimerContext:
        self._start = time.monotonic()
        return self

    def __exit__(self, *args: Any) -> None:
        duration = (time.monotonic() - self._start) * 1000
        self._collector.record_histogram(self._name, duration)


class TraceSpan:
    """Represents a trace span."""

    def __init__(self, name: str, parent: TraceSpan | None = None) -> None:
        self.name = name
        self.parent = parent
        self.start_time = time.monotonic()
        self.end_time: float | None = None
        self.attributes: dict[str, Any] = {}
        self.status = "ok"
        self.children: list[TraceSpan] = []

    def end(self) -> None:
        self.end_time = time.monotonic()

    @property
    def duration_ms(self) -> float:
        if self.end_time is None:
            return (time.monotonic() - self.start_time) * 1000
        return (self.end_time - self.start_time) * 1000

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms,
            "status": self.status,
            "attributes": self.attributes,
            "children": [c.to_dict() for c in self.children],
        }


class MetricsCollector:
    """Thread-safe metrics collection."""

    def __init__(self) -> None:
        self._counters: dict[str, float] = defaultdict(float)
        self._gauges: dict[str, float] = {}
        self._histograms: dict[str, list[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def increment(self, name: str, value: float = 1.0, **tags: str) -> None:
        key = self._make_key(name, tags)
        with self._lock:
            self._counters[key] += value

    def set_gauge(self, name: str, value: float, **tags: str) -> None:
        key = self._make_key(name, tags)
        with self._lock:
            self._gauges[key] = value

    def record_histogram(self, name: str, value: float, **tags: str) -> None:
        key = self._make_key(name, tags)
        with self._lock:
            self._histograms[key].append(value)
            if len(self._histograms[key]) > 1000:
                self._histograms[key] = self._histograms[key][-500:]

    def _make_key(self, name: str, tags: dict[str, str]) -> str:
        if tags:
            tag_str = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
            return f"{name}{{{tag_str}}}"
        return name

    def get_counter(self, name: str, **tags: str) -> float:
        key = self._make_key(name, tags)
        with self._lock:
            return self._counters.get(key, 0.0)

    def get_gauge(self, name: str, **tags: str) -> float | None:
        key = self._make_key(name, tags)
        with self._lock:
            return self._gauges.get(key)

    def get_histogram(self, name: str, **tags: str) -> dict[str, float]:
        key = self._make_key(name, tags)
        with self._lock:
            values = list(self._histograms.get(key, []))
        if not values:
            return {}
        values_sorted = sorted(values)
        return {
            "count": len(values),
            "sum": sum(values),
            "min": values_sorted[0],
            "max": values_sorted[-1],
            "avg": sum(values) / len(values),
            "p50": values_sorted[len(values_sorted) // 2],
            "p95": values_sorted[int(len(values_sorted) * 0.95)],
            "p99": values_sorted[int(len(values_sorted) * 0.99)],
        }

    def get_all(self) -> dict[str, Any]:
        with self._lock:
            return {
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "histograms": {
                    k: self._compute_histogram_stats(v) for k, v in self._histograms.items()
                },
            }

    def _compute_histogram_stats(self, values: list[float]) -> dict[str, float]:
        if not values:
            return {}
        values_sorted = sorted(values)
        return {
            "count": len(values),
            "sum": sum(values),
            "avg": sum(values) / len(values),
        }

    def reset(self) -> None:
        with self._lock:
            self._counters.clear()
            self._gauges.clear()
            self._histograms.clear()


class TelemetryEngine:
    """Metrics, health, and tracing engine."""

    def __init__(self) -> None:
        self._metrics = MetricsCollector()
        self._health_checks: dict[str, Callable[[], dict[str, Any]]] = {}
        self._current_trace: TraceSpan | None = None
        self._trace_stack: list[TraceSpan] = []
        self._completed_traces: list[TraceSpan] = []
        self._lock = threading.Lock()

    def counter(self, name: str, value: float = 1.0, **tags: str) -> None:
        self._metrics.increment(name, value, **tags)

    def gauge(self, name: str, value: float, **tags: str) -> None:
        self._metrics.set_gauge(name, value, **tags)

    def histogram(self, name: str, value: float, **tags: str) -> None:
        self._metrics.record_histogram(name, value, **tags)

    def timer(self, name: str) -> TimerContext:
        return TimerContext(name, self._metrics)

    def register_health_check(self, name: str, check: Callable[[], dict[str, Any]]) -> None:
        self._health_checks[name] = check

    async def health_check(self) -> dict[str, Any]:
        results: dict[str, Any] = {}
        all_healthy = True

        for name, check in self._health_checks.items():
            try:
                result = check()
                results[name] = result
                if result.get("status") != "healthy":
                    all_healthy = False
            except Exception as e:
                results[name] = {"status": "unhealthy", "error": str(e)}
                all_healthy = False

        return {
            "status": "healthy" if all_healthy else "degraded",
            "components": results,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    def start_trace(self, name: str) -> TraceSpan:
        with self._lock:
            parent = self._current_trace
            span = TraceSpan(name, parent)
            if parent:
                parent.children.append(span)
            self._trace_stack.append(span)
            self._current_trace = span
        return span

    def end_trace(self) -> TraceSpan | None:
        with self._lock:
            if self._trace_stack:
                span = self._trace_stack.pop()
                span.end()
                self._current_trace = self._trace_stack[-1] if self._trace_stack else None
                if not span.parent:
                    self._completed_traces.append(span)
                return span
        return None

    def get_traces(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._lock:
            return [t.to_dict() for t in self._completed_traces[-limit:]]

    def get_metrics(self) -> dict[str, Any]:
        return self._metrics.get_all()

    def flush(self) -> None:
        pass

    def reset(self) -> None:
        self._metrics.reset()
        with self._lock:
            self._completed_traces.clear()
            self._trace_stack.clear()
            self._current_trace = None
