"""
NHDOS Unified Healthcare Platform — Frontend Domain Types

Phase 17: Frontend Development
35 business domains, 57 canonical entities, type-safe interfaces
"""

from .base import BaseEntity, BaseEvent, BaseRelationship
from .blood_bank import BloodUnit, Donation, Transfusion
from .citizen import Citizen, DigitalCredential
from .clinical import Diagnosis, Observation, Procedure, VitalSigns
from .communications import Correspondence
from .epidemiology import Disease, Outbreak
from .financial import Claim, Consent, Insurance, Invoice, Payment
from .healthcare_core import Admission, Appointment, Discharge, Encounter, Patient, Visit
from .human_resources import (
    Attendance,
    Bed,
    Department,
    Employee,
    Facility,
    Leave,
    License,
    Organization,
    Professional,
    Room,
)
from .laboratory import Analyzer, LaboratoryOrder, LaboratoryResult, Specimen
from .medical_devices import Calibration, DeviceConnection, MedicalDevice
from .notifications import Message, Notification
from .pharmacy import Dispensing, Medication, Prescription
from .public_health import Immunization, ResearchStudy, Vaccine
from .radiology import Image, RadiologyReport, RadiologyStudy
from .supply_chain import InventoryItem, Purchase, Supplier
from .workflow import Task, Workflow, WorkflowStep

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
