"""
Supply Chain domain types for NHDOS Frontend
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base import BaseEntity


@dataclass
class InventoryItem(BaseEntity):
    """Inventory item record."""

    facility_id: str = ""
    item_code: str = ""
    name: str = ""
    description: str | None = None
    category: str = ""
    unit_of_measure: str = ""
    current_quantity: int = 0
    reorder_level: int = 0
    maximum_level: int | None = None
    location: str | None = None
    status: str = "active"


@dataclass
class Supplier(BaseEntity):
    """Supplier record."""

    name: str = ""
    supplier_type: str = ""
    contact_person: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    rating: float | None = None
    status: str = "active"


@dataclass
class Purchase(BaseEntity):
    """Purchase order record."""

    facility_id: str = ""
    supplier_id: str = ""
    purchase_order_number: str = ""
    order_date: str = ""
    expected_delivery_date: str | None = None
    total_amount: float = 0.0
    currency: str = "IQD"
    status: str = "pending"
    items: list[dict[str, Any]] = field(default_factory=list)
