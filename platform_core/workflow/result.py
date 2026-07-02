from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from platform_core.workflow.status import WorkflowStatus


@dataclass(frozen=True, slots=True)
class WorkflowResult:
    status: WorkflowStatus

    message: str = ""

    data: dict[str, Any] = field(default_factory=dict)

    @property
    def success(self) -> bool:

        return self.status is WorkflowStatus.COMPLETED

    @property
    def failed(self) -> bool:

        return self.status is WorkflowStatus.FAILED

    @classmethod
    def ok(
        cls,
        **data: Any,
    ) -> WorkflowResult:

        return cls(
            status=WorkflowStatus.COMPLETED,
            data=data,
        )

    @classmethod
    def error(
        cls,
        message: str,
        **data: Any,
    ) -> WorkflowResult:

        return cls(
            status=WorkflowStatus.FAILED,
            message=message,
            data=data,
        )
