"""
NHDOS Frontend API Client

Type-safe API client for all 57 entity contracts
"""

from .base import BaseEntityClient
from .blood_bank import BloodUnitClient, DonationClient, TransfusionClient
from .citizen import CitizenClient, DigitalCredentialClient
from .client import APIClient, APIError
from .clinical import DiagnosisClient, ObservationClient, ProcedureClient, VitalSignsClient
from .communications import CorrespondenceClient
from .epidemiology import DiseaseClient, OutbreakClient
from .financial import ClaimClient, ConsentClient, InsuranceClient, InvoiceClient, PaymentClient
from .healthcare_core import (
    AdmissionClient,
    AppointmentClient,
    DischargeClient,
    EncounterClient,
    PatientClient,
    VisitClient,
)
from .human_resources import (
    AttendanceClient,
    BedClient,
    DepartmentClient,
    EmployeeClient,
    FacilityClient,
    LeaveClient,
    LicenseClient,
    OrganizationClient,
    ProfessionalClient,
    RoomClient,
)
from .laboratory import (
    AnalyzerClient,
    LaboratoryOrderClient,
    LaboratoryResultClient,
    SpecimenClient,
)
from .medical_devices import CalibrationClient, DeviceConnectionClient, MedicalDeviceClient
from .notifications import MessageClient, NotificationClient
from .pharmacy import DispensingClient, MedicationClient, PrescriptionClient
from .public_health import ImmunizationClient, ResearchStudyClient, VaccineClient
from .radiology import ImageClient, RadiologyReportClient, RadiologyStudyClient
from .supply_chain import InventoryItemClient, PurchaseClient, SupplierClient
from .workflow import TaskClient, WorkflowClient, WorkflowStepClient

__all__ = [
    "APIClient",
    "APIError",
    "BaseEntityClient",
    "CitizenClient",
    "DigitalCredentialClient",
    "PatientClient",
    "VisitClient",
    "EncounterClient",
    "AppointmentClient",
    "AdmissionClient",
    "DischargeClient",
    "SpecimenClient",
    "LaboratoryOrderClient",
    "LaboratoryResultClient",
    "AnalyzerClient",
    "MedicalDeviceClient",
    "DeviceConnectionClient",
    "CalibrationClient",
    "RadiologyStudyClient",
    "ImageClient",
    "RadiologyReportClient",
    "PrescriptionClient",
    "MedicationClient",
    "DispensingClient",
    "DiagnosisClient",
    "ProcedureClient",
    "ObservationClient",
    "VitalSignsClient",
    "DonationClient",
    "BloodUnitClient",
    "TransfusionClient",
    "DiseaseClient",
    "OutbreakClient",
    "ProfessionalClient",
    "LicenseClient",
    "OrganizationClient",
    "FacilityClient",
    "DepartmentClient",
    "RoomClient",
    "BedClient",
    "EmployeeClient",
    "AttendanceClient",
    "LeaveClient",
    "InsuranceClient",
    "ConsentClient",
    "InvoiceClient",
    "PaymentClient",
    "ClaimClient",
    "InventoryItemClient",
    "SupplierClient",
    "PurchaseClient",
    "WorkflowClient",
    "WorkflowStepClient",
    "TaskClient",
    "NotificationClient",
    "MessageClient",
    "VaccineClient",
    "ImmunizationClient",
    "ResearchStudyClient",
    "CorrespondenceClient",
]
