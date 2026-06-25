"""
Base entity client for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Any, Optional, TypeVar, Generic
from .client import APIClient

T = TypeVar("T")


@dataclass
class BaseEntityClient(Generic[T]):
    """Base client for entity CRUD operations."""
    client: APIClient
    entity_name: str = ""
    endpoint: str = ""

    def list(self, page: int = 1, page_size: int = 20, filters: Optional[dict] = None) -> dict:
        params = {"page": page, "page_size": page_size}
        if filters:
            params.update(filters)
        return self.client.get(self.endpoint, params=params)

    def get(self, entity_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/{entity_id}")

    def create(self, data: dict) -> dict:
        return self.client.post(self.endpoint, data=data)

    def update(self, entity_id: str, data: dict) -> dict:
        return self.client.put(f"{self.endpoint}/{entity_id}", data=data)

    def delete(self, entity_id: str) -> dict:
        return self.client.delete(f"{self.endpoint}/{entity_id}")

    def search(self, query: str, filters: Optional[dict] = None) -> dict:
        params = {"q": query}
        if filters:
            params.update(filters)
        return self.client.get(f"{self.endpoint}/search", params=params)
