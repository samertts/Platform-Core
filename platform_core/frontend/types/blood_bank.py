"""
Blood Bank domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Optional

from .base import BaseEntity


@dataclass
class Donation(BaseEntity):
    """Blood donation record."""

    donor_id: str = ""
    donation_date: str = ""
    facility_id: str = ""
    donation_type: str = ""
    volume_ml: int = 0
    hemoglobin_level: Optional[float] = None
    blood_pressure: Optional[str] = None
    status: str = "completed"


@dataclass
class BloodUnit(BaseEntity):
    """Blood unit record."""

    donation_id: str = ""
    blood_type: str = ""
    component_type: str = ""
    volume_ml: int = 0
    collection_date: str = ""
    expiry_date: str = ""
    storage_location: Optional[str] = None
    status: str = "available"
    crossmatch_compatibility: list[str] = field(default_factory=list)


@dataclass
class Transfusion(BaseEntity):
    """Blood transfusion record."""

    patient_id: str = ""
    blood_unit_id: str = ""
    transfusion_date: str = ""
    performing_provider_id: str = ""
    facility_id: str = ""
    indication: Optional[str] = None
    volume_transfused: int = 0
    reaction: Optional[str] = None
    status: str = "completed"
