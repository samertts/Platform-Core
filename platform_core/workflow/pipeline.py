from __future__ import annotations

from collections.abc import Iterable, Iterator

from platform_core.workflow.step import WorkflowStep


class WorkflowPipeline:
    """
    Ordered collection of workflow steps.
    """

    def __init__(
        self,
        steps: Iterable[WorkflowStep] | None = None,
    ) -> None:

        self._steps: list[WorkflowStep] = list(steps or [])

    def add(
        self,
        step: WorkflowStep,
    ) -> WorkflowPipeline:

        self._steps.append(step)

        return self

    @property
    def steps(
        self,
    ) -> tuple[WorkflowStep, ...]:

        return tuple(self._steps)

    def __len__(
        self,
    ) -> int:

        return len(self._steps)

    def __iter__(
        self,
    ) -> Iterator[WorkflowStep]:
        return iter(self._steps)

    def clear(
        self,
    ) -> None:

        self._steps.clear()
