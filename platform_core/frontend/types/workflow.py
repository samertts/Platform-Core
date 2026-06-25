"""
Workflow domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Optional
from .base import BaseEntity


@dataclass
class Workflow(BaseEntity):
    """Workflow definition."""
    name: str = ""
    description: Optional[str] = None
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
    assigned_role: Optional[str] = None
    timeout_hours: Optional[int] = None
    status: str = "active"


@dataclass
class Task(BaseEntity):
    """Task record."""
    workflow_id: str = ""
    step_id: Optional[str] = None
    title: str = ""
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[str] = None
    priority: str = "medium"
    status: str = "pending"
    completed_at: Optional[str] = None
