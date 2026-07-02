from __future__ import annotations

import pytest

from platform_core.runtime.telemetry.engine import TelemetryEngine


class TestTelemetryEngine:
    def test_counter(self) -> None:
        engine = TelemetryEngine()
        engine.counter("test.counter", value=1.0)
        engine.counter("test.counter", value=2.0)
        metrics = engine.get_metrics()
        assert metrics["counters"]["test.counter"] == 3.0

    def test_gauge(self) -> None:
        engine = TelemetryEngine()
        engine.gauge("test.gauge", 42.0)
        metrics = engine.get_metrics()
        assert metrics["gauges"]["test.gauge"] == 42.0

    def test_histogram(self) -> None:
        engine = TelemetryEngine()
        engine.histogram("test.hist", 1.0)
        engine.histogram("test.hist", 2.0)
        engine.histogram("test.hist", 3.0)
        stats = engine.get_metrics()["histograms"]["test.hist"]
        assert stats["count"] == 3
        assert stats["avg"] == 2.0

    def test_timer(self) -> None:
        engine = TelemetryEngine()
        with engine.timer("test.timer"):
            pass
        stats = engine.get_metrics()["histograms"]["test.timer"]
        assert stats["count"] == 1

    @pytest.mark.asyncio
    async def test_health_check(self) -> None:
        engine = TelemetryEngine()
        engine.register_health_check("test", lambda: {"status": "healthy"})
        result = await engine.health_check()
        assert result["status"] == "healthy"
        assert "test" in result["components"]

    @pytest.mark.asyncio
    async def test_health_check_unhealthy(self) -> None:
        engine = TelemetryEngine()
        engine.register_health_check("failing", lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        result = await engine.health_check()
        assert result["status"] == "degraded"

    def test_trace(self) -> None:
        engine = TelemetryEngine()
        span = engine.start_trace("test")
        assert span.name == "test"
        engine.end_trace()
        traces = engine.get_traces()
        assert len(traces) == 1

    def test_reset(self) -> None:
        engine = TelemetryEngine()
        engine.counter("test", 1.0)
        engine.reset()
        metrics = engine.get_metrics()
        assert metrics["counters"] == {}
