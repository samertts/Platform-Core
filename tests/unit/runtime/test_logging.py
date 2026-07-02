from __future__ import annotations

from uuid import uuid4

from platform_core.runtime.logging.engine import LoggingEngine


class TestLoggingEngine:
    def test_init(self) -> None:
        engine = LoggingEngine(level="DEBUG")
        assert engine is not None

    def test_log_levels(self) -> None:
        engine = LoggingEngine(level="DEBUG")
        engine.debug("debug message")
        engine.info("info message")
        engine.warning("warning message")
        engine.error("error message")
        engine.critical("critical message")

    def test_log_with_context(self) -> None:
        engine = LoggingEngine()
        engine.info("test message", key="value", count=42)

    def test_with_correlation(self) -> None:
        engine = LoggingEngine()
        correlation_id = uuid4()
        correlated = engine.with_correlation(correlation_id)
        correlated.info("correlated message")

    def test_with_context(self) -> None:
        engine = LoggingEngine()
        contextual = engine.with_context(user="test", action="login")
        contextual.info("contextual message")

    def test_audit(self) -> None:
        engine = LoggingEngine()
        engine.audit(
            action="login",
            subject="user@example.com",
            actor="admin",
            result="success",
        )
        entries = engine.get_audit_entries()
        assert len(entries) == 1
        assert entries[0]["action"] == "login"

    def test_get_log_entries(self) -> None:
        engine = LoggingEngine()
        engine.info("entry 1")
        engine.info("entry 2")
        entries = engine.get_log_entries()
        assert len(entries) >= 2
