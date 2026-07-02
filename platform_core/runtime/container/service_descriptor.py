from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .lifetime import Lifetime


@dataclass(slots=True)
class ServiceDescriptor:
    interface: type

    implementation: type | Callable[..., Any]

    lifetime: Lifetime

    instance: Any = None
