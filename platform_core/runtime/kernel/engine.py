from __future__ import annotations

import asyncio
import signal
import threading
from datetime import datetime, timezone
from typing import Any

from platform_core.runtime.types import (HealthReport, HealthStatus,
                                         RuntimeState)


class RuntimeKernel:
    """Runtime lifecycle management — startup, shutdown, health, state."""

    def __init__(self, name: str = "platform-core", version: str = "1.0.0") -> None:
        self._name = name
        self._version = version
        self._state = RuntimeState.CREATED
        self._started_at: datetime | None = None
        self._stopped_at: datetime | None = None
        self._health_checks: dict[str, Any] = {}
        self._shutdown_hooks: list[Any] = []
        self._state_listeners: list[Any] = []
        self._lock = threading.RLock()
        self._ready = asyncio.Event()

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def state(self) -> RuntimeState:
        return self._state

    @property
    def is_running(self) -> bool:
        return self._state == RuntimeState.RUNNING

    @property
    def uptime_seconds(self) -> float | None:
        if self._started_at is None:
            return None
        end = self._stopped_at or datetime.now(timezone.utc)
        return (end - self._started_at).total_seconds()

    def _set_state(self, new_state: RuntimeState) -> None:
        with self._lock:
            old_state = self._state
            self._state = new_state

        for listener in self._state_listeners:
            try:
                listener(old_state, new_state)
            except Exception:
                pass

    def on_state_change(self, listener: Any) -> None:
        with self._lock:
            self._state_listeners.append(listener)

    def register_health_check(self, name: str, check: Any) -> None:
        self._health_checks[name] = check

    def register_shutdown_hook(self, hook: Any) -> None:
        with self._lock:
            self._shutdown_hooks.append(hook)

    async def start(self) -> None:
        if self._state != RuntimeState.CREATED:
            raise RuntimeError(f"Cannot start runtime in state {self._state.value}")

        self._set_state(RuntimeState.STARTING)
        self._started_at = datetime.now(timezone.utc)

        try:
            self._set_state(RuntimeState.RUNNING)
            self._ready.set()
        except Exception as e:
            self._set_state(RuntimeState.ERROR)
            raise RuntimeError(f"Runtime start failed: {e}") from e

    async def stop(self) -> None:
        if self._state not in (RuntimeState.RUNNING, RuntimeState.ERROR):
            return

        self._set_state(RuntimeState.STOPPING)

        for hook in reversed(self._shutdown_hooks):
            try:
                if asyncio.iscoroutinefunction(hook):
                    await hook()
                else:
                    hook()
            except Exception:
                pass

        self._stopped_at = datetime.now(timezone.utc)
        self._set_state(RuntimeState.STOPPED)

    async def ready(self) -> None:
        await self._ready.wait()

    async def health_check(self) -> HealthReport:
        components: dict[str, HealthStatus] = {}
        all_healthy = True

        for name, check in self._health_checks.items():
            try:
                if asyncio.iscoroutinefunction(check):
                    result = await check()
                else:
                    result = check()

                if isinstance(result, dict):
                    status_str = result.get("status", "healthy")
                    status = (
                        HealthStatus.HEALTHY
                        if status_str == "healthy"
                        else (
                            HealthStatus.DEGRADED
                            if status_str == "degraded"
                            else HealthStatus.UNHEALTHY
                        )
                    )
                elif isinstance(result, HealthStatus):
                    status = result
                else:
                    status = HealthStatus.HEALTHY

                components[name] = status
                if status != HealthStatus.HEALTHY:
                    all_healthy = False
            except Exception:
                components[name] = HealthStatus.UNHEALTHY
                all_healthy = False

        overall = (
            HealthStatus.HEALTHY
            if all_healthy
            else HealthStatus.DEGRADED if components else HealthStatus.HEALTHY
        )

        return HealthReport(
            status=overall,
            components=components,
            timestamp=datetime.now(timezone.utc),
            details={
                "name": self._name,
                "version": self._version,
                "uptime_seconds": self.uptime_seconds,
            },
        )

    def get_info(self) -> dict[str, Any]:
        return {
            "name": self._name,
            "version": self._version,
            "state": self._state.value,
            "started_at": self._started_at.isoformat() if self._started_at else None,
            "stopped_at": self._stopped_at.isoformat() if self._stopped_at else None,
            "uptime_seconds": self.uptime_seconds,
            "health_checks": list(self._health_checks.keys()),
            "shutdown_hooks": len(self._shutdown_hooks),
        }
