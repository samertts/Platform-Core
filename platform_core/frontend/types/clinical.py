"""
Clinical domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Optional

from .base import BaseEntity


@dataclass
class Diagnosis(BaseEntity):
    """Diagnosis record."""

    patient_id: str = ""
    encounter_id: Optional[str] = None
    diagnosis_code: str = ""
    diagnosis_name: str = ""
    diagnosis_type: str = ""
    onset_date: Optional[str] = None
    resolution_date: Optional[str] = None
    status: str = "active"
    severity: Optional[str] = None


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
    complications: Optional[str] = None


@dataclass
class Observation(BaseEntity):
    """Clinical observation record."""

    patient_id: str = ""
    encounter_id: Optional[str] = None
    observation_type: str = ""
    observation_code: Optional[str] = None
    observation_value: str = ""
    observation_unit: Optional[str] = None
    reference_range: Optional[str] = None
    abnormal_flag: Optional[str] = None
    recorded_by: Optional[str] = None
    recorded_at: Optional[str] = None


@dataclass
class VitalSigns(BaseEntity):
    """Vital signs record."""

    patient_id: str = ""
    encounter_id: Optional[str] = None
    temperature: Optional[float] = None
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    oxygen_saturation: Optional[float] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    recorded_by: Optional[str] = None
    recorded_at: Optional[str] = None
