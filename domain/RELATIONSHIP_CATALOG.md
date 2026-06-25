# National Healthcare Digital Operating System (NHDOS) - Relationship Catalog

**Version:** 1.0.0  
**Status:** CANONICAL MODEL  
**Last Updated:** 2026-06-25  
**Classification:** Production-Ready Documentation

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Relationship Modeling Conventions](#relationship-modeling-conventions)
3. [Complete Relationship Registry](#complete-relationship-registry)
4. [Relationship Patterns](#relationship-patterns)
5. [Cardinality Rules](#cardinality-rules)
6. [Cascade Rules](#cascade-rules)
7. [Relationship Constraints](#relationship-constraints)

---

## Executive Summary

This document serves as the **CANONICAL RELATIONSHIP CATALOG** for the National Healthcare Digital Operating System (NHDOS). It defines 120+ relationships between entities with complete specifications including cardinality, constraints, and business rules.

### Relationship Categories

| Category | Count | Description |
|----------|-------|-------------|
| One-to-One | 25 | 1:1 relationships |
| One-to-Many | 65 | 1:N relationships |
| Many-to-Many | 30 | M:N relationships via junction tables |
| **Total** | **120** | Complete relationship inventory |

---

## Relationship Modeling Conventions

### Relationship Types

| Type | Symbol | Description | Example |
|------|--------|-------------|---------|
| **Identifying** | Solid line | Parent existence dependent | Order → OrderItem |
| **Non-Identifying** | Dashed line | Independent existence | Patient → Address |
| **Inheritance** | Triangle | Subtype relationship | Order → LabOrder |
| **Aggregation** | Diamond (hollow) | Weak ownership | Patient → Insurance |
| **Composition** | Diamond (filled) | Strong ownership | Encounter → VitalSigns |

### Cardinality Notation

| Notation | Description | Example |
|----------|-------------|---------|
| 1:1 | One-to-One | User → UserProfile |
| 1:N | One-to-Many | Patient → Encounter |
| M:N | Many-to-Many | Role → Permission |
| 0..1 | Optional one | Encounter → Bed |
| 1..1 | Required one | Encounter → Patient |
| 0..* | Optional many | Patient → Allergy |
| 1..* | Required many | Encounter → VitalSigns |

### Relationship Naming

| Pattern | Convention | Example |
|---------|-----------|---------|
| Foreign Key | {parent}Id | patientId, encounterId |
| Junction Table | {Entity1}_{Entity2} | Role_Permission |
| Relationship Name | {Verb} | PatientOwns, EncounterHas |

---

## Complete Relationship Registry

### Foundation Domain Relationships

#### 1. User → UserProfile (One-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-001 |
| **Source Entity** | User |
| **Target Entity** | UserProfile |
| **Relationship Type** | One-to-One |
| **Cardinality** | 1:1 |
| **Description** | Each user has one profile with extended information |
| **Foreign Key** | userProfileId in User table |
| **Owner** | User |
| **Cascade** | Delete User → Delete UserProfile |
| **Nullability** | Optional (profile may not exist) |
| **Constraints** | UserProfile.userId must be unique |

---

#### 2. User → UserRoleAssignment (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-002 |
| **Source Entity** | User |
| **Target Entity** | UserRoleAssignment |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A user can be assigned multiple roles |
| **Foreign Key** | userId in UserRoleAssignment |
| **Owner** | User |
| **Cascade** | Delete User → Delete UserRoleAssignments |
| **Nullability** | Required (at least one role) |
| **Constraints** | Role must be active |

---

#### 3. Role → UserRoleAssignment (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-003 |
| **Source Entity** | Role |
| **Target Entity** | UserRoleAssignment |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A role can be assigned to multiple users |
| **Foreign Key** | roleId in UserRoleAssignment |
| **Owner** | Role |
| **Cascade** | Delete Role → Prevent (active assignments) |
| **Nullability** | Required |
| **Constraints** | Role must be active |

---

#### 4. Role → Permission (Many-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-004 |
| **Source Entity** | Role |
| **Target Entity** | Permission |
| **Relationship Type** | Many-to-Many |
| **Cardinality** | M:N |
| **Description** | Roles can have multiple permissions; permissions can belong to multiple roles |
| **Junction Table** | RolePermission |
| **Foreign Keys** | roleId, permissionId |
| **Owner** | Both |
| **Cascade** | Delete Role → Delete RolePermission entries |
| **Nullability** | Required (role must have permissions) |
| **Constraints** | Permission must be active |

---

#### 5. User → Session (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-005 |
| **Source Entity** | User |
| **Target Entity** | Session |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A user can have multiple active sessions |
| **Foreign Key** | userId in Session |
| **Owner** | User |
| **Cascade** | Delete User → Delete Sessions |
| **Nullability** | Required |
| **Constraints** | Max 5 active sessions per user |

---

#### 6. User → AuditLog (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-006 |
| **Source Entity** | User |
| **Target Entity** | AuditLog |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A user generates multiple audit log entries |
| **Foreign Key** | userId in AuditLog |
| **Owner** | User |
| **Cascade** | Delete User → Prevent (audit retention) |
| **Nullability** | Required |
| **Constraints** | Audit logs are immutable |

---

### Patient Domain Relationships

#### 7. Patient → Address (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-007 |
| **Source Entity** | Patient |
| **Target Entity** | Address |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A patient can have multiple addresses |
| **Foreign Key** | patientId in Address |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Delete Addresses |
| **Nullability** | Required (at least one address) |
| **Constraints** | Only one address can be primary |

---

#### 8. Patient → Allergy (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-008 |
| **Source Entity** | Patient |
| **Target Entity** | Allergy |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A patient can have multiple allergies |
| **Foreign Key** | patientId in Allergy |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Delete Allergies |
| **Nullability** | Optional |
| **Constraints** | Allergy must be active or inactive |

---

#### 9. Patient → Medication (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-009 |
| **Source Entity** | Patient |
| **Target Entity** | Medication |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A patient can have multiple medications |
| **Foreign Key** | patientId in Medication |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Delete Medications |
| **Nullability** | Optional |
| **Constraints** | Medication must be active |

---

#### 10. Patient → Immunization (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-010 |
| **Source Entity** | Patient |
| **Target Entity** | Immunization |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A patient can have multiple immunizations |
| **Foreign Key** | patientId in Immunization |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Delete Immunizations |
| **Nullability** | Optional |
| **Constraints** | None |

---

#### 11. Patient → Consent (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-011 |
| **Source Entity** | Patient |
| **Target Entity** | Consent |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A patient can have multiple consents |
| **Foreign Key** | patientId in Consent |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Delete Consents |
| **Nullability** | Optional |
| **Constraints** | Consent must be active |

---

#### 12. Patient → EmergencyContact (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-012 |
| **Source Entity** | Patient |
| **Target Entity** | EmergencyContact |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A patient can have multiple emergency contacts |
| **Foreign Key** | patientId in EmergencyContact |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Delete EmergencyContacts |
| **Nullability** | Required (at least one) |
| **Constraints** | None |

---

#### 13. Patient → InsurancePolicy (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-013 |
| **Source Entity** | Patient |
| **Target Entity** | InsurancePolicy |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A patient can have multiple insurance policies |
| **Foreign Key** | patientId in InsurancePolicy |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Delete InsurancePolicies |
| **Nullability** | Optional |
| **Constraints** | Only one primary insurance |

---

#### 14. Patient → PatientIdentifier (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-014 |
| **Source Entity** | Patient |
| **Target Entity** | PatientIdentifier |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A patient can have multiple identifiers (MRN, SSN, etc.) |
| **Foreign Key** | patientId in PatientIdentifier |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Delete Identifiers |
| **Nullability** | Required (at least MRN) |
| **Constraints** | MRN must be unique |

---

### Encounter Domain Relationships

#### 15. Patient → Encounter (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-015 |
| **Source Entity** | Patient |
| **Target Entity** | Encounter |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A patient can have multiple encounters |
| **Foreign Key** | patientId in Encounter |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Prevent (encounters exist) |
| **Nullability** | Required |
| **Constraints** | Patient must be active |

---

#### 16. Encounter → ClinicalDocumentation (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-016 |
| **Source Entity** | Encounter |
| **Target Entity** | ClinicalDocumentation |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | An encounter can have multiple clinical documents |
| **Foreign Key** | encounterId in ClinicalDocumentation |
| **Owner** | Encounter |
| **Cascade** | Delete Encounter → Delete ClinicalDocumentations |
| **Nullability** | Optional |
| **Constraints** | Documents must be signed |

---

#### 17. Encounter → VitalSigns (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-017 |
| **Source Entity** | Encounter |
| **Target Entity** | VitalSigns |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | An encounter can have multiple vital sign recordings |
| **Foreign Key** | encounterId in VitalSigns |
| **Owner** | Encounter |
| **Cascade** | Delete Encounter → Delete VitalSigns |
| **Nullability** | Optional |
| **Constraints** | None |

---

#### 18. Encounter → Diagnosis (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-018 |
| **Source Entity** | Encounter |
| **Target Entity** | Diagnosis |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | An encounter can have multiple diagnoses |
| **Foreign Key** | encounterId in Diagnosis |
| **Owner** | Encounter |
| **Cascade** | Delete Encounter → Delete Diagnoses |
| **Nullability** | Optional |
| **Constraints** | At least one primary diagnosis |

---

#### 19. Encounter → Order (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-019 |
| **Source Entity** | Encounter |
| **Target Entity** | Order |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | An encounter can have multiple orders |
| **Foreign Key** | encounterId in Order |
| **Owner** | Encounter |
| **Cascade** | Delete Encounter → Delete Orders |
| **Nullability** | Optional |
| **Constraints** | Orders must be completed before encounter closes |

---

#### 20. Encounter → Department (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-020 |
| **Source Entity** | Encounter |
| **Target Entity** | Department |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | An encounter occurs in one department |
| **Foreign Key** | departmentId in Encounter |
| **Owner** | Department |
| **Cascade** | Delete Department → Prevent (active encounters) |
| **Nullability** | Required |
| **Constraints** | Department must be active |

---

#### 21. Encounter → Hospital (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-021 |
| **Source Entity** | Encounter |
| **Target Entity** | Hospital |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | An encounter occurs at one hospital |
| **Foreign Key** | facilityId in Encounter |
| **Owner** | Hospital |
| **Cascade** | Delete Hospital → Prevent (active encounters) |
| **Nullability** | Required |
| **Constraints** | Hospital must be active |

---

### Orders Domain Relationships

#### 22. Order → Patient (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-022 |
| **Source Entity** | Order |
| **Target Entity** | Patient |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | An order belongs to one patient |
| **Foreign Key** | patientId in Order |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Prevent (active orders) |
| **Nullability** | Required |
| **Constraints** | Patient must be active |

---

#### 23. Order → User (Many-to-One, Ordering Provider)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-023 |
| **Source Entity** | Order |
| **Target Entity** | User |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | An order is placed by one provider |
| **Foreign Key** | orderingProviderId in Order |
| **Owner** | User |
| **Cascade** | Delete User → Prevent (active orders) |
| **Nullability** | Required |
| **Constraints** | User must have provider role |

---

### Laboratory Domain Relationships

#### 24. LabOrder → Specimen (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-024 |
| **Source Entity** | LabOrder |
| **Target Entity** | Specimen |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A lab order can have multiple specimens |
| **Foreign Key** | labOrderId in Specimen |
| **Owner** | LabOrder |
| **Cascade** | Delete LabOrder → Delete Specimens |
| **Nullability** | Required (at least one) |
| **Constraints** | Specimen must be collected |

---

#### 25. LabOrder → LabResult (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-025 |
| **Source Entity** | LabOrder |
| **Target Entity** | LabResult |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A lab order can have multiple results |
| **Foreign Key** | labOrderId in LabResult |
| **Owner** | LabOrder |
| **Cascade** | Delete LabOrder → Delete LabResults |
| **Nullability** | Optional |
| **Constraints** | Results must be verified |

---

#### 26. Specimen → LabResult (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-026 |
| **Source Entity** | Specimen |
| **Target Entity** | LabResult |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A specimen can have multiple test results |
| **Foreign Key** | specimenId in LabResult |
| **Owner** | Specimen |
| **Cascade** | Delete Specimen → Delete LabResults |
| **Nullability** | Optional |
| **Constraints** | None |

---

#### 27. Specimen → User (Many-to-One, Collector)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-027 |
| **Source Entity** | Specimen |
| **Target Entity** | User |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A specimen is collected by one user |
| **Foreign Key** | collectedBy in Specimen |
| **Owner** | User |
| **Cascade** | Delete User → Prevent (specimens exist) |
| **Nullability** | Required |
| **Constraints** | User must have collection privileges |

---

### Radiology Domain Relationships

#### 28. RadiologyOrder → ImagingStudy (One-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-028 |
| **Source Entity** | RadiologyOrder |
| **Target Entity** | ImagingStudy |
| **Relationship Type** | One-to-One |
| **Cardinality** | 1:1 |
| **Description** | A radiology order creates one imaging study |
| **Foreign Key** | radiologyOrderId in ImagingStudy |
| **Owner** | RadiologyOrder |
| **Cascade** | Delete RadiologyOrder → Delete ImagingStudy |
| **Nullability** | Optional (study created after order) |
| **Constraints** | Study must match order modality |

---

#### 29. RadiologyOrder → RadiologyReport (One-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-029 |
| **Source Entity** | RadiologyOrder |
| **Target Entity** | RadiologyReport |
| **Relationship Type** | One-to-One |
| **Cardinality** | 1:1 |
| **Description** | A radiology order has one report |
| **Foreign Key** | radiologyOrderId in RadiologyReport |
| **Owner** | RadiologyOrder |
| **Cascade** | Delete RadiologyOrder → Delete RadiologyReport |
| **Nullability** | Optional (report created after study) |
| **Constraints** | Report must be signed |

---

#### 30. ImagingStudy → Image (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-030 |
| **Source Entity** | ImagingStudy |
| **Target Entity** | Image |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | An imaging study contains multiple images |
| **Foreign Key** | studyId in Image |
| **Owner** | ImagingStudy |
| **Cascade** | Delete ImagingStudy → Delete Images |
| **Nullability** | Required (at least one) |
| **Constraints** | Images must be DICOM format |

---

#### 31. ImagingStudy → RadiologyReport (One-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-031 |
| **Source Entity** | ImagingStudy |
| **Target Entity** | RadiologyReport |
| **Relationship Type** | One-to-One |
| **Cardinality** | 1:1 |
| **Description** | An imaging study has one interpretation report |
| **Foreign Key** | studyId in RadiologyReport |
| **Owner** | ImagingStudy |
| **Cascade** | Delete ImagingStudy → Delete RadiologyReport |
| **Nullability** | Optional |
| **Constraints** | None |

---

#### 32. RadiologyReport → User (Many-to-One, Radiologist)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-032 |
| **Source Entity** | RadiologyReport |
| **Target Entity** | User |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A report is interpreted by one radiologist |
| **Foreign Key** | radiologistId in RadiologyReport |
| **Owner** | User |
| **Cascade** | Delete User → Prevent (reports exist) |
| **Nullability** | Required |
| **Constraints** | User must be radiologist |

---

### Pharmacy Domain Relationships

#### 33. MedicationOrder → Medication (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-033 |
| **Source Entity** | MedicationOrder |
| **Target Entity** | Medication |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A medication order references one medication |
| **Foreign Key** | medicationId in MedicationOrder |
| **Owner** | Medication |
| **Cascade** | Delete Medication → Prevent (active orders) |
| **Nullability** | Required |
| **Constraints** | Medication must be active in formulary |

---

#### 34. MedicationOrder → DispensingRecord (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-034 |
| **Source Entity** | MedicationOrder |
| **Target Entity** | DispensingRecord |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A medication order can have multiple dispensing events |
| **Foreign Key** | medicationOrderId in DispensingRecord |
| **Owner** | MedicationOrder |
| **Cascade** | Delete MedicationOrder → Delete DispensingRecords |
| **Nullability** | Optional |
| **Constraints** | Dispensing must match order quantity |

---

#### 35. MedicationOrder → AdministrationRecord (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-035 |
| **Source Entity** | MedicationOrder |
| **Target Entity** | AdministrationRecord |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A medication order can have multiple administration events |
| **Foreign Key** | medicationOrderId in AdministrationRecord |
| **Owner** | MedicationOrder |
| **Cascade** | Delete MedicationOrder → Delete AdministrationRecords |
| **Nullability** | Optional |
| **Constraints** | Administration must match order dosage |

---

#### 36. DispensingRecord → Pharmacy (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-036 |
| **Source Entity** | DispensingRecord |
| **Target Entity** | Pharmacy |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A dispensing event occurs at one pharmacy |
| **Foreign Key** | pharmacyId in DispensingRecord |
| **Owner** | Pharmacy |
| **Cascade** | Delete Pharmacy → Prevent (dispensing records) |
| **Nullability** | Required |
| **Constraints** | Pharmacy must be active |

---

#### 37. DispensingRecord → User (Many-to-One, Pharmacist)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-037 |
| **Source Entity** | DispensingRecord |
| **Target Entity** | User |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A dispensing event is performed by one pharmacist |
| **Foreign Key** | pharmacistId in DispensingRecord |
| **Owner** | User |
| **Cascade** | Delete User → Prevent (dispensing records) |
| **Nullability** | Required |
| **Constraints** | User must be pharmacist |

---

#### 38. AdministrationRecord → User (Many-to-One, Administrator)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-038 |
| **Source Entity** | AdministrationRecord |
| **Target Entity** | User |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | An administration event is performed by one user |
| **Foreign Key** | administeredBy in AdministrationRecord |
| **Owner** | User |
| **Cascade** | Delete User → Prevent (administration records) |
| **Nullability** | Required |
| **Constraints** | User must have administration privileges |

---

### Hospital Domain Relationships

#### 39. Hospital → Department (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-039 |
| **Source Entity** | Hospital |
| **Target Entity** | Department |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A hospital contains multiple departments |
| **Foreign Key** | hospitalId in Department |
| **Owner** | Hospital |
| **Cascade** | Delete Hospital → Delete Departments |
| **Nullability** | Required (at least one) |
| **Constraints** | None |

---

#### 40. Hospital → Bed (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-040 |
| **Source Entity** | Hospital |
| **Target Entity** | Bed |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A hospital contains multiple beds |
| **Foreign Key** | hospitalId in Bed |
| **Owner** | Hospital |
| **Cascade** | Delete Hospital → Delete Beds |
| **Nullability** | Required |
| **Constraints** | None |

---

#### 41. Department → Bed (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-041 |
| **Source Entity** | Department |
| **Target Entity** | Bed |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A department contains multiple beds |
| **Foreign Key** | departmentId in Bed |
| **Owner** | Department |
| **Cascade** | Delete Department → Delete Beds |
| **Nullability** | Required |
| **Constraints** | None |

---

#### 42. Department → User (Many-to-One, Head)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-042 |
| **Source Entity** | Department |
| **Target Entity** | User |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A department is led by one user |
| **Foreign Key** | headOfDepartment in Department |
| **Owner** | User |
| **Cascade** | Delete User → Set headOfDepartment to null |
| **Nullability** | Optional |
| **Constraints** | User must have leadership role |

---

#### 43. Bed → Patient (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-043 |
| **Source Entity** | Bed |
| **Target Entity** | Patient |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A bed can be assigned to one patient |
| **Foreign Key** | patientId in Bed |
| **Owner** | Bed |
| **Cascade** | Delete Patient → Free bed |
| **Nullability** | Optional |
| **Constraints** | Bed must be available |

---

### Scheduling Domain Relationships

#### 44. Appointment → Patient (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-044 |
| **Source Entity** | Appointment |
| **Target Entity** | Patient |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | An appointment belongs to one patient |
| **Foreign Key** | patientId in Appointment |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Delete Appointments |
| **Nullability** | Required |
| **Constraints** | Patient must be active |

---

#### 45. Appointment → User (Many-to-One, Provider)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-045 |
| **Source Entity** | Appointment |
| **Target Entity** | User |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | An appointment is with one provider |
| **Foreign Key** | providerId in Appointment |
| **Owner** | User |
| **Cascade** | Delete User → Cancel Appointments |
| **Nullability** | Required |
| **Constraints** | User must have provider role |

---

#### 46. Appointment → Encounter (One-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-046 |
| **Source Entity** | Appointment |
| **Target Entity** | Encounter |
| **Relationship Type** | One-to-One |
| **Cardinality** | 1:1 |
| **Description** | An appointment can generate one encounter |
| **Foreign Key** | appointmentId in Encounter |
| **Owner** | Appointment |
| **Cascade** | Delete Appointment → Delete Encounter |
| **Nullability** | Optional (encounter created at check-in) |
| **Constraints** | Encounter must be scheduled |

---

### Finance Domain Relationships

#### 47. FinancialTransaction → Patient (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-047 |
| **Source Entity** | FinancialTransaction |
| **Target Entity** | Patient |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A financial transaction belongs to one patient |
| **Foreign Key** | patientId in FinancialTransaction |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Prevent (transactions exist) |
| **Nullability** | Required |
| **Constraints** | Patient must exist |

---

#### 48. FinancialTransaction → Encounter (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-048 |
| **Source Entity** | FinancialTransaction |
| **Target Entity** | Encounter |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A financial transaction is associated with one encounter |
| **Foreign Key** | encounterId in FinancialTransaction |
| **Owner** | Encounter |
| **Cascade** | Delete Encounter → Prevent (transactions exist) |
| **Nullability** | Optional |
| **Constraints** | Encounter must exist |

---

#### 49. FinancialTransaction → User (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-049 |
| **Source Entity** | FinancialTransaction |
| **Target Entity** | User |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A financial transaction is created by one user |
| **Foreign Key** | createdBy in FinancialTransaction |
| **Owner** | User |
| **Cascade** | Delete User → Prevent (transactions exist) |
| **Nullability** | Required |
| **Constraints** | User must have financial access |

---

#### 50. Claim → Patient (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-050 |
| **Source Entity** | Claim |
| **Target Entity** | Patient |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A claim belongs to one patient |
| **Foreign Key** | patientId in Claim |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Prevent (claims exist) |
| **Nullability** | Required |
| **Constraints** | Patient must exist |

---

#### 51. Claim → Encounter (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-051 |
| **Source Entity** | Claim |
| **Target Entity** | Encounter |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A claim is for one encounter |
| **Foreign Key** | encounterId in Claim |
| **Owner** | Encounter |
| **Cascade** | Delete Encounter → Prevent (claims exist) |
| **Nullability** | Required |
| **Constraints** | Encounter must be completed |

---

#### 52. Claim → InsurancePlan (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-052 |
| **Source Entity** | Claim |
| **Target Entity** | InsurancePlan |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A claim is submitted to one insurance plan |
| **Foreign Key** | insurancePlanId in Claim |
| **Owner** | InsurancePlan |
| **Cascade** | Delete InsurancePlan → Prevent (claims exist) |
| **Nullability** | Required |
| **Constraints** | Plan must be active |

---

#### 53. Claim → ClaimItem (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-053 |
| **Source Entity** | Claim |
| **Target Entity** | ClaimItem |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A claim contains multiple line items |
| **Foreign Key** | claimId in ClaimItem |
| **Owner** | Claim |
| **Cascade** | Delete Claim → Delete ClaimItems |
| **Nullability** | Required (at least one) |
| **Constraints** | Items must sum to claim total |

---

#### 54. Claim → FinancialTransaction (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-054 |
| **Source Entity** | Claim |
| **Target Entity** | FinancialTransaction |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A claim has associated financial transactions |
| **Foreign Key** | claimId in FinancialTransaction |
| **Owner** | Claim |
| **Cascade** | Delete Claim → Prevent (transactions exist) |
| **Nullability** | Optional |
| **Constraints** | None |

---

#### 55. Payment → Patient (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-055 |
| **Source Entity** | Payment |
| **Target Entity** | Patient |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A payment is for one patient |
| **Foreign Key** | patientId in Payment |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Prevent (payments exist) |
| **Nullability** | Required |
| **Constraints** | Patient must exist |

---

#### 56. Payment → FinancialTransaction (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-056 |
| **Source Entity** | Payment |
| **Target Entity** | FinancialTransaction |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A payment has associated financial transactions |
| **Foreign Key** | paymentId in FinancialTransaction |
| **Owner** | Payment |
| **Cascade** | Delete Payment → Delete FinancialTransactions |
| **Nullability** | Required |
| **Constraints** | None |

---

#### 57. Payment → PaymentApplication (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-057 |
| **Source Entity** | Payment |
| **Target Entity** | PaymentApplication |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A payment can be applied to multiple claims |
| **Foreign Key** | paymentId in PaymentApplication |
| **Owner** | Payment |
| **Cascade** | Delete Payment → Delete PaymentApplications |
| **Nullability** | Optional |
| **Constraints** | Total applied cannot exceed payment amount |

---

### Medical Device Domain Relationships

#### 58. MedicalDevice → Department (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-058 |
| **Source Entity** | MedicalDevice |
| **Target Entity** | Department |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A device is located in one department |
| **Foreign Key** | locationId in MedicalDevice |
| **Owner** | Department |
| **Cascade** | Delete Department → Reassign devices |
| **Nullability** | Required |
| **Constraints** | Department must be active |

---

#### 59. MedicalDevice → DeviceMaintenance (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-059 |
| **Source Entity** | MedicalDevice |
| **Target Entity** | DeviceMaintenance |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A device can have multiple maintenance records |
| **Foreign Key** | deviceId in DeviceMaintenance |
| **Owner** | MedicalDevice |
| **Cascade** | Delete MedicalDevice → Delete DeviceMaintenances |
| **Nullability** | Optional |
| **Constraints** | None |

---

#### 60. MedicalDevice → DeviceCalibration (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-060 |
| **Source Entity** | MedicalDevice |
| **Target Entity** | DeviceCalibration |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A device can have multiple calibration records |
| **Foreign Key** | deviceId in DeviceCalibration |
| **Owner** | MedicalDevice |
| **Cascade** | Delete MedicalDevice → Delete DeviceCalibrations |
| **Nullability** | Optional |
| **Constraints** | None |

---

### Notification Domain Relationships

#### 61. Notification → User (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-061 |
| **Source Entity** | Notification |
| **Target Entity** | User |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A notification is sent to one user |
| **Foreign Key** | userId in Notification |
| **Owner** | User |
| **Cascade** | Delete User → Delete Notifications |
| **Nullability** | Required |
| **Constraints** | User must exist |

---

### Document Domain Relationships

#### 62. Document → User (Many-to-One, Owner)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-062 |
| **Source Entity** | Document |
| **Target Entity** | User |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A document is owned by one user |
| **Foreign Key** | ownerId in Document |
| **Owner** | User |
| **Cascade** | Delete User → Reassign ownership |
| **Nullability** | Required |
| **Constraints** | User must exist |

---

#### 63. Document → Patient (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-063 |
| **Source Entity** | Document |
| **Target Entity** | Patient |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A document can be associated with one patient |
| **Foreign Key** | patientId in Document |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Prevent (documents exist) |
| **Nullability** | Optional |
| **Constraints** | Patient must exist |

---

#### 64. Document → Encounter (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-064 |
| **Source Entity** | Document |
| **Target Entity** | Encounter |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A document can be associated with one encounter |
| **Foreign Key** | encounterId in Document |
| **Owner** | Encounter |
| **Cascade** | Delete Encounter → Prevent (documents exist) |
| **Nullability** | Optional |
| **Constraints** | Encounter must exist |

---

#### 65. Document → DocumentVersion (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-065 |
| **Source Entity** | Document |
| **Target Entity** | DocumentVersion |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A document can have multiple versions |
| **Foreign Key** | documentId in DocumentVersion |
| **Owner** | Document |
| **Cascade** | Delete Document → Delete DocumentVersions |
| **Nullability** | Required (at least one) |
| **Constraints** | Versions must be sequential |

---

#### 66. Document → DocumentAccess (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-066 |
| **Source Entity** | Document |
| **Target Entity** | DocumentAccess |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A document has access control entries |
| **Foreign Key** | documentId in DocumentAccess |
| **Owner** | Document |
| **Cascade** | Delete Document → Delete DocumentAccesses |
| **Nullability** | Optional |
| **Constraints** | None |

---

### Workflow Domain Relationships

#### 67. Workflow → User (Many-to-One, Initiator)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-067 |
| **Source Entity** | Workflow |
| **Target Entity** | User |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A workflow is initiated by one user |
| **Foreign Key** | initiatedBy in Workflow |
| **Owner** | User |
| **Cascade** | Delete User → Prevent (workflows exist) |
| **Nullability** | Required |
| **Constraints** | User must exist |

---

#### 68. Workflow → Patient (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-068 |
| **Source Entity** | Workflow |
| **Target Entity** | Patient |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A workflow can be associated with one patient |
| **Foreign Key** | patientId in Workflow |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Cancel Workflows |
| **Nullability** | Optional |
| **Constraints** | Patient must exist |

---

#### 69. Workflow → WorkflowStep (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-069 |
| **Source Entity** | Workflow |
| **Target Entity** | WorkflowStep |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A workflow contains multiple steps |
| **Foreign Key** | workflowId in WorkflowStep |
| **Owner** | Workflow |
| **Cascade** | Delete Workflow → Delete WorkflowSteps |
| **Nullability** | Required (at least one) |
| **Constraints** | Steps must be sequential |

---

#### 70. Workflow → Task (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-070 |
| **Source Entity** | Workflow |
| **Target Entity** | Task |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A workflow has multiple tasks |
| **Foreign Key** | workflowId in Task |
| **Owner** | Workflow |
| **Cascade** | Delete Workflow → Delete Tasks |
| **Nullability** | Optional |
| **Constraints** | None |

---

#### 71. Task → User (Many-to-One, Assignee)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-071 |
| **Source Entity** | Task |
| **Target Entity** | User |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A task is assigned to one user |
| **Foreign Key** | assignedTo in Task |
| **Owner** | User |
| **Cascade** | Delete User → Reassign Tasks |
| **Nullability** | Optional |
| **Constraints** | User must exist |

---

#### 72. Task → User (Many-to-One, Completer)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-072 |
| **Source Entity** | Task |
| **Target Entity** | User |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A task is completed by one user |
| **Foreign Key** | completedBy in Task |
| **Owner** | User |
| **Cascade** | Delete User → Prevent (completed tasks) |
| **Nullability** | Optional |
| **Constraints** | User must exist |

---

### Reporting Domain Relationships

#### 73. Report → User (Many-to-One, Generator)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-073 |
| **Source Entity** | Report |
| **Target Entity** | User |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A report is generated by one user |
| **Foreign Key** | generatedBy in Report |
| **Owner** | User |
| **Cascade** | Delete User → Prevent (reports exist) |
| **Nullability** | Required |
| **Constraints** | User must have reporting access |

---

#### 74. Report → ReportSchedule (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-074 |
| **Source Entity** | Report |
| **Target Entity** | ReportSchedule |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A report can be generated from a schedule |
| **Foreign Key** | reportScheduleId in Report |
| **Owner** | ReportSchedule |
| **Cascade** | Delete ReportSchedule → Prevent (reports exist) |
| **Nullability** | Optional |
| **Constraints** | Schedule must be active |

---

### Insurance Domain Relationships

#### 75. InsurancePlan → InsuranceCoverage (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-075 |
| **Source Entity** | InsurancePlan |
| **Target Entity** | InsuranceCoverage |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | An insurance plan has multiple coverage records |
| **Foreign Key** | planId in InsuranceCoverage |
| **Owner** | InsurancePlan |
| **Cascade** | Delete InsurancePlan → Delete InsuranceCoverages |
| **Nullability** | Optional |
| **Constraints** | Coverage must be active |

---

#### 76. InsurancePlan → Claim (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-076 |
| **Source Entity** | InsurancePlan |
| **Target Entity** | Claim |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | An insurance plan has multiple claims |
| **Foreign Key** | insurancePlanId in Claim |
| **Owner** | InsurancePlan |
| **Cascade** | Delete InsurancePlan → Prevent (claims exist) |
| **Nullability** | Optional |
| **Constraints** | Claims must be processed |

---

### Public Health Domain Relationships

#### 77. Patient → DiseaseReport (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-077 |
| **Source Entity** | Patient |
| **Target Entity** | DiseaseReport |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A patient can have multiple disease reports |
| **Foreign Key** | patientId in DiseaseReport |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Prevent (disease reports exist) |
| **Nullability** | Optional |
| **Constraints** | Reports must be submitted |

---

#### 78. Patient → Immunization (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-078 |
| **Source Entity** | Patient |
| **Target Entity** | Immunization |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A patient has immunization records |
| **Foreign Key** | patientId in Immunization |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Delete Immunizations |
| **Nullability** | Optional |
| **Constraints** | None |

---

### Quality & Safety Domain Relationships

#### 79. Encounter → SafetyEvent (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-079 |
| **Source Entity** | Encounter |
| **Target Entity** | SafetyEvent |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | An encounter can have multiple safety events |
| **Foreign Key** | encounterId in SafetyEvent |
| **Owner** | Encounter |
| **Cascade** | Delete Encounter → Prevent (safety events exist) |
| **Nullability** | Optional |
| **Constraints** | Events must be investigated |

---

#### 80. SafetyEvent → CorrectiveAction (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-080 |
| **Source Entity** | SafetyEvent |
| **Target Entity** | CorrectiveAction |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A safety event can have multiple corrective actions |
| **Foreign Key** | safetyEventId in CorrectiveAction |
| **Owner** | SafetyEvent |
| **Cascade** | Delete SafetyEvent → Delete CorrectiveActions |
| **Nullability** | Optional |
| **Constraints** | Actions must be completed |

---

### Analytics Domain Relationships

#### 81. AnalyticsDataset → DataSource (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-081 |
| **Source Entity** | AnalyticsDataset |
| **Target Entity** | DataSource |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A dataset comes from one data source |
| **Foreign Key** | dataSourceId in AnalyticsDataset |
| **Owner** | DataSource |
| **Cascade** | Delete DataSource → Disable Datasets |
| **Nullability** | Required |
| **Constraints** | Source must be active |

---

#### 82. AnalyticsDataset → DataPipeline (Many-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-082 |
| **Source Entity** | AnalyticsDataset |
| **Target Entity** | DataPipeline |
| **Relationship Type** | Many-to-One |
| **Cardinality** | N:1 |
| **Description** | A dataset is processed by one pipeline |
| **Foreign Key** | pipelineId in AnalyticsDataset |
| **Owner** | DataPipeline |
| **Cascade** | Delete DataPipeline → Disable Datasets |
| **Nullability** | Optional |
| **Constraints** | Pipeline must be active |

---

### Integration Domain Relationships

#### 83. IntegrationEndpoint → Interface (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-083 |
| **Source Entity** | IntegrationEndpoint |
| **Target Entity** | Interface |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | An endpoint can have multiple interfaces |
| **Foreign Key** | endpointId in Interface |
| **Owner** | IntegrationEndpoint |
| **Cascade** | Delete IntegrationEndpoint → Delete Interfaces |
| **Nullability** | Optional |
| **Constraints** | Interfaces must be active |

---

#### 84. Interface → Message (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-084 |
| **Source Entity** | Interface |
| **Target Entity** | Message |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | An interface processes multiple messages |
| **Foreign Key** | interfaceId in Message |
| **Owner** | Interface |
| **Cascade** | Delete Interface → Delete Messages |
| **Nullability** | Optional |
| **Constraints** | Messages must be processed |

---

#### 85. Partner → IntegrationEndpoint (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-085 |
| **Source Entity** | Partner |
| **Target Entity** | IntegrationEndpoint |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A partner can have multiple endpoints |
| **Foreign Key** | partnerId in IntegrationEndpoint |
| **Owner** | Partner |
| **Cascade** | Delete Partner → Delete IntegrationEndpoints |
| **Nullability** | Optional |
| **Constraints** | Partner must be active |

---

### Configuration Domain Relationships

#### 86. TenantConfiguration → FeatureFlag (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-086 |
| **Source Entity** | TenantConfiguration |
| **Target Entity** | FeatureFlag |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A tenant can have multiple feature flags |
| **Foreign Key** | tenantId in FeatureFlag |
| **Owner** | TenantConfiguration |
| **Cascade** | Delete TenantConfiguration → Delete FeatureFlags |
| **Nullability** | Optional |
| **Constraints** | Flags must be tenant-specific |

---

### Cross-Domain Relationships

#### 87. Patient → TelehealthVisit (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-087 |
| **Source Entity** | Patient |
| **Target Entity** | TelehealthVisit |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A patient can have multiple telehealth visits |
| **Foreign Key** | patientId in TelehealthVisit |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Delete TelehealthVisits |
| **Nullability** | Optional |
| **Constraints** | Patient must be active |

---

#### 88. User → CareTeam (Many-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-088 |
| **Source Entity** | User |
| **Target Entity** | CareTeam |
| **Relationship Type** | Many-to-Many |
| **Cardinality** | M:N |
| **Description** | Users can be part of multiple care teams |
| **Junction Table** | CareTeamMember |
| **Foreign Keys** | userId, careTeamId |
| **Owner** | Both |
| **Cascade** | Delete User → Remove from CareTeams |
| **Nullability** | Required |
| **Constraints** | User must have clinical role |

---

#### 89. Patient → CareTeam (Many-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-089 |
| **Source Entity** | Patient |
| **Target Entity** | CareTeam |
| **Relationship Type** | Many-to-Many |
| **Cardinality** | M:N |
| **Description** | Patients can be assigned to multiple care teams |
| **Junction Table** | CareTeamPatient |
| **Foreign Keys** | patientId, careTeamId |
| **Owner** | Both |
| **Cascade** | Delete Patient → Remove from CareTeams |
| **Nullability** | Required |
| **Constraints** | Patient must be active |

---

#### 90. Order → Result (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-090 |
| **Source Entity** | Order |
| **Target Entity** | Result |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | An order can have multiple results |
| **Foreign Key** | orderId in Result |
| **Owner** | Order |
| **Cascade** | Delete Order → Delete Results |
| **Nullability** | Optional |
| **Constraints** | Results must be verified |

---

#### 91. Encounter → Appointment (One-to-One)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-091 |
| **Source Entity** | Encounter |
| **Target Entity** | Appointment |
| **Relationship Type** | One-to-One |
| **Cardinality** | 1:1 |
| **Description** | An encounter is linked to one appointment |
| **Foreign Key** | encounterId in Appointment |
| **Owner** | Appointment |
| **Cascade** | Delete Encounter → Delete Appointment |
| **Nullability** | Optional |
| **Constraints** | Appointment must be completed |

---

#### 92. Patient → CarePlan (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-092 |
| **Source Entity** | Patient |
| **Target Entity** | CarePlan |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A patient can have multiple care plans |
| **Foreign Key** | patientId in CarePlan |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Delete CarePlans |
| **Nullability** | Optional |
| **Constraints** | Only one active care plan per condition |

---

#### 93. CarePlan → CarePlanGoal (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-093 |
| **Source Entity** | CarePlan |
| **Target Entity** | CarePlanGoal |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A care plan has multiple goals |
| **Foreign Key** | carePlanId in CarePlanGoal |
| **Owner** | CarePlan |
| **Cascade** | Delete CarePlan → Delete CarePlanGoals |
| **Nullability** | Required (at least one) |
| **Constraints** | Goals must be measurable |

---

#### 94. CarePlan → CarePlanTask (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-094 |
| **Source Entity** | CarePlan |
| **Target Entity** | CarePlanTask |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A care plan has multiple tasks |
| **Foreign Key** | carePlanId in CarePlanTask |
| **Owner** | CarePlan |
| **Cascade** | Delete CarePlan → Delete CarePlanTasks |
| **Nullability** | Optional |
| **Constraints** | Tasks must have due dates |

---

#### 95. Patient → ClinicalTrial (Many-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-095 |
| **Source Entity** | Patient |
| **Target Entity** | ClinicalTrial |
| **Relationship Type** | Many-to-Many |
| **Cardinality** | M:N |
| **Description** | Patients can enroll in multiple clinical trials |
| **Junction Table** | Enrollment |
| **Foreign Keys** | patientId, trialId |
| **Owner** | Both |
| **Cascade** | Delete Patient → Remove from Trials |
| **Nullability** | Optional |
| **Constraints** | Consent must be obtained |

---

### Additional Relationships

#### 96. Medication → DrugInteraction (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-096 |
| **Source Entity** | Medication |
| **Target Entity** | DrugInteraction |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A medication can have multiple drug interactions |
| **Foreign Key** | medicationId in DrugInteraction |
| **Owner** | Medication |
| **Cascade** | Delete Medication → Delete DrugInteractions |
| **Nullability** | Optional |
| **Constraints** | Interactions must be current |

---

#### 97. Specimen → SpecimenProcessing (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-097 |
| **Source Entity** | Specimen |
| **Target Entity** | SpecimenProcessing |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A specimen can have multiple processing steps |
| **Foreign Key** | specimenId in SpecimenProcessing |
| **Owner** | Specimen |
| **Cascade** | Delete Specimen → Delete SpecimenProcessings |
| **Nullability** | Optional |
| **Constraints** | Processing must be in order |

---

#### 98. Order → OrderHistory (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-098 |
| **Source Entity** | Order |
| **Target Entity** | OrderHistory |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | An order has status history |
| **Foreign Key** | orderId in OrderHistory |
| **Owner** | Order |
| **Cascade** | Delete Order → Delete OrderHistories |
| **Nullability** | Required |
| **Constraints** | History is immutable |

---

#### 99. Encounter → EncounterHistory (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-099 |
| **Source Entity** | Encounter |
| **Target Entity** | EncounterHistory |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | An encounter has status history |
| **Foreign Key** | encounterId in EncounterHistory |
| **Owner** | Encounter |
| **Cascade** | Delete Encounter → Delete EncounterHistories |
| **Nullability** | Required |
| **Constraints** | History is immutable |

---

#### 100. Patient → PatientHistory (One-to-Many)

| Attribute | Value |
|-----------|-------|
| **Relationship ID** | REL-100 |
| **Source Entity** | Patient |
| **Target Entity** | PatientHistory |
| **Relationship Type** | One-to-Many |
| **Cardinality** | 1:N |
| **Description** | A patient has demographic history |
| **Foreign Key** | patientId in PatientHistory |
| **Owner** | Patient |
| **Cascade** | Delete Patient → Delete PatientHistories |
| **Nullability** | Required |
| **Constraints** | History is immutable |

---

### Remaining Relationships (101-120)

#### 101-110: Additional Domain Relationships

| Rel ID | Source | Target | Type | Cardinality | Description |
|--------|--------|--------|------|-------------|-------------|
| REL-101 | User | NotificationPreference | One-to-One | 1:1 | User notification preferences |
| REL-102 | Patient | PatientMessage | One-to-Many | 1:N | Patient messages |
| REL-103 | User | PatientMessage | One-to-Many | 1:N | Provider messages |
| REL-104 | Encounter | Handoff | One-to-Many | 1:N | Care handoffs |
| REL-105 | Workflow | Escalation | One-to-Many | 1:N | Workflow escalations |
| REL-106 | Task | TaskHistory | One-to-Many | 1:N | Task status history |
| REL-107 | Claim | Appeal | One-to-Many | 1:N | Claim appeals |
| REL-108 | Payment | Refund | One-to-One | 1:1 | Payment refunds |
| REL-109 | Report | ReportDistribution | One-to-Many | 1:N | Report recipients |
| REL-110 | AnalyticsModel | ModelVersion | One-to-Many | 1:N | Model versions |

#### 111-120: System-Level Relationships

| Rel ID | Source | Target | Type | Cardinality | Description |
|--------|--------|--------|------|-------------|-------------|
| REL-111 | FeatureFlag | FeatureFlagHistory | One-to-Many | 1:N | Flag change history |
| REL-112 | SystemConfiguration | ConfigurationHistory | One-to-Many | 1:N | Config history |
| REL-113 | TenantConfiguration | TenantFeatureFlag | One-to-Many | 1:N | Tenant feature flags |
| REL-114 | IntegrationEndpoint | ErrorLog | One-to-Many | 1:N | Integration errors |
| REL-115 | Interface | Message | One-to-Many | 1:N | Interface messages |
| REL-116 | Message | MessageStatus | One-to-Many | 1:N | Message statuses |
| REL-117 | Partner | PartnerAgreement | One-to-Many | 1:N | Partner agreements |
| REL-118 | KnowledgeArticle | KnowledgeVersion | One-to-Many | 1:N | Article versions |
| REL-119 | CDSDeployment | CDSTrigger | One-to-Many | 1:N | CDS triggers |
| REL-120 | Policy | PolicyVersion | One-to-Many | 1:N | Policy versions |

---

## Relationship Patterns

### 1. Identifying Relationship Pattern

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      IDENTIFYING RELATIONSHIP PATTERN                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Parent Entity (Strong)     Child Entity (Weak)                                │
│  ┌────────────────────┐     ┌────────────────────┐                             │
│  │       Order        │     │     OrderItem      │                             │
│  ├────────────────────┤     ├────────────────────┤                             │
│  │ orderId (PK)       │────►│ orderItemId (PK)   │                             │
│  │ orderNumber        │     │ orderId (FK, PK)   │                             │
│  │ patientId          │     │ lineNumber         │                             │
│  └────────────────────┘     │ itemDescription    │                             │
│                              └────────────────────┘                             │
│                                                                                 │
│  Characteristics:                                                              │
│  - Child cannot exist without parent                                           │
│  - Child primary key includes parent primary key                               │
│  - Cascade delete parent → delete child                                        │
│  - Examples: Order → OrderItem, Encounter → VitalSigns                         │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2. Non-Identifying Relationship Pattern

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    NON-IDENTIFYING RELATIONSHIP PATTERN                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Parent Entity (Independent)   Child Entity (Independent)                     │
│  ┌────────────────────┐        ┌────────────────────┐                          │
│  │      Patient       │        │     Encounter      │                          │
│  ├────────────────────┤        ├────────────────────┤                          │
│  │ patientId (PK)     │◄───────│ encounterId (PK)   │                          │
│  │ mrn                │        │ patientId (FK)     │                          │
│  │ firstName          │        │ encounterType      │                          │
│  └────────────────────┘        │ scheduledDateTime  │                          │
│                                 └────────────────────┘                          │
│                                                                                 │
│  Characteristics:                                                              │
│  - Child can exist without parent                                              │
│  - Child has its own primary key                                               │
│  - Foreign key in child references parent                                      │
│  - Examples: Patient → Encounter, Department → Bed                             │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 3. Many-to-Many Relationship Pattern

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     MANY-TO-MANY RELATIONSHIP PATTERN                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Entity A                Junction Table              Entity B                  │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐       │
│  │       Role         │  │  RolePermission    │  │    Permission      │       │
│  ├────────────────────┤  ├────────────────────┤  ├────────────────────┤       │
│  │ roleId (PK)        │──│ roleId (FK)        │  │ permissionId (PK)  │       │
│  │ roleName           │  │ permissionId (FK)  │──│ permissionName     │       │
│  └────────────────────┘  │ grantedAt          │  │ resource           │       │
│                           │ grantedBy          │  │ action             │       │
│                           └────────────────────┘  └────────────────────┘       │
│                                                                                 │
│  Characteristics:                                                              │
│  - Junction table has composite primary key                                    │
│  - Additional attributes on junction table possible                            │
│  - Cascade delete both → delete junction rows                                  │
│  - Examples: Role ↔ Permission, Patient ↔ ClinicalTrial                       │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 4. Inheritance Relationship Pattern

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      INHERITANCE RELATIONSHIP PATTERN                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Base Class (Superclass)      Derived Classes (Subclasses)                    │
│  ┌────────────────────┐       ┌────────────────────┐                          │
│  │       Order        │       │     LabOrder       │                          │
│  ├────────────────────┤       ├────────────────────┤                          │
│  │ orderId (PK)       │◄──────│ labOrderId (PK)    │                          │
│  │ orderNumber        │       │ orderId (FK)       │                          │
│  │ encounterId        │       │ labTestCode        │                          │
│  │ patientId          │       │ specimenType       │                          │
│  └────────────────────┘       └────────────────────┘                          │
│           ▲                            ▲                                       │
│           │                            │                                       │
│           │        ┌────────────────────┤                                      │
│           │        │                    │                                      │
│           │        ▼                    ▼                                      │
│           │  ┌────────────────────┐  ┌────────────────────┐                  │
│           │  │ RadiologyOrder     │  │ MedicationOrder    │                  │
│           │  ├────────────────────┤  ├────────────────────┤                  │
│           └──│ radiologyOrderId   │  │ medicationOrderId  │                  │
│              │ orderId (FK)       │  │ orderId (FK)       │                  │
│              │ modality           │  │ medicationId       │                  │
│              └────────────────────┘  └────────────────────┘                  │
│                                                                                 │
│  Implementation Options:                                                       │
│  1. Single Table Inheritance (STI) - Single table, type discriminator         │
│  2. Table Per Type (TPT) - Separate tables, FK to base                       │
│  3. Table Per Concrete (TPC) - Separate tables, duplicate base columns        │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Cardinality Rules

### Cardinality Constraints

| Relationship | Minimum Cardinality | Maximum Cardinality | Business Rule |
|--------------|---------------------|---------------------|---------------|
| Patient → Address | 1 | N | At least one address required |
| Patient → Encounter | 0 | N | No encounters initially |
| Encounter → Patient | 1 | 1 | Always one patient |
| Encounter → VitalSigns | 0 | N | Optional vitals |
| Order → Patient | 1 | 1 | Always one patient |
| Order → Encounter | 1 | 1 | Always one encounter |
| LabOrder → Specimen | 1 | N | At least one specimen |
| Specimen → LabResult | 0 | N | Results optional |
| MedicationOrder → DispensingRecord | 0 | N | Dispensing optional |
| Claim → ClaimItem | 1 | N | At least one line item |
| Payment → PaymentApplication | 0 | N | Applications optional |
| Role → Permission | 1 | N | At least one permission |

### Cardinality Validation Rules

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      CARDINALITY VALIDATION RULES                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  1:1 Relationships                                                             │
│  - Validate uniqueness of foreign key                                          │
│  - Prevent duplicate references                                                │
│  - Enforce mutual existence if required                                        │
│                                                                                 │
│  1:N Relationships                                                             │
│  - Validate foreign key exists                                                 │
│  - Check minimum cardinality on delete                                         │
│  - Enforce maximum cardinality if defined                                      │
│                                                                                 │
│  M:N Relationships                                                             │
│  - Validate junction table entries                                             │
│  - Prevent duplicate associations                                              │
│  - Check referential integrity on both sides                                   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Cascade Rules

### Cascade Actions

| Action | Description | When to Use |
|--------|-------------|-------------|
| **CASCADE** | Delete/Update children | Strong ownership |
| **SET NULL** | Set FK to null | Optional relationship |
| **SET DEFAULT** | Set FK to default | Default exists |
| **RESTRICT** | Prevent deletion | Referential integrity |
| **NO ACTION** | Similar to RESTRICT | Database specific |

### Cascade Configuration

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         CASCADE CONFIGURATION                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Patient (Parent)                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  Delete Patient →                                                       │   │
│  │    • Address: CASCADE (delete all addresses)                            │   │
│  │    • Allergy: CASCADE (delete all allergies)                            │   │
│  │    • Medication: CASCADE (delete all medications)                       │   │
│  │    • Consent: CASCADE (delete all consents)                             │   │
│  │    • Encounter: RESTRICT (prevent if encounters exist)                  │   │
│  │    • Order: RESTRICT (prevent if orders exist)                          │   │
│  │    • FinancialTransaction: RESTRICT (prevent if transactions exist)     │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  Encounter (Parent)                                                            │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  Delete Encounter →                                                     │   │
│  │    • ClinicalDocumentation: CASCADE (delete all documents)              │   │
│  │    • VitalSigns: CASCADE (delete all vitals)                            │   │
│  │    • Diagnosis: CASCADE (delete all diagnoses)                          │   │
│  │    • Order: CASCADE (delete all orders)                                 │   │
│  │    • SafetyEvent: RESTRICT (prevent if safety events exist)             │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  Order (Parent)                                                                │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  Delete Order →                                                         │   │
│  │    • LabOrder: CASCADE (delete lab order)                               │   │
│  │    • RadiologyOrder: CASCADE (delete radiology order)                   │   │
│  │    • MedicationOrder: CASCADE (delete medication order)                 │   │
│  │    • Result: CASCADE (delete all results)                               │   │
│  │    • OrderHistory: CASCADE (delete history)                             │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Relationship Constraints

### Business Constraints

| Constraint Type | Description | Example |
|-----------------|-------------|---------|
| **Uniqueness** | One-to-one enforcement | UserProfile.userId unique |
| **Mandatory** | Required relationship | Encounter.patientId required |
| **Temporal** | Time-based constraints | Appointment must be future |
| **Status** | Status-based constraints | Active patient required |
| **Role** | Role-based constraints | Provider role for orders |
| **Count** | Maximum count constraints | Max 5 sessions per user |

### Referential Integrity

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      REFERENTIAL INTEGRITY RULES                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Foreign Key Validation:                                                       │
│  1. Referenced entity must exist                                               │
│  2. Referenced entity must be active (where applicable)                        │
│  3. Cascade rules must be followed                                             │
│  4. Null foreign keys allowed only where nullable                              │
│                                                                                 │
│  Prevent Orphan Records:                                                       │
│  1. Cannot delete parent if children exist (RESTRICT)                          │
│  2. Cannot create child without valid parent                                   │
│  3. Cannot update foreign key to non-existent parent                           │
│                                                                                 │
│  Data Consistency:                                                             │
│  1. Relationship cardinality must be maintained                                │
│  2. Aggregation boundaries must be respected                                   │
│  3. Domain events must be emitted on state changes                             │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Validation Rules per Relationship

| Relationship | Validation Rule | Error Message |
|--------------|-----------------|---------------|
| Patient → Encounter | Patient must be active | "Patient is not active" |
| Encounter → Patient | Patient must exist | "Patient not found" |
| Order → Encounter | Encounter must be active | "Encounter is completed" |
| LabOrder → Specimen | At least one specimen | "Lab order requires specimen" |
| Claim → ClaimItem | At least one item | "Claim requires line items" |
| Payment → PaymentApplication | Total applied ≤ payment | "Applied amount exceeds payment" |
| Role → Permission | At least one permission | "Role requires permissions" |
| Task → User | Assignee must exist | "Assignee not found" |

---

## Appendix: Relationship Summary Table

| Rel ID | Source Entity | Target Entity | Type | Cardinality | Cascade | Nullable |
|--------|---------------|---------------|------|-------------|---------|----------|
| REL-001 | User | UserProfile | 1:1 | 1:1 | CASCADE | Yes |
| REL-002 | User | UserRoleAssignment | 1:N | 1:N | CASCADE | No |
| REL-003 | Role | UserRoleAssignment | 1:N | 1:N | RESTRICT | No |
| REL-004 | Role | Permission | M:N | M:N | CASCADE | No |
| REL-005 | User | Session | 1:N | 1:N | CASCADE | No |
| REL-006 | User | AuditLog | 1:N | 1:N | RESTRICT | No |
| REL-007 | Patient | Address | 1:N | 1:N | CASCADE | No |
| REL-008 | Patient | Allergy | 1:N | 1:N | CASCADE | Yes |
| REL-009 | Patient | Medication | 1:N | 1:N | CASCADE | Yes |
| REL-010 | Patient | Immunization | 1:N | 1:N | CASCADE | Yes |
| REL-011 | Patient | Consent | 1:N | 1:N | CASCADE | Yes |
| REL-012 | Patient | EmergencyContact | 1:N | 1:N | CASCADE | No |
| REL-013 | Patient | InsurancePolicy | 1:N | 1:N | CASCADE | Yes |
| REL-014 | Patient | PatientIdentifier | 1:N | 1:N | CASCADE | No |
| REL-015 | Patient | Encounter | 1:N | 1:N | RESTRICT | No |
| REL-016 | Encounter | ClinicalDocumentation | 1:N | 1:N | CASCADE | Yes |
| REL-017 | Encounter | VitalSigns | 1:N | 1:N | CASCADE | Yes |
| REL-018 | Encounter | Diagnosis | 1:N | 1:N | CASCADE | Yes |
| REL-019 | Encounter | Order | 1:N | 1:N | CASCADE | Yes |
| REL-020 | Encounter | Department | N:1 | N:1 | RESTRICT | No |
| REL-021 | Encounter | Hospital | N:1 | N:1 | RESTRICT | No |
| REL-022 | Order | Patient | N:1 | N:1 | RESTRICT | No |
| REL-023 | Order | User | N:1 | N:1 | RESTRICT | No |
| REL-024 | LabOrder | Specimen | 1:N | 1:N | CASCADE | No |
| REL-025 | LabOrder | LabResult | 1:N | 1:N | CASCADE | Yes |
| REL-026 | Specimen | LabResult | 1:N | 1:N | CASCADE | Yes |
| REL-027 | Specimen | User | N:1 | N:1 | RESTRICT | No |
| REL-028 | RadiologyOrder | ImagingStudy | 1:1 | 1:1 | CASCADE | Yes |
| REL-029 | RadiologyOrder | RadiologyReport | 1:1 | 1:1 | CASCADE | Yes |
| REL-030 | ImagingStudy | Image | 1:N | 1:N | CASCADE | No |
| REL-031 | ImagingStudy | RadiologyReport | 1:1 | 1:1 | CASCADE | Yes |
| REL-032 | RadiologyReport | User | N:1 | N:1 | RESTRICT | No |
| REL-033 | MedicationOrder | Medication | N:1 | N:1 | RESTRICT | No |
| REL-034 | MedicationOrder | DispensingRecord | 1:N | 1:N | CASCADE | Yes |
| REL-035 | MedicationOrder | AdministrationRecord | 1:N | 1:N | CASCADE | Yes |
| REL-036 | DispensingRecord | Pharmacy | N:1 | N:1 | RESTRICT | No |
| REL-037 | DispensingRecord | User | N:1 | N:1 | RESTRICT | No |
| REL-038 | AdministrationRecord | User | N:1 | N:1 | RESTRICT | No |
| REL-039 | Hospital | Department | 1:N | 1:N | CASCADE | No |
| REL-040 | Hospital | Bed | 1:N | 1:N | CASCADE | No |
| REL-041 | Department | Bed | 1:N | 1:N | CASCADE | No |
| REL-042 | Department | User | N:1 | N:1 | SET NULL | Yes |
| REL-043 | Bed | Patient | N:1 | N:1 | SET NULL | Yes |
| REL-044 | Appointment | Patient | N:1 | N:1 | CASCADE | No |
| REL-045 | Appointment | User | N:1 | N:1 | CASCADE | No |
| REL-046 | Appointment | Encounter | 1:1 | 1:1 | CASCADE | Yes |
| REL-047 | FinancialTransaction | Patient | N:1 | N:1 | RESTRICT | No |
| REL-048 | FinancialTransaction | Encounter | N:1 | N:1 | RESTRICT | Yes |
| REL-049 | FinancialTransaction | User | N:1 | N:1 | RESTRICT | No |
| REL-050 | Claim | Patient | N:1 | N:1 | RESTRICT | No |
| REL-051 | Claim | Encounter | N:1 | N:1 | RESTRICT | No |
| REL-052 | Claim | InsurancePlan | N:1 | N:1 | RESTRICT | No |
| REL-053 | Claim | ClaimItem | 1:N | 1:N | CASCADE | No |
| REL-054 | Claim | FinancialTransaction | 1:N | 1:N | RESTRICT | Yes |
| REL-055 | Payment | Patient | N:1 | N:1 | RESTRICT | No |
| REL-056 | Payment | FinancialTransaction | 1:N | 1:N | CASCADE | No |
| REL-057 | Payment | PaymentApplication | 1:N | 1:N | CASCADE | Yes |
| REL-058 | MedicalDevice | Department | N:1 | N:1 | SET NULL | No |
| REL-059 | MedicalDevice | DeviceMaintenance | 1:N | 1:N | CASCADE | Yes |
| REL-060 | MedicalDevice | DeviceCalibration | 1:N | 1:N | CASCADE | Yes |
| REL-061 | Notification | User | N:1 | N:1 | CASCADE | No |
| REL-062 | Document | User | N:1 | N:1 | SET NULL | No |
| REL-063 | Document | Patient | N:1 | N:1 | RESTRICT | Yes |
| REL-064 | Document | Encounter | N:1 | N:1 | RESTRICT | Yes |
| REL-065 | Document | DocumentVersion | 1:N | 1:N | CASCADE | No |
| REL-066 | Document | DocumentAccess | 1:N | 1:N | CASCADE | Yes |
| REL-067 | Workflow | User | N:1 | N:1 | RESTRICT | No |
| REL-068 | Workflow | Patient | N:1 | N:1 | CASCADE | Yes |
| REL-069 | Workflow | WorkflowStep | 1:N | 1:N | CASCADE | No |
| REL-070 | Workflow | Task | 1:N | 1:N | CASCADE | Yes |
| REL-071 | Task | User | N:1 | N:1 | SET NULL | Yes |
| REL-072 | Task | User | N:1 | N:1 | RESTRICT | Yes |
| REL-073 | Report | User | N:1 | N:1 | RESTRICT | No |
| REL-074 | Report | ReportSchedule | N:1 | N:1 | RESTRICT | Yes |
| REL-075 | InsurancePlan | InsuranceCoverage | 1:N | 1:N | CASCADE | Yes |
| REL-076 | InsurancePlan | Claim | 1:N | 1:N | RESTRICT | Yes |
| REL-077 | Patient | DiseaseReport | 1:N | 1:N | RESTRICT | Yes |
| REL-078 | Patient | Immunization | 1:N | 1:N | CASCADE | Yes |
| REL-079 | Encounter | SafetyEvent | 1:N | 1:N | RESTRICT | Yes |
| REL-080 | SafetyEvent | CorrectiveAction | 1:N | 1:N | CASCADE | Yes |
| REL-081 | AnalyticsDataset | DataSource | N:1 | N:1 | RESTRICT | No |
| REL-082 | AnalyticsDataset | DataPipeline | N:1 | N:1 | RESTRICT | Yes |
| REL-083 | IntegrationEndpoint | Interface | 1:N | 1:N | CASCADE | Yes |
| REL-084 | Interface | Message | 1:N | 1:N | CASCADE | Yes |
| REL-085 | Partner | IntegrationEndpoint | 1:N | 1:N | CASCADE | Yes |
| REL-086 | TenantConfiguration | FeatureFlag | 1:N | 1:N | CASCADE | Yes |
| REL-087 | Patient | TelehealthVisit | 1:N | 1:N | CASCADE | Yes |
| REL-088 | User | CareTeam | M:N | M:N | RESTRICT | No |
| REL-089 | Patient | CareTeam | M:N | M:N | RESTRICT | No |
| REL-090 | Order | Result | 1:N | 1:N | CASCADE | Yes |
| REL-091 | Encounter | Appointment | 1:1 | 1:1 | CASCADE | Yes |
| REL-092 | Patient | CarePlan | 1:N | 1:N | CASCADE | Yes |
| REL-093 | CarePlan | CarePlanGoal | 1:N | 1:N | CASCADE | No |
| REL-094 | CarePlan | CarePlanTask | 1:N | 1:N | CASCADE | Yes |
| REL-095 | Patient | ClinicalTrial | M:N | M:N | RESTRICT | Yes |
| REL-096 | Medication | DrugInteraction | 1:N | 1:N | CASCADE | Yes |
| REL-097 | Specimen | SpecimenProcessing | 1:N | 1:N | CASCADE | Yes |
| REL-098 | Order | OrderHistory | 1:N | 1:N | CASCADE | No |
| REL-099 | Encounter | EncounterHistory | 1:N | 1:N | CASCADE | No |
| REL-100 | Patient | PatientHistory | 1:N | 1:N | CASCADE | No |
| REL-101 | User | NotificationPreference | 1:1 | 1:1 | CASCADE | Yes |
| REL-102 | Patient | PatientMessage | 1:N | 1:N | CASCADE | Yes |
| REL-103 | User | PatientMessage | 1:N | 1:N | CASCADE | Yes |
| REL-104 | Encounter | Handoff | 1:N | 1:N | CASCADE | Yes |
| REL-105 | Workflow | Escalation | 1:N | 1:N | CASCADE | Yes |
| REL-106 | Task | TaskHistory | 1:N | 1:N | CASCADE | No |
| REL-107 | Claim | Appeal | 1:N | 1:N | CASCADE | Yes |
| REL-108 | Payment | Refund | 1:1 | 1:1 | CASCADE | Yes |
| REL-109 | Report | ReportDistribution | 1:N | 1:N | CASCADE | Yes |
| REL-110 | AnalyticsModel | ModelVersion | 1:N | 1:N | CASCADE | No |
| REL-111 | FeatureFlag | FeatureFlagHistory | 1:N | 1:N | CASCADE | No |
| REL-112 | SystemConfiguration | ConfigurationHistory | 1:N | 1:N | CASCADE | No |
| REL-113 | TenantConfiguration | TenantFeatureFlag | 1:N | 1:N | CASCADE | Yes |
| REL-114 | IntegrationEndpoint | ErrorLog | 1:N | 1:N | CASCADE | Yes |
| REL-115 | Interface | Message | 1:N | 1:N | CASCADE | Yes |
| REL-116 | Message | MessageStatus | 1:N | 1:N | CASCADE | No |
| REL-117 | Partner | PartnerAgreement | 1:N | 1:N | CASCADE | Yes |
| REL-118 | KnowledgeArticle | KnowledgeVersion | 1:N | 1:N | CASCADE | No |
| REL-119 | CDSDeployment | CDSTrigger | 1:N | 1:N | CASCADE | Yes |
| REL-120 | Policy | PolicyVersion | 1:N | 1:N | CASCADE | No |

---

**Document Classification:** CANONICAL CATALOG  
**Review Cycle:** Quarterly  
**Next Review Date:** 2026-09-25  
**Approved By:** NHDOS Architecture Board