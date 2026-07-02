"""
Laboratory domain types for NHDOS Frontend
"""

from dataclasses import dataclass

from .base import BaseEntity


@dataclass
class Specimen(BaseEntity):
    """Laboratory specimen."""

    patient_id: str = ""
    specimen_type: str = ""
    collection_date: str = ""
    collection_method: str | None = None
    collector_id: str | None = None
    facility_id: str = ""
    status: str = "collected"
    rejection_reason: str | None = None


@dataclass
class LaboratoryOrder(BaseEntity):
    """Laboratory test order."""

    patient_id: str = ""
    encounter_id: str | None = None
    ordering_provider_id: str = ""
    facility_id: str = ""
    test_code: str = ""
    test_name: str = ""
    priority: str = "routine"
    clinical_indication: str | None = None
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
    result_unit: str | None = None
    reference_range: str | None = None
    abnormal_flag: str | None = None
    result_status: str = "final"
    performing_lab_id: str | None = None
    validated_by: str | None = None
    validated_at: str | None = None


@dataclass
class Analyzer(BaseEntity):
    """Laboratory analyzer device."""

    facility_id: str = ""
    department_id: str | None = None
    analyzer_type: str = ""
    manufacturer: str = ""
    model: str = ""
    serial_number: str = ""
    location: str | None = None
    status: str = "active"
    last_calibration_date: str | None = None
