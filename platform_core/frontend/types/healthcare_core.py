"""
Healthcare Core domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field

from .base import BaseEntity


@dataclass
class Patient(BaseEntity):
    """Patient record linking citizen to healthcare."""

    citizen_id: str = ""
    medical_record_number: str = ""
    facility_id: str | None = None
    primary_care_provider_id: str | None = None
    blood_type: str | None = None
    allergies: list[str] = field(default_factory=list)
    chronic_conditions: list[str] = field(default_factory=list)
    status: str = "active"
    confidentiality_level: int = 5


@dataclass
class Visit(BaseEntity):
    """Patient visit to facility."""

    patient_id: str = ""
    facility_id: str = ""
    department_id: str | None = None
    visit_type: str = ""
    reason: str | None = None
    status: str = "active"
    started_at: str | None = None
    ended_at: str | None = None


@dataclass
class Encounter(BaseEntity):
    """Clinical encounter within a visit."""

    visit_id: str = ""
    patient_id: str = ""
    encounter_type: str = ""
    chief_complaint: str | None = None
    assessment: str | None = None
    plan: str | None = None
    status: str = "active"
    started_at: str | None = None
    ended_at: str | None = None


@dataclass
class Appointment(BaseEntity):
    """Scheduled appointment."""

    patient_id: str = ""
    facility_id: str = ""
    department_id: str | None = None
    provider_id: str | None = None
    appointment_type: str = ""
    scheduled_date: str = ""
    scheduled_time: str = ""
    duration_minutes: int = 30
    reason: str | None = None
    status: str = "scheduled"


@dataclass
class Admission(BaseEntity):
    """Hospital admission record."""

    patient_id: str = ""
    facility_id: str = ""
    admission_type: str = ""
    admission_date: str = ""
    department_id: str | None = None
    bed_id: str | None = None
    admitting_diagnosis: str | None = None
    status: str = "active"


@dataclass
class Discharge(BaseEntity):
    """Hospital discharge record."""

    admission_id: str = ""
    patient_id: str = ""
    discharge_date: str = ""
    discharge_type: str = ""
    discharge_diagnosis: str | None = None
    discharge_instructions: str | None = None
    follow_up_date: str | None = None
    status: str = "completed"
