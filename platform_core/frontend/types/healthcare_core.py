"""
Healthcare Core domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Optional

from .base import BaseEntity


@dataclass
class Patient(BaseEntity):
    """Patient record linking citizen to healthcare."""

    citizen_id: str = ""
    medical_record_number: str = ""
    facility_id: Optional[str] = None
    primary_care_provider_id: Optional[str] = None
    blood_type: Optional[str] = None
    allergies: list[str] = field(default_factory=list)
    chronic_conditions: list[str] = field(default_factory=list)
    status: str = "active"
    confidentiality_level: int = 5


@dataclass
class Visit(BaseEntity):
    """Patient visit to facility."""

    patient_id: str = ""
    facility_id: str = ""
    department_id: Optional[str] = None
    visit_type: str = ""
    reason: Optional[str] = None
    status: str = "active"
    started_at: Optional[str] = None
    ended_at: Optional[str] = None


@dataclass
class Encounter(BaseEntity):
    """Clinical encounter within a visit."""

    visit_id: str = ""
    patient_id: str = ""
    encounter_type: str = ""
    chief_complaint: Optional[str] = None
    assessment: Optional[str] = None
    plan: Optional[str] = None
    status: str = "active"
    started_at: Optional[str] = None
    ended_at: Optional[str] = None


@dataclass
class Appointment(BaseEntity):
    """Scheduled appointment."""

    patient_id: str = ""
    facility_id: str = ""
    department_id: Optional[str] = None
    provider_id: Optional[str] = None
    appointment_type: str = ""
    scheduled_date: str = ""
    scheduled_time: str = ""
    duration_minutes: int = 30
    reason: Optional[str] = None
    status: str = "scheduled"


@dataclass
class Admission(BaseEntity):
    """Hospital admission record."""

    patient_id: str = ""
    facility_id: str = ""
    admission_type: str = ""
    admission_date: str = ""
    department_id: Optional[str] = None
    bed_id: Optional[str] = None
    admitting_diagnosis: Optional[str] = None
    status: str = "active"


@dataclass
class Discharge(BaseEntity):
    """Hospital discharge record."""

    admission_id: str = ""
    patient_id: str = ""
    discharge_date: str = ""
    discharge_type: str = ""
    discharge_diagnosis: Optional[str] = None
    discharge_instructions: Optional[str] = None
    follow_up_date: Optional[str] = None
    status: str = "completed"
