"""
Supply Chain API client for NHDOS Frontend
"""

from dataclasses import dataclass
from .base import BaseEntityClient
from .client import APIClient


@dataclass
class InventoryItemClient(BaseEntityClient):
    """Client for InventoryItem entity API."""
    client: APIClient
    entity_name: str = "inventory_item"
    endpoint: str = "inventory-items"

    def get_by_facility(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/facility/{facility_id}")

    def get_low_stock(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/low-stock", params={"facility_id": facility_id})

    def update_quantity(self, item_id: str, quantity: int) -> dict:
        return self.client.put(f"{self.endpoint}/{item_id}/quantity", data={"quantity": quantity})

    def search(self, query: str) -> dict:
        return self.client.get(f"{self.endpoint}/search", params={"q": query})


@dataclass
class SupplierClient(BaseEntityClient):
    """Client for Supplier entity API."""
    client: APIClient
    entity_name: str = "supplier"
    endpoint: str = "suppliers"

    def get_by_type(self, supplier_type: str) -> dict:
        return self.client.get(f"{self.endpoint}/type/{supplier_type}")

    def get_rated(self, min_rating: float) -> dict:
        return self.client.get(f"{self.endpoint}/rated", params={"min_rating": min_rating})


@dataclass
class PurchaseClient(BaseEntityClient):
    """Client for Purchase entity API."""
    client: APIClient
    entity_name: str = "purchase"
    endpoint: str = "purchases"

    def get_by_facility(self, facility_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/facility/{facility_id}")

    def get_by_supplier(self, supplier_id: str) -> dict:
        return self.client.get(f"{self.endpoint}/supplier/{supplier_id}")

    def receive(self, purchase_id: str, items: list[dict]) -> dict:
        return self.client.put(f"{self.endpoint}/{purchase_id}/receive", data={"items": items})

    def cancel(self, purchase_id: str, reason: str) -> dict:
        return self.client.put(f"{self.endpoint}/{purchase_id}/cancel", data={"reason": reason})
