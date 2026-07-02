from __future__ import annotations


class WorkflowError(Exception):
    """Base workflow exception."""


class WorkflowExecutionError(WorkflowError):
    """Workflow execution failed."""


class WorkflowValidationError(WorkflowError):
    """Workflow validation failed."""
