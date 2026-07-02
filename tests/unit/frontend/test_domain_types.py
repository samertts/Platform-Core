"""
Tests for NHDOS Frontend Domain Types
"""

import sys

sys.path.insert(0, "/tmp")

from platform_core.frontend.types.citizen import Citizen, DigitalCredential
from platform_core.frontend.types.clinical import (Diagnosis, Observation,
                                                   Procedure, VitalSigns)
from platform_core.frontend.types.healthcare_core import (Admission,
                                                          Appointment,
                                                          Discharge, Encounter,
                                                          Patient, Visit)
from platform_core.frontend.types.laboratory import (Analyzer, LaboratoryOrder,
                                                     LaboratoryResult,
                                                     Specimen)
from platform_core.frontend.types.medical_devices import (Calibration,
                                                          DeviceConnection,
                                                          MedicalDevice)
from platform_core.frontend.types.pharmacy import (Dispensing, Medication,
                                                   Prescription)


class TestCitizenTypes:
    def test_citizen_creation(self):
        citizen = Citizen(national_id="1234567890", full_name="John Doe")
        assert citizen.national_id == "1234567890"
        assert citizen.full_name == "John Doe"
        assert citizen.confidentiality_level == 5

    def test_digital_credential_creation(self):
        credential = DigitalCredential(citizen_id="c1", credential_type="national_id")
        assert credential.citizen_id == "c1"
        assert credential.credential_type == "national_id"


class TestHealthcareCoreTypes:
    def test_patient_creation(self):
        patient = Patient(citizen_id="c1", medical_record_number="MRN001")
        assert patient.citizen_id == "c1"
        assert patient.medical_record_number == "MRN001"
        assert patient.confidentiality_level == 5

    def test_visit_creation(self):
        visit = Visit(patient_id="p1", facility_id="f1", visit_type="outpatient")
        assert visit.patient_id == "p1"
        assert visit.facility_id == "f1"

    def test_encounter_creation(self):
        encounter = Encounter(
            visit_id="v1", patient_id="p1", encounter_type="consultation"
        )
        assert encounter.visit_id == "v1"
        assert encounter.patient_id == "p1"

    def test_appointment_creation(self):
        appointment = Appointment(
            patient_id="p1", facility_id="f1", scheduled_date="2026-01-01"
        )
        assert appointment.patient_id == "p1"
        assert appointment.scheduled_date == "2026-01-01"

    def test_admission_creation(self):
        admission = Admission(
            patient_id="p1", facility_id="f1", admission_type="emergency"
        )
        assert admission.patient_id == "p1"
        assert admission.admission_type == "emergency"

    def test_discharge_creation(self):
        discharge = Discharge(
            admission_id="a1", patient_id="p1", discharge_type="regular"
        )
        assert discharge.admission_id == "a1"
        assert discharge.patient_id == "p1"


class TestLaboratoryTypes:
    def test_specimen_creation(self):
        specimen = Specimen(patient_id="p1", specimen_type="blood", facility_id="f1")
        assert specimen.patient_id == "p1"
        assert specimen.specimen_type == "blood"

    def test_lab_order_creation(self):
        order = LaboratoryOrder(
            patient_id="p1", ordering_provider_id="doc1", test_code="CBC"
        )
        assert order.patient_id == "p1"
        assert order.test_code == "CBC"

    def test_lab_result_creation(self):
        result = LaboratoryResult(order_id="o1", specimen_id="s1", result_value="12.5")
        assert result.order_id == "o1"
        assert result.result_value == "12.5"

    def test_analyzer_creation(self):
        analyzer = Analyzer(
            facility_id="f1", analyzer_type="hematology", manufacturer="Sysmex"
        )
        assert analyzer.analyzer_type == "hematology"
        assert analyzer.manufacturer == "Sysmex"


class TestMedicalDeviceTypes:
    def test_medical_device_creation(self):
        device = MedicalDevice(
            facility_id="f1", device_type="monitor", manufacturer="Philips"
        )
        assert device.device_type == "monitor"
        assert device.manufacturer == "Philips"

    def test_device_connection_creation(self):
        connection = DeviceConnection(device_id="d1", connection_type="usb")
        assert connection.device_id == "d1"
        assert connection.connection_type == "usb"

    def test_calibration_creation(self):
        calibration = Calibration(
            device_id="d1", calibration_type="daily", result="pass"
        )
        assert calibration.device_id == "d1"
        assert calibration.result == "pass"


class TestPharmacyTypes:
    def test_prescription_creation(self):
        prescription = Prescription(patient_id="p1", medication_id="m1", dosage="500mg")
        assert prescription.patient_id == "p1"
        assert prescription.dosage == "500mg"

    def test_medication_creation(self):
        medication = Medication(name="Paracetamol", manufacturer="PharmaCo")
        assert medication.name == "Paracetamol"
        assert medication.manufacturer == "PharmaCo"

    def test_dispensing_creation(self):
        dispensing = Dispensing(
            prescription_id="pr1", medication_id="m1", quantity_dispensed=10
        )
        assert dispensing.prescription_id == "pr1"
        assert dispensing.quantity_dispensed == 10


class TestClinicalTypes:
    def test_diagnosis_creation(self):
        diagnosis = Diagnosis(
            patient_id="p1", diagnosis_code="J06.9", diagnosis_name="Common cold"
        )
        assert diagnosis.diagnosis_code == "J06.9"
        assert diagnosis.diagnosis_name == "Common cold"

    def test_procedure_creation(self):
        procedure = Procedure(
            patient_id="p1", procedure_code="99213", procedure_name="Office visit"
        )
        assert procedure.procedure_code == "99213"

    def test_observation_creation(self):
        observation = Observation(patient_id="p1", observation_value="120/80")
        assert observation.observation_value == "120/80"

    def test_vital_signs_creation(self):
        vitals = VitalSigns(patient_id="p1", temperature=36.5, heart_rate=72)
        assert vitals.temperature == 36.5
        assert vitals.heart_rate == 72
