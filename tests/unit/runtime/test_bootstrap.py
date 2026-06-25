from __future__ import annotations

import pytest

from platform_core.runtime.bootstrap.manager import BootstrapManager


class TestBootstrapManager:
    def test_init(self) -> None:
        manager = BootstrapManager()
        assert manager.kernel is not None
        assert manager.config is not None
        assert manager.container is not None
        assert manager.event_bus is not None
        assert manager.plugins is not None
        assert manager.manifest_loader is not None
        assert manager.sdk_loader is not None

    @pytest.mark.asyncio
    async def test_bootstrap(self) -> None:
        manager = BootstrapManager()
        await manager.bootstrap()
        assert manager.kernel.is_running
        await manager.shutdown()

    @pytest.mark.asyncio
    async def test_bootstrap_and_shutdown(self) -> None:
        manager = BootstrapManager()
        await manager.bootstrap()
        assert manager.kernel.is_running
        await manager.shutdown()

    def test_get_startup_log(self) -> None:
        manager = BootstrapManager()
        log = manager.get_startup_log()
        assert isinstance(log, list)

    def test_get_info(self) -> None:
        manager = BootstrapManager()
        info = manager.get_info()
        assert "kernel" in info
        assert "config_loaded" in info
        assert "services_registered" in info
        assert "event_bus_stats" in info

    @pytest.mark.asyncio
    async def test_logging_access(self) -> None:
        manager = BootstrapManager()
        await manager.bootstrap()
        logger = manager.logging
        logger.info("test message")
        await manager.shutdown()

    @pytest.mark.asyncio
    async def test_telemetry_access(self) -> None:
        manager = BootstrapManager()
        await manager.bootstrap()
        telemetry = manager.telemetry
        telemetry.counter("test.counter", 1.0)
        await manager.shutdown()

    @pytest.mark.asyncio
    async def test_identity_access(self) -> None:
        manager = BootstrapManager()
        await manager.bootstrap()
        identity = manager.identity
        assert identity.runtime_identity.name == "platform-core"
        await manager.shutdown()

    @pytest.mark.asyncio
    async def test_policy_access(self) -> None:
        manager = BootstrapManager()
        await manager.bootstrap()
        policy = manager.policy
        assert policy.get_active_policies() == []
        await manager.shutdown()
