"""
Base entity client for NHDOS Frontend
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from .client import APIClient

T = TypeVar("T")


@dataclass
class BaseEntityClient(Generic[T]):
    """Base client for entity CRUD operations."""

    client: APIClient
    entity_name: str = ""
    endpoint: str = ""

    def list(
        self, page: int = 1, page_size: int = 20, filters: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if filters:
            params.update(filters)
        return self.client.get(self.endpoint, params=params)

    def get(self, entity_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/{entity_id}")

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self.client.post(self.endpoint, data=data)

    def update(self, entity_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self.client.put(f"{self.endpoint}/{entity_id}", data=data)

    def delete(self, entity_id: str) -> dict[str, Any]:
        return self.client.delete(f"{self.endpoint}/{entity_id}")

    def search(self, query: str, filters: dict[str, Any] | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"q": query}
        if filters:
            params.update(filters)
        return self.client.get(f"{self.endpoint}/search", params=params)
