"""
Workflow API client for NHDOS Frontend
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .base import BaseEntityClient
from .client import APIClient


@dataclass
class WorkflowClient(BaseEntityClient[Any]):
    """Client for Workflow entity API."""

    client: APIClient
    entity_name: str = "workflow"
    endpoint: str = "workflows"

    def get_by_type(self, workflow_type: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/type/{workflow_type}")

    def start(self, workflow_id: str, context: dict[str, Any]) -> dict[str, Any]:
        return self.client.post(f"{self.endpoint}/{workflow_id}/start", data=context)

    def complete(self, workflow_id: str) -> dict[str, Any]:
        return self.client.put(f"{self.endpoint}/{workflow_id}/complete")

    def get_status(self, workflow_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/{workflow_id}/status")


@dataclass
class WorkflowStepClient(BaseEntityClient[Any]):
    """Client for WorkflowStep entity API."""

    client: APIClient
    entity_name: str = "workflow_step"
    endpoint: str = "workflow-steps"

    def get_by_workflow(self, workflow_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/workflow/{workflow_id}")

    def complete(self, step_id: str, result: dict[str, Any]) -> dict[str, Any]:
        return self.client.put(f"{self.endpoint}/{step_id}/complete", data=result)

    def skip(self, step_id: str, reason: str) -> dict[str, Any]:
        return self.client.put(f"{self.endpoint}/{step_id}/skip", data={"reason": reason})


@dataclass
class TaskClient(BaseEntityClient[Any]):
    """Client for Task entity API."""

    client: APIClient
    entity_name: str = "task"
    endpoint: str = "tasks"

    def get_by_workflow(self, workflow_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/workflow/{workflow_id}")

    def get_by_assignee(self, assignee_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/assignee/{assignee_id}")

    def assign(self, task_id: str, assignee_id: str) -> dict[str, Any]:
        return self.client.put(
            f"{self.endpoint}/{task_id}/assign", data={"assignee_id": assignee_id}
        )

    def complete(self, task_id: str) -> dict[str, Any]:
        return self.client.put(f"{self.endpoint}/{task_id}/complete")

    def get_pending(self, assignee_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/pending", params={"assignee_id": assignee_id})
