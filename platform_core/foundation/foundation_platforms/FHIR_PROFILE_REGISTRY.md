# FHIR PROFILE REGISTRY

**NHDOS Platform-Core — Foundation Platform 4: FHIR Profiles for Iraqi Healthcare**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The FHIR Profile Registry defines and manages HL7 FHIR R4 profiles customized for Iraqi healthcare data exchange requirements. It provides validation, conformance testing, and version management for all NHDOS FHIR profiles across 18 governorates and 4,800 healthcare facilities.

---

## 2. Architecture

### 2.1 Core Principles

| Principle | Description |
|-----------|-------------|
| FHIR R4 Compliance | HL7 FHIR R4 base conformance |
| Iraqi Customization | Profiles adapted for national requirements |
| Validation-First | All data validated against profiles |
| Versioned | Profiles versioned with backward compatibility |
| Registry-Based | Centralized profile registry |
| Offline Capable | Profile validation on edge sites |

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FHIR PROFILE REGISTRY                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Profile     │  │  Validation  │  │  Conformance │          │
│  │  Registry    │──▶│  Engine      │──▶│  Testing     │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │  Structure   │  │  Implementation│ │  Validation  │          │
│  │  Definitions │  │  Guides       │  │  Resources   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Core Profiles

### 3.1 Patient Profiles

| Profile | Description | Resources |
|---------|-------------|-----------|
| NHDOS-Patient | Core patient demographics | Patient |
| NHDOS-Patient-Identity | National identity extension | Patient |
| NHDOS-Patient-Insurance | Insurance information | Patient |
| NHDOS-Patient-Contact | Emergency contact | Patient |

### 3.2 Clinical Profiles

| Profile | Description | Resources |
|---------|-------------|-----------|
| NHDOS-Encounter | Clinical encounter | Encounter |
| NHDOS-Condition | Diagnosis/condition | Condition |
| NHDOS-Observation | Clinical observation | Observation |
| NHDOS-MedicationRequest | Prescription | MedicationRequest |
| NHDOS-MedicationAdministration | Drug administration | MedicationAdministration |
| NHDOS-AllergyIntolerance | Allergy/intolerance | AllergyIntolerance |
| NHDOS-Procedure | Clinical procedure | Procedure |

### 3.3 Laboratory Profiles

| Profile | Description | Resources |
|---------|-------------|-----------|
| NHDOS-Specimen | Lab specimen | Specimen |
| NHDOS-DiagnosticReport | Lab result report | DiagnosticReport |
| NHDOS-Observation-Lab | Lab observation | Observation |

### 3.4 Imaging Profiles

| Profile | Description | Resources |
|---------|-------------|-----------|
| NHDOS-ImagingStudy | Imaging study | ImagingStudy |
| NHDOS-DICOMMetadata | DICOM metadata | ImagingStudy |

---

## 4. Profile Definitions

### 4.1 NHDOS-Patient Profile

```json
{
  "resourceType": "StructureDefinition",
  "id": "NHDOS-Patient",
  "url": "http://nhdos.iq/fhir/StructureDefinition/NHDOS-Patient",
  "name": "NHDOS Patient",
  "status": "active",
  "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
  "type": "Patient",
  "differential": {
    "element": [
      {
        "path": "Patient.identifier",
        "min": 1,
        "max": "*"
      },
      {
        "path": "Patient.identifier:nationalId",
        "min": 1,
        "max": 1,
        "type": {
          "code": "Identifier",
          "profile": "http://nhdos.iq/fhir/StructureDefinition/NHDOS-Identifier-National"
        }
      },
      {
        "path": "Patient.name",
        "min": 1,
        "max": "*"
      },
      {
        "path": "Patient.gender",
        "min": 1,
        "max": 1
      },
      {
        "path": "Patient.birthDate",
        "min": 1,
        "max": 1
      }
    ]
  }
}
```

---

## 5. Validation Rules

### 5.1 Validation Levels

| Level | Description | Action |
|-------|-------------|--------|
| Error | Must conform | Reject resource |
| Warning | Should conform | Log warning |
| Information | May conform | Log info |

### 5.2 Common Validation Rules

| Rule | Profile | Level | Description |
|------|---------|-------|-------------|
| National ID Required | Patient | Error | National ID must be present |
| Gender Required | Patient | Error | Gender must be specified |
| Arabic Name Required | Patient | Error | Arabic name must be present |
| Encounter Type Required | Encounter | Error | Encounter type must be specified |
| Condition Code Required | Condition | Error | Condition code must be valid ICD-11 |
| Lab Result Required | DiagnosticReport | Error | At least one result required |

---

## 6. APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| /fhir/StructureDefinition | GET | List all profiles |
| /fhir/StructureDefinition/{id} | GET | Get profile |
| /fhir/StructureDefinition/{id}/validate | POST | Validate resource |
| /api/v1/fhir-profiles | GET | List NHDOS profiles |
| /api/v1/fhir-profiles/{id}/metadata | GET | Get profile metadata |
| /api/v1/fhir-profiles/validation-rules | GET | Get validation rules |

---

## 7. Offline Support

| Capability | Implementation |
|------------|----------------|
| Profile Cache | Full profile cache on edge |
| Offline Validation | Local validation engine |
| Sync Protocol | Delta sync on reconnect |
| Cache Size | ~50MB compressed |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
