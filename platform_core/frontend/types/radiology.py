"""
Radiology domain types for NHDOS Frontend
"""

from dataclasses import dataclass, field
from typing import Optional

from .base import BaseEntity


@dataclass
class RadiologyStudy(BaseEntity):
    """Radiology study record."""

    patient_id: str = ""
    facility_id: str = ""
    study_type: str = ""
    modality: str = ""
    body_part: Optional[str] = None
    clinical_indication: Optional[str] = None
    ordering_provider_id: str = ""
    status: str = "scheduled"
    study_date: Optional[str] = None


@dataclass
class Image(BaseEntity):
    """Radiology image record."""

    study_id: str = ""
    image_type: str = ""
    file_path: str = ""
    file_size: Optional[int] = None
    format: str = "DICOM"
    status: str = "available"


@dataclass
class RadiologyReport(BaseEntity):
    """Radiology report."""

    study_id: str = ""
    patient_id: str = ""
    radiologist_id: str = ""
    report_type: str = ""
    findings: Optional[str] = None
    impression: Optional[str] = None
    recommendation: Optional[str] = None
    status: str = "draft"
    signed_at: Optional[str] = None
