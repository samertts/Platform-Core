from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from platform_core.engine.cancellation import CancellationToken


@dataclass(frozen=True, slots=True)
class EngineContext:
    """
    Immutable execution context.

    See:
        ENGINE_SPEC.md
        E-010
    """

    execution_id: UUID

    execution_mode: str

    cancellation_token: CancellationToken

    correlation_id: UUID | None = None

    deadline: datetime | None = None

    metadata: Mapping[str, str] = field(default_factory=dict)

    tags: tuple[str, ...] = field(default_factory=tuple)
