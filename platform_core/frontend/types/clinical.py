"""
Clinical domain types for NHDOS Frontend
"""

from dataclasses import dataclass

from .base import BaseEntity


@dataclass
class Diagnosis(BaseEntity):
    """Diagnosis record."""

    patient_id: str = ""
    encounter_id: str | None = None
    diagnosis_code: str = ""
    diagnosis_name: str = ""
    diagnosis_type: str = ""
    onset_date: str | None = None
    resolution_date: str | None = None
    status: str = "active"
    severity: str | None = None


@dataclass
class Procedure(BaseEntity):
    """Procedure record."""

    patient_id: str = ""
    encounter_id: str = ""
    procedure_code: str = ""
    procedure_name: str = ""
    performing_provider_id: str = ""
    facility_id: str = ""
    procedure_date: str = ""
    status: str = "completed"
    complications: str | None = None


@dataclass
class Observation(BaseEntity):
    """Clinical observation record."""

    patient_id: str = ""
    encounter_id: str | None = None
    observation_type: str = ""
    observation_code: str | None = None
    observation_value: str = ""
    observation_unit: str | None = None
    reference_range: str | None = None
    abnormal_flag: str | None = None
    recorded_by: str | None = None
    recorded_at: str | None = None


@dataclass
class VitalSigns(BaseEntity):
    """Vital signs record."""

    patient_id: str = ""
    encounter_id: str | None = None
    temperature: float | None = None
    heart_rate: int | None = None
    respiratory_rate: int | None = None
    blood_pressure_systolic: int | None = None
    blood_pressure_diastolic: int | None = None
    oxygen_saturation: float | None = None
    weight: float | None = None
    height: float | None = None
    recorded_by: str | None = None
    recorded_at: str | None = None
