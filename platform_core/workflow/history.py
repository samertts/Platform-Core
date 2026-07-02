from __future__ import annotations

from platform_core.workflow.result import WorkflowResult


class WorkflowHistory:
    def __init__(self) -> None:

        self._items: list[WorkflowResult] = []

    def add(
        self,
        result: WorkflowResult,
    ) -> None:

        self._items.append(result)

    def clear(
        self,
    ) -> None:

        self._items.clear()

    @property
    def items(
        self,
    ) -> tuple[WorkflowResult, ...]:

        return tuple(self._items)

    def __len__(
        self,
    ) -> int:

        return len(self._items)
