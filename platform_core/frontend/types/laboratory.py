"""
Laboratory domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Optional

from .base import BaseEntity


@dataclass
class Specimen(BaseEntity):
    """Laboratory specimen."""

    patient_id: str = ""
    specimen_type: str = ""
    collection_date: str = ""
    collection_method: Optional[str] = None
    collector_id: Optional[str] = None
    facility_id: str = ""
    status: str = "collected"
    rejection_reason: Optional[str] = None


@dataclass
class LaboratoryOrder(BaseEntity):
    """Laboratory test order."""

    patient_id: str = ""
    encounter_id: Optional[str] = None
    ordering_provider_id: str = ""
    facility_id: str = ""
    test_code: str = ""
    test_name: str = ""
    priority: str = "routine"
    clinical_indication: Optional[str] = None
    status: str = "ordered"


@dataclass
class LaboratoryResult(BaseEntity):
    """Laboratory test result."""

    order_id: str = ""
    specimen_id: str = ""
    patient_id: str = ""
    test_code: str = ""
    test_name: str = ""
    result_value: str = ""
    result_unit: Optional[str] = None
    reference_range: Optional[str] = None
    abnormal_flag: Optional[str] = None
    result_status: str = "final"
    performing_lab_id: Optional[str] = None
    validated_by: Optional[str] = None
    validated_at: Optional[str] = None


@dataclass
class Analyzer(BaseEntity):
    """Laboratory analyzer device."""

    facility_id: str = ""
    department_id: Optional[str] = None
    analyzer_type: str = ""
    manufacturer: str = ""
    model: str = ""
    serial_number: str = ""
    location: Optional[str] = None
    status: str = "active"
    last_calibration_date: Optional[str] = None
