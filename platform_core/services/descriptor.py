from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from platform_core.services.lifetime import ServiceLifetime


@dataclass(frozen=True, slots=True)
class ServiceDescriptor:
    """
    Immutable description of a registered service.
    """

    key: str

    implementation: type[Any]

    lifetime: ServiceLifetime = ServiceLifetime.SINGLETON
