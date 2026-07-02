from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class WorkflowContext:
    """
    Shared mutable context passed between workflow steps.
    """

    data: dict[str, Any] = field(default_factory=dict)

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.data.get(
            key,
            default,
        )

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.data[key] = value

    def exists(
        self,
        key: str,
    ) -> bool:

        return key in self.data

    def clear(self) -> None:

        self.data.clear()
