from __future__ import annotations

import pytest

from platform_core.runtime.bootstrap.manager import BootstrapManager
from platform_core.runtime.types import Event, EventResult, RuntimeState


class TestRuntimeIntegration:
    """Integration tests for the complete Platform Runtime."""

    @pytest.mark.asyncio
    async def test_full_lifecycle(self) -> None:
        manager = BootstrapManager()
        await manager.bootstrap()

        assert manager.kernel.is_running
        assert manager.config.loaded

        manager.logging.info("Integration test log")
        manager.telemetry.counter("integration.test", 1.0)

        identity = manager.identity
        module_id = identity.register_module("test-module", "1.0.0")
        assert module_id.name == "test-module"

        event = Event(type="integration.test", source="test", data={"key": "value"})
        await manager.event_bus.publish(event)
        assert manager.event_bus.stats["published"] == 1

        await manager.shutdown()
        assert manager.kernel.state == RuntimeState.STOPPED

    @pytest.mark.asyncio
    async def test_container_with_all_services(self) -> None:
        manager = BootstrapManager()
        await manager.bootstrap()

        container = manager.container
        types = container.registered_types
        assert "ConfigurationEngine" in types
        assert "LoggingEngine" in types
        assert "TelemetryEngine" in types
        assert "EventBus" in types

        await manager.shutdown()

    @pytest.mark.asyncio
    async def test_event_bus_integration(self) -> None:
        manager = BootstrapManager()
        await manager.bootstrap()

        received: list[Event] = []

        class TestHandler:
            async def handle(self, event: Event) -> EventResult:
                received.append(event)
                return EventResult(success=True, handler="TestHandler")

        manager.event_bus.subscribe("test.integration", TestHandler())
        event = Event(type="test.integration", source="integration-test")
        await manager.event_bus.publish(event)

        assert len(received) == 1
        assert received[0].type == "test.integration"

        await manager.shutdown()

    @pytest.mark.asyncio
    async def test_health_check_integration(self) -> None:
        manager = BootstrapManager()
        await manager.bootstrap()

        report = await manager.kernel.health_check()
        assert report.status.value in ("healthy", "degraded")

        await manager.shutdown()
