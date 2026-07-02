"""
Radiology domain types for NHDOS Frontend
"""

from dataclasses import dataclass

from .base import BaseEntity


@dataclass
class RadiologyStudy(BaseEntity):
    """Radiology study record."""

    patient_id: str = ""
    facility_id: str = ""
    study_type: str = ""
    modality: str = ""
    body_part: str | None = None
    clinical_indication: str | None = None
    ordering_provider_id: str = ""
    status: str = "scheduled"
    study_date: str | None = None


@dataclass
class Image(BaseEntity):
    """Radiology image record."""

    study_id: str = ""
    image_type: str = ""
    file_path: str = ""
    file_size: int | None = None
    format: str = "DICOM"
    status: str = "available"


@dataclass
class RadiologyReport(BaseEntity):
    """Radiology report."""

    study_id: str = ""
    patient_id: str = ""
    radiologist_id: str = ""
    report_type: str = ""
    findings: str | None = None
    impression: str | None = None
    recommendation: str | None = None
    status: str = "draft"
    signed_at: str | None = None
