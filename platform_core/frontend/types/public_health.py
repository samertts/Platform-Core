"""
Public Health domain types for NHDOS Frontend
"""

from dataclasses import dataclass

from .base import BaseEntity


@dataclass
class Vaccine(BaseEntity):
    """Vaccine record."""

    name: str = ""
    vaccine_type: str = ""
    manufacturer: str = ""
    dose_number: int = 1
    required_doses: int = 1
    interval_days: int | None = None
    storage_temperature: str | None = None
    status: str = "active"


@dataclass
class Immunization(BaseEntity):
    """Immunization record."""

    patient_id: str = ""
    vaccine_id: str = ""
    administration_date: str = ""
    dose_number: int = 1
    lot_number: str | None = None
    expiry_date: str | None = None
    site: str | None = None
    route: str | None = None
    administered_by: str | None = None
    facility_id: str = ""
    status: str = "completed"


@dataclass
class ResearchStudy(BaseEntity):
    """Research study record."""

    title: str = ""
    description: str | None = None
    study_type: str = ""
    principal_investigator_id: str | None = None
    facility_id: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    status: str = "planning"
    participants_count: int = 0
    ethical_approval_status: str = "pending"
