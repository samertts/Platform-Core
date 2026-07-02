"""
Platform-Core Engineering Intelligence

Shared base classes.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Any


@dataclass(slots=True)
class EngineeringObject:
    """
    Root object for all engineering domain models.
    """

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def field_names(self) -> tuple[str, ...]:
        return tuple(field.name for field in fields(self))

    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def copy(self):
        cls = type(self)
        return cls(**self.to_dict())

    def __repr__(self) -> str:
        values = ", ".join(f"{name}={getattr(self, name)!r}" for name in self.field_names())
        return f"{self.__class__.__name__}({values})"
