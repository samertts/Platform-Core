"""
Pharmacy domain types for NHDOS Frontend
"""

from dataclasses import dataclass

from .base import BaseEntity


@dataclass
class Prescription(BaseEntity):
    """Prescription record."""

    patient_id: str = ""
    encounter_id: str | None = None
    prescribing_provider_id: str = ""
    facility_id: str = ""
    medication_id: str = ""
    dosage: str = ""
    frequency: str = ""
    duration: str | None = None
    quantity: int = 1
    refills: int = 0
    instructions: str | None = None
    status: str = "active"


@dataclass
class Medication(BaseEntity):
    """Medication record."""

    name: str = ""
    generic_name: str | None = None
    manufacturer: str = ""
    ndc_code: str | None = None
    dosage_form: str = ""
    strength: str = ""
    category: str | None = None
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
    lot_number: str | None = None
    expiry_date: str | None = None
    status: str = "dispensed"
