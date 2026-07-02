"""
Platform Runtime package.

Keep this package lightweight to avoid circular imports.
Objects are imported lazily on first access.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "Runtime",
]


def __getattr__(name: str) -> Any:
    if name == "Runtime":
        from .runtime import Runtime

        return Runtime

    raise AttributeError(
        f"module {__name__!r} has no attribute {name!r}"
    )
