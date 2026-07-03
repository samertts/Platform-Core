"""
Supply Chain API client for NHDOS Frontend
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .base import BaseEntityClient
from .client import APIClient


@dataclass
class InventoryItemClient(BaseEntityClient[Any]):
    """Client for InventoryItem entity API."""

    client: APIClient
    entity_name: str = "inventory_item"
    endpoint: str = "inventory-items"

    def get_by_facility(self, facility_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/facility/{facility_id}")

    def get_low_stock(self, facility_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/low-stock", params={"facility_id": facility_id})

    def update_quantity(self, item_id: str, quantity: int) -> dict[str, Any]:
        return self.client.put(f"{self.endpoint}/{item_id}/quantity", data={"quantity": quantity})

    def search(self, query: str, filters: dict[str, Any] | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"q": query}
        if filters:
            params.update(filters)
        return self.client.get(f"{self.endpoint}/search", params=params)


@dataclass
class SupplierClient(BaseEntityClient[Any]):
    """Client for Supplier entity API."""

    client: APIClient
    entity_name: str = "supplier"
    endpoint: str = "suppliers"

    def get_by_type(self, supplier_type: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/type/{supplier_type}")

    def get_rated(self, min_rating: float) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/rated", params={"min_rating": min_rating})


@dataclass
class PurchaseClient(BaseEntityClient[Any]):
    """Client for Purchase entity API."""

    client: APIClient
    entity_name: str = "purchase"
    endpoint: str = "purchases"

    def get_by_facility(self, facility_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/facility/{facility_id}")

    def get_by_supplier(self, supplier_id: str) -> dict[str, Any]:
        return self.client.get(f"{self.endpoint}/supplier/{supplier_id}")

    def receive(self, purchase_id: str, items: list[dict[str, Any]]) -> dict[str, Any]:
        return self.client.put(f"{self.endpoint}/{purchase_id}/receive", data={"items": items})

    def cancel(self, purchase_id: str, reason: str) -> dict[str, Any]:
        return self.client.put(f"{self.endpoint}/{purchase_id}/cancel", data={"reason": reason})
