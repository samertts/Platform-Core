from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from platform_core.workflow.context import WorkflowContext
from platform_core.workflow.result import WorkflowResult


class WorkflowStep(ABC):
    """
    Base class for every workflow step.
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult:
        """
        Execute this workflow step.
        """
        raise NotImplementedError
