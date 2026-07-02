"""
Pharmacy domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Optional

from .base import BaseEntity


@dataclass
class Prescription(BaseEntity):
    """Prescription record."""

    patient_id: str = ""
    encounter_id: Optional[str] = None
    prescribing_provider_id: str = ""
    facility_id: str = ""
    medication_id: str = ""
    dosage: str = ""
    frequency: str = ""
    duration: Optional[str] = None
    quantity: int = 1
    refills: int = 0
    instructions: Optional[str] = None
    status: str = "active"


@dataclass
class Medication(BaseEntity):
    """Medication record."""

    name: str = ""
    generic_name: Optional[str] = None
    manufacturer: str = ""
    ndc_code: Optional[str] = None
    dosage_form: str = ""
    strength: str = ""
    category: Optional[str] = None
    controlled_substance: bool = False
    stock_quantity: int = 0
    reorder_level: int = 10


@dataclass
class Dispensing(BaseEntity):
    """Medication dispensing record."""

    prescription_id: str = ""
    patient_id: str = ""
    medication_id: str = ""
    pharmacist_id: str = ""
    facility_id: str = ""
    quantity_dispensed: int = 0
    lot_number: Optional[str] = None
    expiry_date: Optional[str] = None
    status: str = "dispensed"
