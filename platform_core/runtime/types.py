from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


class RuntimeState(Enum):
    CREATED = "created"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
    DISPOSED = "disposed"


class ServiceType(Enum):
    SINGLETON = "singleton"
    SCOPED = "scoped"
    TRANSIENT = "transient"


class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class EventPriority(Enum):
    LOW = 0
    NORMAL = 50
    HIGH = 75
    CRITICAL = 100


@dataclass(frozen=True)
class Identity:
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    version: str = "0.1.0"
    type: str = "runtime"


@dataclass
class HealthReport:
    status: HealthStatus
    components: dict[str, HealthStatus] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class Event:
    id: UUID = field(default_factory=uuid4)
    type: str = ""
    source: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    priority: EventPriority = EventPriority.NORMAL
    correlation_id: UUID | None = None


@dataclass
class EventResult:
    success: bool
    handler: str = ""
    error: str | None = None
    duration_ms: float = 0.0
