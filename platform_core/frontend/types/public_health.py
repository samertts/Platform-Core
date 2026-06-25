"""
Public Health domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Optional
from .base import BaseEntity


@dataclass
class Vaccine(BaseEntity):
    """Vaccine record."""
    name: str = ""
    vaccine_type: str = ""
    manufacturer: str = ""
    dose_number: int = 1
    required_doses: int = 1
    interval_days: Optional[int] = None
    storage_temperature: Optional[str] = None
    status: str = "active"


@dataclass
class Immunization(BaseEntity):
    """Immunization record."""
    patient_id: str = ""
    vaccine_id: str = ""
    administration_date: str = ""
    dose_number: int = 1
    lot_number: Optional[str] = None
    expiry_date: Optional[str] = None
    site: Optional[str] = None
    route: Optional[str] = None
    administered_by: Optional[str] = None
    facility_id: str = ""
    status: str = "completed"


@dataclass
class ResearchStudy(BaseEntity):
    """Research study record."""
    title: str = ""
    description: Optional[str] = None
    study_type: str = ""
    principal_investigator_id: Optional[str] = None
    facility_id: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: str = "planning"
    participants_count: int = 0
    ethical_approval_status: str = "pending"
