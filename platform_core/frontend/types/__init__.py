"""
NHDOS Unified Healthcare Platform — Frontend Domain Types

Phase 17: Frontend Development
35 business domains, 57 canonical entities, type-safe interfaces
"""

from .base import BaseEntity, BaseRelationship, BaseEvent
from .citizen import Citizen, DigitalCredential
from .healthcare_core import (
    Patient, Visit, Encounter, Appointment, Admission, Discharge
)
from .laboratory import (
    Specimen, LaboratoryOrder, LaboratoryResult, Analyzer
)
from .medical_devices import (
    MedicalDevice, DeviceConnection, Calibration
)
from .radiology import (
    RadiologyStudy, Image, RadiologyReport
)
from .pharmacy import (
    Prescription, Medication, Dispensing
)
from .clinical import (
    Diagnosis, Procedure, Observation, VitalSigns
)
from .blood_bank import (
    Donation, BloodUnit, Transfusion
)
from .epidemiology import (
    Disease, Outbreak
)
from .human_resources import (
    Professional, License, Organization, Facility, Department, Room, Bed, Employee, Attendance, Leave
)
from .financial import (
    Insurance, Consent, Invoice, Payment, Claim
)
from .supply_chain import (
    InventoryItem, Supplier, Purchase
)
from .workflow import (
    Workflow, WorkflowStep, Task
)
from .notifications import (
    Notification, Message
)
from .public_health import (
    Vaccine, Immunization, ResearchStudy
)
from .communications import (
    Correspondence
)

__all__ = [
    "BaseEntity",
    "BaseRelationship",
    "BaseEvent",
    "Citizen",
    "DigitalCredential",
    "Patient",
    "Visit",
    "Encounter",
    "Appointment",
    "Admission",
    "Discharge",
    "Specimen",
    "LaboratoryOrder",
    "LaboratoryResult",
    "Analyzer",
    "MedicalDevice",
    "DeviceConnection",
    "Calibration",
    "RadiologyStudy",
    "Image",
    "RadiologyReport",
    "Prescription",
    "Medication",
    "Dispensing",
    "Diagnosis",
    "Procedure",
    "Observation",
    "VitalSigns",
    "Donation",
    "BloodUnit",
    "Transfusion",
    "Disease",
    "Outbreak",
    "Professional",
    "License",
    "Organization",
    "Facility",
    "Department",
    "Room",
    "Bed",
    "Employee",
    "Attendance",
    "Leave",
    "Insurance",
    "Consent",
    "Invoice",
    "Payment",
    "Claim",
    "InventoryItem",
    "Supplier",
    "Purchase",
    "Workflow",
    "WorkflowStep",
    "Task",
    "Notification",
    "Message",
    "Vaccine",
    "Immunization",
    "ResearchStudy",
    "Correspondence",
]
