from __future__ import annotations

import asyncio

import pytest

from platform_core.runtime.kernel.engine import RuntimeKernel
from platform_core.runtime.types import RuntimeState, HealthStatus


class TestRuntimeKernel:
    @pytest.mark.asyncio
    async def test_lifecycle(self) -> None:
        kernel = RuntimeKernel(name="test", version="1.0.0")
        assert kernel.state == RuntimeState.CREATED
        assert kernel.name == "test"
        assert kernel.version == "1.0.0"

        await kernel.start()
        assert kernel.state == RuntimeState.RUNNING
        assert kernel.is_running
        assert kernel.uptime_seconds is not None

        await kernel.stop()
        assert kernel.state == RuntimeState.STOPPED

    @pytest.mark.asyncio
    async def test_health_check(self) -> None:
        kernel = RuntimeKernel()
        await kernel.start()
        report = await kernel.health_check()
        assert report.status == HealthStatus.HEALTHY
        await kernel.stop()

    @pytest.mark.asyncio
    async def test_health_check_with_component(self) -> None:
        kernel = RuntimeKernel()
        kernel.register_health_check(
            "test", lambda: {"status": "healthy"}
        )
        await kernel.start()
        report = await kernel.health_check()
        assert "test" in report.components
        await kernel.stop()

    @pytest.mark.asyncio
    async def test_health_check_failing_component(self) -> None:
        kernel = RuntimeKernel()
        kernel.register_health_check(
            "failing", lambda: (_ for _ in ()).throw(RuntimeError("fail"))
        )
        await kernel.start()
        report = await kernel.health_check()
        assert report.components["failing"] == HealthStatus.UNHEALTHY
        await kernel.stop()

    def test_state_change_listener(self) -> None:
        kernel = RuntimeKernel()
        changes: list[tuple[str, str]] = []
        kernel.on_state_change(lambda o, n: changes.append((o.value, n.value)))
        kernel._set_state(RuntimeState.STARTING)
        assert len(changes) == 1
        assert changes[0] == ("created", "starting")

    @pytest.mark.asyncio
    async def test_shutdown_hook(self) -> None:
        kernel = RuntimeKernel()
        hook_called = []
        kernel.register_shutdown_hook(lambda: hook_called.append(True))
        await kernel.start()
        await kernel.stop()
        assert len(hook_called) == 1

    def test_get_info(self) -> None:
        kernel = RuntimeKernel(name="test", version="2.0.0")
        info = kernel.get_info()
        assert info["name"] == "test"
        assert info["version"] == "2.0.0"
        assert info["state"] == "created"
