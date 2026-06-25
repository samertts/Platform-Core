"""
NHDOS Frontend API Client

Type-safe API client for all 57 entity contracts
"""

from .client import APIClient, APIError
from .base import BaseEntityClient
from .citizen import CitizenClient, DigitalCredentialClient
from .healthcare_core import (
    PatientClient, VisitClient, EncounterClient,
    AppointmentClient, AdmissionClient, DischargeClient
)
from .laboratory import (
    SpecimenClient, LaboratoryOrderClient, LaboratoryResultClient, AnalyzerClient
)
from .medical_devices import (
    MedicalDeviceClient, DeviceConnectionClient, CalibrationClient
)
from .radiology import (
    RadiologyStudyClient, ImageClient, RadiologyReportClient
)
from .pharmacy import (
    PrescriptionClient, MedicationClient, DispensingClient
)
from .clinical import (
    DiagnosisClient, ProcedureClient, ObservationClient, VitalSignsClient
)
from .blood_bank import (
    DonationClient, BloodUnitClient, TransfusionClient
)
from .epidemiology import (
    DiseaseClient, OutbreakClient
)
from .human_resources import (
    ProfessionalClient, LicenseClient, OrganizationClient,
    FacilityClient, DepartmentClient, RoomClient, BedClient,
    EmployeeClient, AttendanceClient, LeaveClient
)
from .financial import (
    InsuranceClient, ConsentClient, InvoiceClient, PaymentClient, ClaimClient
)
from .supply_chain import (
    InventoryItemClient, SupplierClient, PurchaseClient
)
from .workflow import (
    WorkflowClient, WorkflowStepClient, TaskClient
)
from .notifications import (
    NotificationClient, MessageClient
)
from .public_health import (
    VaccineClient, ImmunizationClient, ResearchStudyClient
)
from .communications import (
    CorrespondenceClient
)

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
