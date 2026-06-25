"""
Supply Chain domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Optional
from .base import BaseEntity


@dataclass
class InventoryItem(BaseEntity):
    """Inventory item record."""
    facility_id: str = ""
    item_code: str = ""
    name: str = ""
    description: Optional[str] = None
    category: str = ""
    unit_of_measure: str = ""
    current_quantity: int = 0
    reorder_level: int = 0
    maximum_level: Optional[int] = None
    location: Optional[str] = None
    status: str = "active"


@dataclass
class Supplier(BaseEntity):
    """Supplier record."""
    name: str = ""
    supplier_type: str = ""
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    rating: Optional[float] = None
    status: str = "active"


@dataclass
class Purchase(BaseEntity):
    """Purchase order record."""
    facility_id: str = ""
    supplier_id: str = ""
    purchase_order_number: str = ""
    order_date: str = ""
    expected_delivery_date: Optional[str] = None
    total_amount: float = 0.0
    currency: str = "IQD"
    status: str = "pending"
    items: list[dict] = field(default_factory=list)
