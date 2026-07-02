"""
Workflow domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field

from .base import BaseEntity


@dataclass
class Workflow(BaseEntity):
    """Workflow definition."""

    name: str = ""
    description: str | None = None
    workflow_type: str = ""
    version: str = "1.0.0"
    status: str = "active"
    steps: list[str] = field(default_factory=list)


@dataclass
class WorkflowStep(BaseEntity):
    """Workflow step definition."""

    workflow_id: str = ""
    step_name: str = ""
    step_order: int = 0
    step_type: str = ""
    assigned_role: str | None = None
    timeout_hours: int | None = None
    status: str = "active"


@dataclass
class Task(BaseEntity):
    """Task record."""

    workflow_id: str = ""
    step_id: str | None = None
    title: str = ""
    description: str | None = None
    assigned_to: str | None = None
    due_date: str | None = None
    priority: str = "medium"
    status: str = "pending"
    completed_at: str | None = None
