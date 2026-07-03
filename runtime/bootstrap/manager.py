from __future__ import annotations

import asyncio
import logging
import signal
import time
from datetime import UTC, datetime
from typing import Any

from platform_core.runtime.config.engine import ConfigurationEngine
from platform_core.runtime.container.engine import ServiceContainer
from platform_core.runtime.events.engine import EventBus
from platform_core.runtime.identity.engine import IdentityEngine
from platform_core.runtime.kernel.engine import RuntimeKernel
from platform_core.runtime.logging.engine import LoggingEngine
from platform_core.runtime.manifest.loader import ManifestLoader
from platform_core.runtime.plugins.engine import PluginEngine
from platform_core.runtime.policy.engine import PolicyEngine
from platform_core.runtime.sdk.loader import SDKLoader
from platform_core.runtime.telemetry.engine import TelemetryEngine
from platform_core.runtime.types import RuntimeState

logger = logging.getLogger("platform_core.bootstrap")


class BootstrapManager:
    """Orchestrates runtime startup and shutdown sequence."""

    def __init__(self, config_path: str | None = None) -> None:
        self._kernel = RuntimeKernel()
        self._config = ConfigurationEngine()
        self._logging: LoggingEngine | None = None
        self._telemetry: TelemetryEngine | None = None
        self._identity: IdentityEngine | None = None
        self._policy: PolicyEngine | None = None
        self._container = ServiceContainer()
        self._event_bus = EventBus()
        self._plugins = PluginEngine()
        self._manifest_loader = ManifestLoader()
        self._sdk_loader = SDKLoader()
        self._config_path = config_path
        self._startup_log: list[dict[str, Any]] = []
        self._signal_handlers_registered = False

    @property
    def kernel(self) -> RuntimeKernel:
        return self._kernel

    @property
    def config(self) -> ConfigurationEngine:
        return self._config

    @property
    def logging(self) -> LoggingEngine:
        if self._logging is None:
            raise RuntimeError("Logging not initialized")
        return self._logging

    @property
    def telemetry(self) -> TelemetryEngine:
        if self._telemetry is None:
            raise RuntimeError("Telemetry not initialized")
        return self._telemetry

    @property
    def identity(self) -> IdentityEngine:
        if self._identity is None:
            raise RuntimeError("Identity not initialized")
        return self._identity

    @property
    def policy(self) -> PolicyEngine:
        if self._policy is None:
            raise RuntimeError("Policy not initialized")
        return self._policy

    @property
    def container(self) -> ServiceContainer:
        return self._container

    @property
    def event_bus(self) -> EventBus:
        return self._event_bus

    @property
    def plugins(self) -> PluginEngine:
        return self._plugins

    @property
    def manifest_loader(self) -> ManifestLoader:
        return self._manifest_loader

    @property
    def sdk_loader(self) -> SDKLoader:
        return self._sdk_loader

    async def bootstrap(self) -> None:
        start_time = time.monotonic()

        await self._step("Load Configuration", self._load_configuration)
        await self._step("Initialize Logging", self._init_logging)
        await self._step("Initialize Telemetry", self._init_telemetry)
        await self._step("Initialize Identity", self._init_identity)
        await self._step("Initialize Policy Engine", self._init_policy)
        await self._step("Initialize Service Container", self._init_container)
        await self._step("Initialize Event Bus", self._init_event_bus)
        await self._step("Load Plugins", self._load_plugins)
        await self._step("Register Core Services", self._register_core_services)
        await self._step("Load SDKs", self._load_sdks)
        await self._step("Start Runtime Kernel", self._start_kernel)
        await self._step("Register Signal Handlers", self._register_signals)

        total_time = (time.monotonic() - start_time) * 1000
        self._log_step("Bootstrap Complete", f"All steps completed in {total_time:.1f}ms")

    async def _step(self, name: str, func: Any) -> None:
        step_start = time.monotonic()
        try:
            if asyncio.iscoroutinefunction(func):
                await func()
            else:
                func()
            duration = (time.monotonic() - step_start) * 1000
            self._log_step(name, f"OK ({duration:.1f}ms)", "success")
        except Exception as e:
            duration = (time.monotonic() - step_start) * 1000
            self._log_step(name, f"FAILED ({duration:.1f}ms): {e}", "error")
            raise

    def _log_step(self, step: str, message: str, status: str = "info") -> None:
        entry = {
            "step": step,
            "message": message,
            "status": status,
            "timestamp": datetime.now(UTC).isoformat(),
        }
        self._startup_log.append(entry)
        if status == "error":
            logger.error("[%s] %s", step, message)
        else:
            logger.info("[%s] %s", step, message)

    async def _load_configuration(self) -> None:
        sources = []
        if self._config_path:
            sources.append(self._config_path)
        sources.append("PLATFORM_")
        await self._config.load(sources)

    def _init_logging(self) -> None:
        level = self._config.get("logging.level", "INFO")
        output = self._config.get("logging.output", "stdout")
        self._logging = LoggingEngine(level=level, output=output)

    def _init_telemetry(self) -> None:
        self._telemetry = TelemetryEngine()

    def _init_identity(self) -> None:
        name = self._config.get("runtime.name", "platform-core")
        version = self._config.get("runtime.version", "1.0.0")
        self._identity = IdentityEngine(runtime_name=name, runtime_version=version)

    def _init_policy(self) -> None:
        self._policy = PolicyEngine()
        policy_source = self._config.get("policy.source")
        if policy_source:
            self._policy.load_policies(policy_source)

    def _init_container(self) -> None:
        pass

    async def _init_event_bus(self) -> None:
        await self._event_bus.start()

    async def _load_plugins(self) -> None:
        plugin_paths = self._config.get("plugins.paths", [])
        if plugin_paths:
            await self._plugins.discover(plugin_paths)
            for plugin_info in self._plugins.list_plugins():
                if plugin_info["status"] == "discovered":
                    try:
                        await self._plugins.load(plugin_info["id"])
                        await self._plugins.activate(plugin_info["id"])
                    except Exception as e:
                        if self._logging is not None:
                            self._logging.warning(
                                f"Failed to load plugin {plugin_info['id']}: {e}",
                            )

    def _register_core_services(self) -> None:
        self._container.register_instance(ConfigurationEngine, self._config)
        self._container.register_instance(LoggingEngine, self.logging)
        self._container.register_instance(TelemetryEngine, self.telemetry)
        self._container.register_instance(IdentityEngine, self.identity)
        self._container.register_instance(PolicyEngine, self.policy)
        self._container.register_instance(ServiceContainer, self._container)
        self._container.register_instance(EventBus, self._event_bus)
        self._container.register_instance(PluginEngine, self._plugins)
        self._container.register_instance(ManifestLoader, self._manifest_loader)
        self._container.register_instance(SDKLoader, self._sdk_loader)

    async def _load_sdks(self) -> None:
        pass

    async def _start_kernel(self) -> None:
        await self._kernel.start()
        self._kernel.register_health_check(
            "event_bus",
            lambda: {
                "status": "healthy",
                "subscriptions": self._event_bus.subscription_count,
            },
        )
        self._kernel.register_health_check(
            "container",
            lambda: {
                "status": "healthy",
                "services": len(self._container.registered_types),
            },
        )

    def _register_signals(self) -> None:
        if self._signal_handlers_registered:
            return

        def handle_signal(signum: int, frame: Any) -> None:
            logger.info("Received signal %s, initiating shutdown", signum)
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.ensure_future(self.shutdown())
            else:
                loop.run_until_complete(self.shutdown())

        try:
            signal.signal(signal.SIGTERM, handle_signal)
            signal.signal(signal.SIGINT, handle_signal)
            self._signal_handlers_registered = True
        except (OSError, ValueError):
            pass

    async def shutdown(self) -> None:
        if self._kernel.state in (RuntimeState.STOPPED, RuntimeState.DISPOSED):
            return

        self._log_step("Shutdown", "Initiating graceful shutdown")

        await self._event_bus.stop()

        for plugin in reversed(self._plugins.list_plugins()):
            if plugin["status"] == "active":
                try:
                    await self._plugins.deactivate(plugin["id"])
                    await self._plugins.unload(plugin["id"])
                except Exception:
                    pass

        self._container.dispose()
        await self._kernel.stop()

        if self._telemetry:
            self._telemetry.flush()

        self._log_step("Shutdown", "Shutdown complete")

    def get_startup_log(self) -> list[dict[str, Any]]:
        return list(self._startup_log)

    def get_info(self) -> dict[str, Any]:
        return {
            "kernel": self._kernel.get_info(),
            "config_loaded": self._config.loaded,
            "services_registered": self._container.registered_types,
            "event_bus_stats": self._event_bus.stats,
            "plugins": self._plugins.list_plugins(),
            "sdks": self._sdk_loader.list_sdks(),
            "startup_log": self._startup_log,
        }
