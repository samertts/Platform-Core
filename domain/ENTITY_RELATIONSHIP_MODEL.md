# National Healthcare Digital Operating System (NHDOS) - Entity Relationship Model

**Version:** 1.0.0  
**Status:** CANONICAL MODEL  
**Last Updated:** 2026-06-25  
**Classification:** Production-Ready Documentation

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Entity Modeling Conventions](#entity-modeling-conventions)
3. [Core Entity Definitions](#core-entity-definitions)
4. [Entity Relationship Diagrams](#entity-relationship-diagrams)
5. [Relationship Patterns](#relationship-patterns)
6. [Aggregate Root Definitions](#aggregate-root-definitions)
7. [Value Object Definitions](#value-object-definitions)
8. [Entity Lifecycle Management](#entity-lifecycle-management)

---

## Executive Summary

This document serves as the **CANONICAL ENTITY RELATIONSHIP MODEL** for the National Healthcare Digital Operating System (NHDOS). It defines 70+ healthcare entities with complete specifications including attributes, relationships, lifecycle states, and business rules.

### Entity Categories

| Category | Entity Count | Description |
|----------|--------------|-------------|
| Foundation | 12 | Core platform entities |
| Clinical Care | 25 | Patient care entities |
| Business Operations | 18 | Financial and operational |
| Intelligence | 8 | Analytics and AI |
| Engagement | 7 | Patient and provider engagement |

---

## Entity Modeling Conventions

### Entity Types

| Type | Description | Example |
|------|-------------|---------|
| **Aggregate Root** | Top-level entity that maintains consistency | Patient, Encounter |
| **Entity** | Object with identity and lifecycle | Order, Result |
| **Value Object** | Immutable object defined by attributes | Address, BloodType |
| **Domain Event** | Record of something that happened | PatientRegistered |
| **Command** | Intent to perform an action | RegisterPatient |
| **Read Model** | Optimized view for queries | PatientSummary |

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Entity Names | PascalCase | `Patient`, `LabOrder` |
| Attribute Names | camelCase | `patientId`, `createdDate` |
| Table Names | snake_case | `patients`, `lab_orders` |
| Event Names | PastTenseVerbNoun | `PatientRegistered`, `OrderPlaced` |
| Command Names | ImperativeVerbNoun | `RegisterPatient`, `PlaceOrder` |

### Data Types

| Type | Description | Example |
|------|-------------|---------|
| UUID | Primary key format | `550e8400-e29b-41d4-a716-446655440000` |
| String | Text data | `John Doe` |
| Date | ISO 8601 date | `2026-06-25` |
| DateTime | ISO 8601 datetime | `2026-06-25T14:30:00Z` |
| Enum | Predefined values | `ACTIVE`, `INACTIVE` |
| Decimal | Precise numbers | `123.45` |
| Boolean | True/false | `true` |
| Integer | Whole numbers | `42` |

---

## Core Entity Definitions

### Foundation Entities

#### 1. User

**Entity ID:** `USER`  
**UUID:** `550e8400-e29b-41d4-a716-446655440001`  
**Canonical Name:** User  
**Aliases:** SystemUser, StaffUser, ClinicianUser  
**Description:** Represents a system user with authentication credentials and access rights.  
**Owner Domain:** Identity  
**Lifecycle States:** Pending, Active, Inactive, Suspended, Deleted

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| userId | UUID | Yes | Unique identifier | Primary Key |
| username | String | Yes | Login username | Unique, 3-50 chars |
| email | String | Yes | Email address | Unique, valid format |
| phoneNumber | String | No | Phone number | E.164 format |
| passwordHash | String | Yes | Hashed password | Bcrypt, min 12 chars |
| firstName | String | Yes | First name | 1-100 chars |
| lastName | String | Yes | Last name | 1-100 chars |
| displayName | String | Yes | Display name | 1-200 chars |
| status | Enum | Yes | Account status | Pending, Active, Inactive, Suspended, Deleted |
| lastLoginAt | DateTime | No | Last login timestamp | ISO 8601 |
| failedLoginAttempts | Integer | Yes | Failed login count | Default: 0 |
| lockoutEndAt | DateTime | No | Account lockout end | ISO 8601 |
| mfaEnabled | Boolean | Yes | MFA enabled flag | Default: false |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |
| createdBy | UUID | Yes | Creator user ID | FK to User |
| updatedBy | UUID | Yes | Last updater user ID | FK to User |

**Relationships:**

- `User` → `UserProfile` (One-to-One)
- `User` → `UserRoleAssignment` (One-to-Many)
- `User` → `Session` (One-to-Many)
- `User` → `AuditLog` (One-to-Many)
- `User` → `Notification` (One-to-Many)

---

#### 2. UserProfile

**Entity ID:** `USER_PROFILE`  
**UUID:** `550e8400-e29b-41d4-a716-446655440002`  
**Canonical Name:** UserProfile  
**Aliases:** UserDetail, StaffProfile  
**Description:** Extended user profile information including professional details.  
**Owner Domain:** Identity  
**Lifecycle States:** Draft, Complete, Archived

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| profileId | UUID | Yes | Unique identifier | Primary Key |
| userId | UUID | Yes | Associated user | FK to User, Unique |
| jobTitle | String | No | Job title | 1-200 chars |
| department | String | No | Department | 1-200 chars |
| employeeId | String | No | Employee ID | Unique, 1-50 chars |
| licenseNumber | String | No | Professional license | 1-100 chars |
| licenseExpiration | Date | No | License expiry | Future date |
| specialty | String | No | Medical specialty | 1-200 chars |
| npiNumber | String | No | NPI number | 10 digits |
| avatarUrl | String | No | Profile picture URL | Valid URL |
| preferences | JSON | No | User preferences | Valid JSON |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `UserProfile` → `User` (Many-to-One)
- `UserProfile` → `Department` (Many-to-One)

---

#### 3. Role

**Entity ID:** `ROLE`  
**UUID:** `550e8400-e29b-41d4-a716-446655440003`  
**Canonical Name:** Role  
**Aliases:** SystemRole, AccessRole  
**Description:** Defines a role with associated permissions for access control.  
**Owner Domain:** Authorization  
**Lifecycle States:** Draft, Active, Inactive, Archived

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| roleId | UUID | Yes | Unique identifier | Primary Key |
| roleName | String | Yes | Role name | Unique, 1-100 chars |
| description | String | Yes | Role description | 1-500 chars |
| roleType | Enum | Yes | Role type | System, Clinical, Administrative |
| status | Enum | Yes | Role status | Draft, Active, Inactive, Archived |
| isSystemRole | Boolean | Yes | System role flag | Default: false |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Role` → `UserRoleAssignment` (One-to-Many)
- `Role` → `RolePermission` (One-to-Many)

---

#### 4. Permission

**Entity ID:** `PERMISSION`  
**UUID:** `550e8400-e29b-41d4-a716-446655440004`  
**Canonical Name:** Permission  
**Aliases:** AccessPermission, SystemPermission  
**Description:** Granular permission for system actions.  
**Owner Domain:** Authorization  
**Lifecycle States:** Active, Inactive

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| permissionId | UUID | Yes | Unique identifier | Primary Key |
| permissionName | String | Yes | Permission name | Unique, 1-100 chars |
| description | String | Yes | Permission description | 1-500 chars |
| resource | String | Yes | Target resource | 1-200 chars |
| action | String | Yes | Allowed action | 1-100 chars |
| status | Enum | Yes | Permission status | Active, Inactive |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |

**Relationships:**

- `Permission` → `RolePermission` (One-to-Many)

---

#### 5. AuditLog

**Entity ID:** `AUDIT_LOG`  
**UUID:** `550e8400-e29b-41d4-a716-446655440005`  
**Canonical Name:** AuditLog  
**Aliases:** SystemAudit, AccessAudit  
**Description:** Immutable record of system activities for compliance.  
**Owner Domain:** Audit  
**Lifecycle States:** Created (immutable)

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| auditId | UUID | Yes | Unique identifier | Primary Key |
| userId | UUID | Yes | User who performed action | FK to User |
| action | String | Yes | Action performed | 1-100 chars |
| resourceType | String | Yes | Resource type | 1-100 chars |
| resourceId | UUID | Yes | Resource identifier | Valid UUID |
| actionDetails | JSON | No | Action details | Valid JSON |
| ipAddress | String | Yes | Client IP address | IPv4/IPv6 |
| userAgent | String | Yes | Client user agent | 1-500 chars |
| timestamp | DateTime | Yes | Action timestamp | ISO 8601, indexed |
| result | Enum | Yes | Action result | Success, Failure, Partial |

**Relationships:**

- `AuditLog` → `User` (Many-to-One)

---

#### 6. Session

**Entity ID:** `SESSION`  
**UUID:** `550e8400-e29b-41d4-a716-446655440006`  
**Canonical Name:** Session  
**Aliases:** UserSession, AuthSession  
**Description:** Active user session tracking.  
**Owner Domain:** Identity  
**Lifecycle States:** Active, Expired, Revoked

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| sessionId | UUID | Yes | Unique identifier | Primary Key |
| userId | UUID | Yes | Session user | FK to User |
| token | String | Yes | Session token | Unique, 128 chars |
| ipAddress | String | Yes | Client IP | IPv4/IPv6 |
| userAgent | String | Yes | Client user agent | 1-500 chars |
| expiresAt | DateTime | Yes | Expiration time | ISO 8601, future |
| status | Enum | Yes | Session status | Active, Expired, Revoked |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| lastAccessedAt | DateTime | Yes | Last access time | ISO 8601 |

**Relationships:**

- `Session` → `User` (Many-to-One)

---

### Clinical Care Entities

#### 7. Patient

**Entity ID:** `PATIENT`  
**UUID:** `550e8400-e29b-41d4-a716-446655440010`  
**Canonical Name:** Patient  
**Aliases:** PatientRecord, MedicalRecord  
**Description:** Master patient record with demographics and medical history.  
**Owner Domain:** Patient  
**Lifecycle States:** Active, Inactive, Deceased, Merged

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| patientId | UUID | Yes | Unique identifier | Primary Key |
| mrn | String | Yes | Medical Record Number | Unique, PAT-YYYY-NNNNNN |
| firstName | String | Yes | First name | 1-100 chars |
| lastName | String | Yes | Last name | 1-100 chars |
| middleName | String | No | Middle name | 1-100 chars |
| dateOfBirth | Date | Yes | Date of birth | Past date |
| gender | Enum | Yes | Gender | Male, Female, NonBinary, Unknown |
| sexAssignedAtBirth | Enum | Yes | Sex assigned at birth | Male, Female, Unknown |
| ssn | String | No | Social Security Number | Encrypted, 9 digits |
| maritalStatus | Enum | No | Marital status | Single, Married, Divorced, Widowed |
| language | String | No | Preferred language | ISO 639-1 |
| ethnicity | String | No | Ethnicity | 1-100 chars |
| race | String | No | Race | 1-100 chars |
| religion | String | No | Religion | 1-100 chars |
| status | Enum | Yes | Patient status | Active, Inactive, Deceased, Merged |
| deceasedDate | DateTime | No | Date of death | ISO 8601 |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |
| createdBy | UUID | Yes | Creator user ID | FK to User |
| updatedBy | UUID | Yes | Last updater user ID | FK to User |

**Relationships:**

- `Patient` → `Address` (One-to-Many)
- `Patient` → `PatientIdentifier` (One-to-Many)
- `Patient` → `EmergencyContact` (One-to-Many)
- `Patient` → `InsurancePolicy` (One-to-Many)
- `Patient` → `Allergy` (One-to-Many)
- `Patient` → `Medication` (One-to-Many)
- `Patient` → `Immunization` (One-to-Many)
- `Patient` → `MedicalHistory` (One-to-Many)
- `Patient` → `Encounter` (One-to-Many)
- `Patient` → `Consent` (One-to-Many)

**Business Rules:**

1. MRN must be unique across the system
2. Date of birth cannot be in the future
3. Deceased patients cannot have new encounters
4. Merged patients must reference surviving patient

---

#### 8. Address

**Entity ID:** `ADDRESS`  
**UUID:** `550e8400-e29b-41d4-a716-446655440011`  
**Canonical Name:** Address  
**Aliases:** PatientAddress, ContactAddress  
**Description:** Physical address for patients and contacts.  
**Owner Domain:** Patient  
**Lifecycle States:** Active, Inactive

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| addressId | UUID | Yes | Unique identifier | Primary Key |
| addressType | Enum | Yes | Address type | Home, Work, Temporary, Mailing |
| addressLine1 | String | Yes | Street address | 1-200 chars |
| addressLine2 | String | No | Apartment/Suite | 1-200 chars |
| city | String | Yes | City | 1-100 chars |
| state | String | Yes | State/Province | 2 chars (US) |
| postalCode | String | Yes | ZIP/Postal code | Valid format |
| country | String | Yes | Country | ISO 3166-1 |
| isPrimary | Boolean | Yes | Primary address flag | Default: false |
| startDate | Date | Yes | Address start date | Valid date |
| endDate | Date | No | Address end date | Future date |
| status | Enum | Yes | Address status | Active, Inactive |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Address` → `Patient` (Many-to-One)

---

#### 9. Encounter

**Entity ID:** `ENCOUNTER`  
**UUID:** `550e8400-e29b-41d4-a716-446655440020`  
**Canonical Name:** Encounter  
**Aliases:** Visit, PatientVisit, ClinicalEncounter  
**Description:** Healthcare encounter between patient and provider.  
**Owner Domain:** Encounter  
**Lifecycle States:** Scheduled, CheckedIn, InProgress, Completed, Cancelled, NoShow

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| encounterId | UUID | Yes | Unique identifier | Primary Key |
| encounterNumber | String | Yes | Encounter number | Unique, ENC-YYYY-NNNNNN |
| patientId | UUID | Yes | Patient | FK to Patient |
| encounterType | Enum | Yes | Encounter type | Outpatient, Inpatient, Emergency, Telehealth |
| status | Enum | Yes | Encounter status | Scheduled, CheckedIn, InProgress, Completed, Cancelled, NoShow |
| scheduledDateTime | DateTime | Yes | Scheduled time | ISO 8601 |
| actualStartDateTime | DateTime | No | Actual start time | ISO 8601 |
| actualEndDateTime | DateTime | No | Actual end time | ISO 8601 |
| departmentId | UUID | Yes | Department | FK to Department |
| primaryProviderId | UUID | Yes | Primary provider | FK to User |
| facilityId | UUID | Yes | Facility | FK to Hospital |
| reasonForVisit | String | Yes | Chief complaint | 1-2000 chars |
| priority | Enum | Yes | Visit priority | Routine, Urgent, Emergent |
| dischargeDisposition | Enum | No | Discharge disposition | Home, Transfer, AMA, Deceased |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Encounter` → `Patient` (Many-to-One)
- `Encounter` → `Department` (Many-to-One)
- `Encounter` → `Hospital` (Many-to-One)
- `Encounter` → `ClinicalDocumentation` (One-to-Many)
- `Encounter` → `Diagnosis` (One-to-Many)
- `Encounter` → `Order` (One-to-Many)
- `Encounter` → `VitalSigns` (One-to-Many)

**Business Rules:**

1. Encounter must be associated with an active patient
2. Completed encounters cannot be cancelled
3. Inpatient encounters require bed assignment
4. Emergency encounters bypass scheduling

---

#### 10. ClinicalDocumentation

**Entity ID:** `CLINICAL_DOCUMENTATION`  
**UUID:** `550e8400-e29b-41d4-a716-446655440021`  
**Canonical Name:** ClinicalDocumentation  
**Aliases:** ClinicalNote, ProgressNote, MedicalRecord  
**Description:** Clinical notes and documentation for encounters.  
**Owner Domain:** Encounter  
**Lifecycle States:** Draft, InReview, Signed, Amended, Voided

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| documentationId | UUID | Yes | Unique identifier | Primary Key |
| encounterId | UUID | Yes | Associated encounter | FK to Encounter |
| documentType | Enum | Yes | Document type | ProgressNote, H&P, DischargeSummary, Consult, Procedure |
| authorId | UUID | Yes | Document author | FK to User |
| title | String | Yes | Document title | 1-200 chars |
| content | String | Yes | Document content | Rich text, max 100000 chars |
| status | Enum | Yes | Document status | Draft, InReview, Signed, Amended, Voided |
| signedAt | DateTime | No | Signature timestamp | ISO 8601 |
| signedBy | UUID | No | Signer | FK to User |
| version | Integer | Yes | Document version | 1+ |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `ClinicalDocumentation` → `Encounter` (Many-to-One)
- `ClinicalDocumentation` → `User` (Many-to-One, Author)
- `ClinicalDocumentation` → `User` (Many-to-One, Signer)

---

#### 11. VitalSigns

**Entity ID:** `VITAL_SIGNS`  
**UUID:** `550e8400-e29b-41d4-a716-446655440022`  
**Canonical Name:** VitalSigns  
**Aliases:** Vitals, PatientVitals  
**Description:** Patient vital signs measurements.  
**Owner Domain:** Encounter  
**Lifecycle States:** Recorded (immutable)

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| vitalSignsId | UUID | Yes | Unique identifier | Primary Key |
| encounterId | UUID | Yes | Associated encounter | FK to Encounter |
| patientId | UUID | Yes | Patient | FK to Patient |
| temperature | Decimal | No | Body temperature | 90-110°F or 32-43°C |
| heartRate | Integer | No | Heart rate (bpm) | 20-300 |
| respiratoryRate | Integer | No | Respiratory rate | 5-60 |
| bloodPressureSystolic | Integer | No | Systolic BP | 40-300 mmHg |
| bloodPressureDiastolic | Integer | No | Diastolic BP | 20-200 mmHg |
| oxygenSaturation | Decimal | No | O2 saturation | 0-100% |
| weight | Decimal | No | Weight | 0-1000 lbs |
| height | Decimal | No | Height | 0-120 inches |
| bmi | Decimal | No | Body Mass Index | Calculated |
| painLevel | Integer | No | Pain scale | 0-10 |
| recordedAt | DateTime | Yes | Recording time | ISO 8601 |
| recordedBy | UUID | Yes | Recorder | FK to User |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |

**Relationships:**

- `VitalSigns` → `Encounter` (Many-to-One)
- `VitalSigns` → `Patient` (Many-to-One)
- `VitalSigns` → `User` (Many-to-One)

---

#### 12. Diagnosis

**Entity ID:** `DIAGNOSIS`  
**UUID:** `550e8400-e29b-41d4-a716-446655440023`  
**Canonical Name:** Diagnosis  
**Aliases:** PatientDiagnosis, ClinicalDiagnosis  
**Description:** Diagnoses documented during encounters.  
**Owner Domain:** Encounter  
**Lifecycle States:** Active, Inactive, Resolved

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| diagnosisId | UUID | Yes | Unique identifier | Primary Key |
| encounterId | UUID | Yes | Associated encounter | FK to Encounter |
| patientId | UUID | Yes | Patient | FK to Patient |
| icd10Code | String | Yes | ICD-10 code | Valid ICD-10 |
| snomedCode | String | No | SNOMED CT code | Valid SNOMED |
| diagnosisName | String | Yes | Diagnosis description | 1-500 chars |
| diagnosisType | Enum | Yes | Diagnosis type | Primary, Secondary, Admitting, Discharge |
| status | Enum | Yes | Diagnosis status | Active, Inactive, Resolved |
| onsetDate | Date | Yes | Onset date | Valid date |
| resolvedDate | Date | No | Resolution date | Future date |
| severity | Enum | No | Severity | Mild, Moderate, Severe |
| clinicianId | UUID | Yes | Diagnosing clinician | FK to User |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Diagnosis` → `Encounter` (Many-to-One)
- `Diagnosis` → `Patient` (Many-to-One)
- `Diagnosis` → `User` (Many-to-One)

---

#### 13. Order

**Entity ID:** `ORDER`  
**UUID:** `550e8400-e29b-41d4-a716-446655440030`  
**Canonical Name:** Order  
**Aliases:** ClinicalOrder, ProviderOrder  
**Description:** Clinical orders placed by providers.  
**Owner Domain:** Orders  
**Lifecycle States:** Draft, Submitted, Accepted, InProgress, Completed, Cancelled, Expired

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| orderId | UUID | Yes | Unique identifier | Primary Key |
| orderNumber | String | Yes | Order number | Unique, ORD-YYYY-NNNNNN |
| encounterId | UUID | Yes | Associated encounter | FK to Encounter |
| patientId | UUID | Yes | Patient | FK to Patient |
| orderType | Enum | Yes | Order type | Laboratory, Radiology, Pharmacy, Consult, Procedure |
| orderStatus | Enum | Yes | Order status | Draft, Submitted, Accepted, InProgress, Completed, Cancelled, Expired |
| priority | Enum | Yes | Order priority | Routine, Urgent, Stat, PreOp |
| orderDateTime | DateTime | Yes | Order time | ISO 8601 |
| orderingProviderId | UUID | Yes | Ordering provider | FK to User |
| orderDetails | JSON | Yes | Order-specific details | Valid JSON |
| clinicalIndication | String | Yes | Clinical reason | 1-2000 chars |
| scheduledDateTime | DateTime | No | Scheduled time | ISO 8601 |
| completionDateTime | DateTime | No | Completion time | ISO 8601 |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Order` → `Encounter` (Many-to-One)
- `Order` → `Patient` (Many-to-One)
- `Order` → `User` (Many-to-One, Ordering Provider)
- `Order` → `LabOrder` (One-to-One, Inheritance)
- `Order` → `RadiologyOrder` (One-to-One, Inheritance)
- `Order` → `MedicationOrder` (One-to-One, Inheritance)

**Business Rules:**

1. Orders must be associated with an active encounter
2. Cancelled orders cannot be reactivated
3. Expired orders require new order placement
4. Stat orders must be processed within 1 hour

---

### Laboratory Domain Entities

#### 14. LabOrder

**Entity ID:** `LAB_ORDER`  
**UUID:** `550e8400-e29b-41d4-a716-446655440040`  
**Canonical Name:** LabOrder  
**Aliases:** LaboratoryOrder, TestOrder  
**Description:** Laboratory test order extending base Order.  
**Owner Domain:** Laboratory  
**Lifecycle States:** Submitted, Accepted, Rejected, InProgress, Completed

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| labOrderId | UUID | Yes | Unique identifier | Primary Key |
| orderId | UUID | Yes | Parent order | FK to Order, Unique |
| labTestCode | String | Yes | Test code | LOINC code |
| labTestName | String | Yes | Test name | 1-200 chars |
| specimenType | Enum | Yes | Specimen type | Blood, Urine, Stool, CSF, Tissue |
| collectionInstructions | String | No | Special instructions | 1-1000 chars |
| fastingRequired | Boolean | Yes | Fasting required | Default: false |
| clinicalHistory | String | No | Clinical context | 1-2000 chars |
| status | Enum | Yes | Lab order status | Submitted, Accepted, Rejected, InProgress, Completed |
| acceptedAt | DateTime | No | Acceptance time | ISO 8601 |
| completedAt | DateTime | No | Completion time | ISO 8601 |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `LabOrder` → `Order` (One-to-One, Inheritance)
- `LabOrder` → `Specimen` (One-to-Many)
- `LabOrder` → `LabResult` (One-to-Many)

---

#### 15. Specimen

**Entity ID:** `SPECIMEN`  
**UUID:** `550e8400-e29b-41d4-a716-446655440041`  
**Canonical Name:** Specimen  
**Aliases:** LabSpecimen, BiologicalSpecimen  
**Description:** Biological specimen collected for laboratory testing.  
**Owner Domain:** Laboratory  
**Lifecycle States:** Collected, Received, Processed, Tested, Archived, Rejected

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| specimenId | UUID | Yes | Unique identifier | Primary Key |
| specimenNumber | String | Yes | Specimen number | Unique, SPC-YYYY-NNNNNN |
| labOrderId | UUID | Yes | Associated order | FK to LabOrder |
| patientId | UUID | Yes | Patient | FK to Patient |
| specimenType | Enum | Yes | Specimen type | Blood, Urine, Stool, CSF, Tissue, Other |
| collectionMethod | Enum | Yes | Collection method | Venipuncture, Fingerstick, CleanCatch, Swab |
| collectionDateTime | DateTime | Yes | Collection time | ISO 8601 |
| collectedBy | UUID | Yes | Collector | FK to User |
| receivedAt | DateTime | No | Receipt time | ISO 8601 |
| receivedBy | UUID | No | Receiver | FK to User |
| containerType | String | Yes | Container type | 1-100 chars |
| volume | Decimal | No | Volume collected | 0+ |
| volumeUnit | String | No | Volume unit | mL, L |
| status | Enum | Yes | Specimen status | Collected, Received, Processed, Tested, Archived, Rejected |
| rejectionReason | String | No | Rejection reason | 1-500 chars |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Specimen` → `LabOrder` (Many-to-One)
- `Specimen` → `Patient` (Many-to-One)
- `Specimen` → `User` (Many-to-One, Collector)
- `Specimen` → `LabResult` (One-to-Many)
- `Specimen` → `SpecimenProcessing` (One-to-Many)

---

#### 16. LabResult

**Entity ID:** `LAB_RESULT`  
**UUID:** `550e8400-e29b-41d4-a716-446655440042`  
**Canonical Name:** LabResult  
**Aliases:** TestResult, LaboratoryResult  
**Description:** Laboratory test result with values and interpretation.  
**Owner Domain:** Laboratory  
**Lifecycle States:** Preliminary, Final, Amended, Cancelled

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| labResultId | UUID | Yes | Unique identifier | Primary Key |
| resultNumber | String | Yes | Result number | Unique, RES-YYYY-NNNNNN |
| labOrderId | UUID | Yes | Associated order | FK to LabOrder |
| specimenId | UUID | Yes | Specimen | FK to Specimen |
| patientId | UUID | Yes | Patient | FK to Patient |
| resultCode | String | Yes | Result code | LOINC code |
| resultName | String | Yes | Result name | 1-200 chars |
| resultValue | String | Yes | Result value | 1-500 chars |
| resultUnit | String | Yes | Result unit | 1-50 chars |
| referenceRangeLow | Decimal | No | Reference low | Numeric |
| referenceRangeHigh | Decimal | No | Reference high | Numeric |
| abnormalFlag | Enum | No | Abnormal indicator | Normal, Low, High, Critical |
| interpretation | String | No | Clinical interpretation | 1-2000 chars |
| status | Enum | Yes | Result status | Preliminary, Final, Amended, Cancelled |
| performedAt | DateTime | Yes | Performance time | ISO 8601 |
| verifiedAt | DateTime | No | Verification time | ISO 8601 |
| verifiedBy | UUID | No | Verifier | FK to User |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `LabResult` → `LabOrder` (Many-to-One)
- `LabResult` → `Specimen` (Many-to-One)
- `LabResult` → `Patient` (Many-to-One)
- `LabResult` → `User` (Many-to-One, Verifier)

---

### Radiology Domain Entities

#### 17. RadiologyOrder

**Entity ID:** `RADIOLOGY_ORDER`  
**UUID:** `550e8400-e29b-41d4-a716-446655440050`  
**Canonical Name:** RadiologyOrder  
**Aliases:** ImagingOrder, StudyOrder  
**Description:** Radiology/imaging order extending base Order.  
**Owner Domain:** Radiology  
**Lifecycle States:** Submitted, Scheduled, InProgress, Completed

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| radiologyOrderId | UUID | Yes | Unique identifier | Primary Key |
| orderId | UUID | Yes | Parent order | FK to Order, Unique |
| modality | Enum | Yes | Imaging modality | CT, MRI, XRay, Ultrasound, PET, Nuclear |
| bodyPart | String | Yes | Body part examined | 1-200 chars |
| laterality | Enum | No | Laterality | Left, Right, Bilateral, None |
| contrastRequired | Boolean | Yes | Contrast required | Default: false |
| contrastType | String | No | Contrast type | 1-100 chars |
| clinicalIndication | String | Yes | Clinical reason | 1-2000 chars |
| patientHistory | String | No | Relevant history | 1-2000 chars |
| pregnancyStatus | Enum | No | Pregnancy status | Positive, Negative, Unknown |
| claustrophobia | Boolean | No | Claustrophobia flag | Default: false |
| status | Enum | Yes | Order status | Submitted, Scheduled, InProgress, Completed |
| scheduledAt | DateTime | No | Scheduled time | ISO 8601 |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `RadiologyOrder` → `Order` (One-to-One, Inheritance)
- `RadiologyOrder` → `ImagingStudy` (One-to-One)
- `RadiologyOrder` → `RadiologyReport` (One-to-One)

---

#### 18. ImagingStudy

**Entity ID:** `IMAGING_STUDY`  
**UUID:** `550e8400-e29b-41d4-a716-446655440051`  
**Canonical Name:** ImagingStudy  
**Aliases:** DiagnosticStudy, RadiologyStudy  
**Description:** Complete imaging study with associated images.  
**Owner Domain:** Radiology  
**Lifecycle States:** Started, Completed, Archived

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| studyId | UUID | Yes | Unique identifier | Primary Key |
| studyInstanceUid | String | Yes | DICOM Study UID | Unique, DICOM format |
| radiologyOrderId | UUID | Yes | Associated order | FK to RadiologyOrder |
| patientId | UUID | Yes | Patient | FK to Patient |
| accessionNumber | String | Yes | Accession number | Unique |
| studyDate | DateTime | Yes | Study date/time | ISO 8601 |
| modality | Enum | Yes | Modality | CT, MRI, XRay, Ultrasound |
| bodyPart | String | Yes | Body part | 1-200 chars |
| institution | String | Yes | Institution name | 1-200 chars |
| status | Enum | Yes | Study status | Started, Completed, Archived |
| imageCount | Integer | Yes | Number of images | 0+ |
| pacsUrl | String | No | PACS URL | Valid URL |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `ImagingStudy` → `RadiologyOrder` (One-to-One)
- `ImagingStudy` → `Patient` (Many-to-One)
- `ImagingStudy` → `Image` (One-to-Many)
- `ImagingStudy` → `RadiologyReport` (One-to-One)

---

#### 19. RadiologyReport

**Entity ID:** `RADIOLOGY_REPORT`  
**UUID:** `550e8400-e29b-41d4-a716-446655440052`  
**Canonical Name:** RadiologyReport  
**Aliases:** ImagingReport, InterpretationReport  
**Description:** Radiologist interpretation and findings.  
**Owner Domain:** Radiology  
**Lifecycle States:** Dictated, Transcribed, Signed, Amended

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| reportId | UUID | Yes | Unique identifier | Primary Key |
| reportNumber | String | Yes | Report number | Unique, RPT-YYYY-NNNNNN |
| studyId | UUID | Yes | Associated study | FK to ImagingStudy |
| radiologyOrderId | UUID | Yes | Associated order | FK to RadiologyOrder |
| patientId | UUID | Yes | Patient | FK to Patient |
| radiologistId | UUID | Yes | Interpreting radiologist | FK to User |
| clinicalIndication | String | Yes | Clinical reason | 1-2000 chars |
| findings | String | Yes | Imaging findings | 1-10000 chars |
| impression | String | Yes | Radiologist impression | 1-2000 chars |
| recommendation | String | No | Recommendations | 1-2000 chars |
| criticalFinding | Boolean | Yes | Critical finding flag | Default: false |
| status | Enum | Yes | Report status | Dictated, Transcribed, Signed, Amended |
| dictatedAt | DateTime | No | Dictation time | ISO 8601 |
| transcribedAt | DateTime | No | Transcription time | ISO 8601 |
| signedAt | DateTime | No | Signature time | ISO 8601 |
| signedBy | UUID | No | Signer | FK to User |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `RadiologyReport` → `ImagingStudy` (One-to-One)
- `RadiologyReport` → `RadiologyOrder` (One-to-One)
- `RadiologyReport` → `Patient` (Many-to-One)
- `RadiologyReport` → `User` (Many-to-One, Radiologist)

---

### Pharmacy Domain Entities

#### 20. MedicationOrder

**Entity ID:** `MEDICATION_ORDER`  
**UUID:** `550e8400-e29b-41d4-a716-446655440060`  
**Canonical Name:** MedicationOrder  
**Aliases:** DrugOrder, PrescriptionOrder  
**Description:** Medication order extending base Order.  
**Owner Domain:** Pharmacy  
**Lifecycle States:** Submitted, Verified, Dispensed, Administered, Completed, Cancelled

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| medicationOrderId | UUID | Yes | Unique identifier | Primary Key |
| orderId | UUID | Yes | Parent order | FK to Order, Unique |
| medicationId | UUID | Yes | Medication | FK to Medication |
| dosage | String | Yes | Dosage | 1-100 chars |
| route | Enum | Yes | Administration route | Oral, IV, IM, SC, Topical, Inhaled |
| frequency | String | Yes | Dosing frequency | 1-100 chars |
| duration | String | No | Treatment duration | 1-50 chars |
| quantity | Integer | Yes | Quantity ordered | 1+ |
| refills | Integer | No | Number of refills | 0-12 |
| startDate | Date | Yes | Start date | Valid date |
| endDate | Date | No | End date | Future date |
| indication | String | Yes | Clinical indication | 1-500 chars |
| specialInstructions | String | No | Special instructions | 1-1000 chars |
| status | Enum | Yes | Order status | Submitted, Verified, Dispensed, Administered, Completed, Cancelled |
| verifiedAt | DateTime | No | Verification time | ISO 8601 |
| verifiedBy | UUID | No | Verifier | FK to User |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `MedicationOrder` → `Order` (One-to-One, Inheritance)
- `MedicationOrder` → `Medication` (Many-to-One)
- `MedicationOrder` → `DispensingRecord` (One-to-Many)
- `MedicationOrder` → `AdministrationRecord` (One-to-Many)

---

#### 21. Medication

**Entity ID:** `MEDICATION`  
**UUID:** `550e8400-e29b-41d4-a716-446655440061`  
**Canonical Name:** Medication  
**Aliases:** Drug, Pharmaceutical  
**Description:** Drug definition from formulary.  
**Owner Domain:** Pharmacy  
**Lifecycle States:** Active, Inactive, Discontinued

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| medicationId | UUID | Yes | Unique identifier | Primary Key |
| ndcCode | String | Yes | NDC code | Unique, 11 digits |
| name | String | Yes | Medication name | 1-200 chars |
| genericName | String | Yes | Generic name | 1-200 chars |
| brandName | String | No | Brand name | 1-200 chars |
| medicationClass | String | Yes | Drug class | 1-200 chars |
| dosageForm | Enum | Yes | Dosage form | Tablet, Capsule, Liquid, Injection, Topical |
| strength | String | Yes | Strength | 1-100 chars |
| route | Enum | Yes | Route | Oral, IV, IM, SC, Topical, Inhaled |
| controlledSubstance | Enum | No | Controlled substance | None, II, III, IV, V |
| formularyStatus | Enum | Yes | Formulary status | Formulary, NonFormulary, Restricted |
| status | Enum | Yes | Medication status | Active, Inactive, Discontinued |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Medication` → `MedicationOrder` (One-to-Many)
- `Medication` → `DrugInteraction` (One-to-Many)

---

#### 22. DispensingRecord

**Entity ID:** `DISPENSING_RECORD`  
**UUID:** `550e8400-e29b-41d4-a716-446655440062`  
**Canonical Name:** DispensingRecord  
**Aliases:** PharmacyDispensing, DrugDispensing  
**Description:** Record of medication dispensing.  
**Owner Domain:** Pharmacy  
**Lifecycle States:** Dispensed, PickedUp, Returned

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| dispensingId | UUID | Yes | Unique identifier | Primary Key |
| dispensingNumber | String | Yes | Dispensing number | Unique, DSP-YYYY-NNNNNN |
| medicationOrderId | UUID | Yes | Associated order | FK to MedicationOrder |
| patientId | UUID | Yes | Patient | FK to Patient |
| medicationId | UUID | Yes | Medication | FK to Medication |
| quantityDispensed | Integer | Yes | Quantity | 1+ |
| lotNumber | String | Yes | Lot number | 1-50 chars |
| expirationDate | Date | Yes | Expiration date | Future date |
| pharmacistId | UUID | Yes | Dispensing pharmacist | FK to User |
| pharmacyId | UUID | Yes | Pharmacy | FK to Pharmacy |
| status | Enum | Yes | Dispensing status | Dispensed, PickedUp, Returned |
| dispensedAt | DateTime | Yes | Dispensing time | ISO 8601 |
| pickedUpAt | DateTime | No | Pickup time | ISO 8601 |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `DispensingRecord` → `MedicationOrder` (Many-to-One)
- `DispensingRecord` → `Patient` (Many-to-One)
- `DispensingRecord` → `Medication` (Many-to-One)
- `DispensingRecord` → `User` (Many-to-One)
- `DispensingRecord` → `Pharmacy` (Many-to-One)

---

#### 23. AdministrationRecord

**Entity ID:** `ADMINISTRATION_RECORD`  
**UUID:** `550e8400-e29b-41d4-a716-446655440063`  
**Canonical Name:** AdministrationRecord  
**Aliases:** MedicationAdministration, DrugAdministration  
**Description:** Record of medication administration to patient.  
**Owner Domain:** Pharmacy  
**Lifecycle States:** Scheduled, Administered, Missed, Refused

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| administrationId | UUID | Yes | Unique identifier | Primary Key |
| medicationOrderId | UUID | Yes | Associated order | FK to MedicationOrder |
| patientId | UUID | Yes | Patient | FK to Patient |
| medicationId | UUID | Yes | Medication | FK to Medication |
| dosage | String | Yes | Dosage administered | 1-100 chars |
| route | Enum | Yes | Route | Oral, IV, IM, SC, Topical |
| administeredBy | UUID | Yes | Administrator | FK to User |
| administeredAt | DateTime | Yes | Administration time | ISO 8601 |
| status | Enum | Yes | Administration status | Scheduled, Administered, Missed, Refused |
| refusalReason | String | No | Refusal reason | 1-500 chars |
| site | String | No | Injection site | 1-100 chars |
| batchNumber | String | No | Batch number | 1-50 chars |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |

**Relationships:**

- `AdministrationRecord` → `MedicationOrder` (Many-to-One)
- `AdministrationRecord` → `Patient` (Many-to-One)
- `AdministrationRecord` → `Medication` (Many-to-One)
- `AdministrationRecord` → `User` (Many-to-One)

---

### Hospital Domain Entities

#### 24. Hospital

**Entity ID:** `HOSPITAL`  
**UUID:** `550e8400-e29b-41d4-a716-446655440070`  
**Canonical Name:** Hospital  
**Aliases:** Facility, HealthcareFacility  
**Description:** Hospital or healthcare facility.  
**Owner Domain:** Hospital  
**Lifecycle States:** Active, Inactive, Closed

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| hospitalId | UUID | Yes | Unique identifier | Primary Key |
| facilityCode | String | Yes | Facility code | Unique, 1-20 chars |
| name | String | Yes | Facility name | 1-200 chars |
| facilityType | Enum | Yes | Facility type | Hospital, Clinic, SNF, HomeHealth |
| address | String | Yes | Facility address | 1-500 chars |
| phoneNumber | String | Yes | Phone number | E.164 format |
| email | String | Yes | Contact email | Valid email |
| licenseNumber | String | Yes | License number | 1-100 chars |
| bedCapacity | Integer | Yes | Total bed capacity | 1+ |
| status | Enum | Yes | Facility status | Active, Inactive, Closed |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Hospital` → `Department` (One-to-Many)
- `Hospital` → `Bed` (One-to-Many)
- `Hospital` → `Encounter` (One-to-Many)

---

#### 25. Department

**Entity ID:** `DEPARTMENT`  
**UUID:** `550e8400-e29b-41d4-a716-446655440071`  
**Canonical Name:** Department  
**Aliases:** HospitalDepartment, ClinicalDepartment  
**Description:** Hospital department or unit.  
**Owner Domain:** Hospital  
**Lifecycle States:** Active, Inactive, Merged

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| departmentId | UUID | Yes | Unique identifier | Primary Key |
| departmentCode | String | Yes | Department code | Unique, 1-20 chars |
| hospitalId | UUID | Yes | Parent hospital | FK to Hospital |
| name | String | Yes | Department name | 1-200 chars |
| departmentType | Enum | Yes | Department type | Medical, Surgical, ICU, ED, Outpatient, Admin |
| floor | String | No | Floor location | 1-50 chars |
| wing | String | No | Wing/building | 1-50 chars |
| phoneExtension | String | No | Phone extension | 1-20 chars |
| capacity | Integer | Yes | Bed capacity | 0+ |
| headOfDepartment | UUID | No | Department head | FK to User |
| status | Enum | Yes | Department status | Active, Inactive, Merged |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Department` → `Hospital` (Many-to-One)
- `Department` → `Bed` (One-to-Many)
- `Department` → `Encounter` (One-to-Many)
- `Department` → `User` (Many-to-One, Head)

---

#### 26. Bed

**Entity ID:** `BED`  
**UUID:** `550e8400-e29b-41d4-a716-446655440072`  
**Canonical Name:** Bed  
**Aliases:** HospitalBed, PatientBed  
**Description:** Hospital bed for patient care.  
**Owner Domain:** Hospital  
**Lifecycle States:** Available, Occupied, Reserved, Maintenance, OutOfService

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| bedId | UUID | Yes | Unique identifier | Primary Key |
| bedNumber | String | Yes | Bed number | Unique within department |
| hospitalId | UUID | Yes | Hospital | FK to Hospital |
| departmentId | UUID | Yes | Department | FK to Department |
| bedType | Enum | Yes | Bed type | Medical, Surgical, ICU, ED, Telemetry |
| status | Enum | Yes | Bed status | Available, Occupied, Reserved, Maintenance, OutOfService |
| patientId | UUID | No | Current patient | FK to Patient |
| admitDate | DateTime | No | Admission date | ISO 8601 |
| expectedDischarge | DateTime | No | Expected discharge | ISO 8601 |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Bed` → `Hospital` (Many-to-One)
- `Bed` → `Department` (Many-to-One)
- `Bed` → `Patient` (Many-to-One, Optional)

---

### Scheduling Domain Entities

#### 27. Appointment

**Entity ID:** `APPOINTMENT`  
**UUID:** `550e8400-e29b-41d4-a716-446655440080`  
**Canonical Name:** Appointment  
**Aliases:** PatientAppointment, ScheduledAppointment  
**Description:** Scheduled patient appointment.  
**Owner Domain:** Scheduling  
**Lifecycle States:** Scheduled, Confirmed, CheckedIn, InProgress, Completed, Cancelled, NoShow

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| appointmentId | UUID | Yes | Unique identifier | Primary Key |
| appointmentNumber | String | Yes | Appointment number | Unique, APT-YYYY-NNNNNN |
| patientId | UUID | Yes | Patient | FK to Patient |
| providerId | UUID | Yes | Provider | FK to User |
| appointmentType | Enum | Yes | Appointment type | OfficeVisit, FollowUp, Procedure, Consultation |
| scheduledDate | Date | Yes | Appointment date | Valid date |
| scheduledTime | String | Yes | Appointment time | HH:MM format |
| duration | Integer | Yes | Duration (minutes) | 15-480 |
| departmentId | UUID | Yes | Department | FK to Department |
| reason | String | Yes | Visit reason | 1-500 chars |
| status | Enum | Yes | Appointment status | Scheduled, Confirmed, CheckedIn, InProgress, Completed, Cancelled, NoShow |
| confirmationStatus | Enum | Yes | Confirmation status | Pending, Confirmed, Cancelled |
| notes | String | No | Appointment notes | 1-1000 chars |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Appointment` → `Patient` (Many-to-One)
- `Appointment` → `User` (Many-to-One, Provider)
- `Appointment` → `Department` (Many-to-One)
- `Appointment` → `Encounter` (One-to-One, Optional)

**Business Rules:**

1. Appointments must be in the future
2. Provider must be available at scheduled time
3. Double-booking not allowed for same provider/time
4. Cancellation within 24 hours may incur fee

---

### Finance Domain Entities

#### 28. FinancialTransaction

**Entity ID:** `FINANCIAL_TRANSACTION`  
**UUID:** `550e8400-e29b-41d4-a716-446655440090`  
**Canonical Name:** FinancialTransaction  
**Aliases:** Transaction, AccountingEntry  
**Description:** Financial transaction for billing and accounting.  
**Owner Domain:** Finance  
**Lifecycle States:** Pending, Posted, Reversed, Voided

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| transactionId | UUID | Yes | Unique identifier | Primary Key |
| transactionNumber | String | Yes | Transaction number | Unique, FIN-YYYY-NNNNNN |
| transactionType | Enum | Yes | Transaction type | Charge, Payment, Refund, Adjustment, Denial |
| patientId | UUID | Yes | Patient | FK to Patient |
| encounterId | UUID | No | Encounter | FK to Encounter |
| amount | Decimal | Yes | Transaction amount | Positive for charges, negative for credits |
| currency | String | Yes | Currency | ISO 4217, default: USD |
| transactionDate | DateTime | Yes | Transaction date | ISO 8601 |
| postingDate | DateTime | No | Posting date | ISO 8601 |
| status | Enum | Yes | Transaction status | Pending, Posted, Reversed, Voided |
| description | String | Yes | Description | 1-500 chars |
| glAccount | String | Yes | GL account | 1-50 chars |
| costCenter | String | No | Cost center | 1-50 chars |
| createdBy | UUID | Yes | Creator | FK to User |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `FinancialTransaction` → `Patient` (Many-to-One)
- `FinancialTransaction` → `Encounter` (Many-to-One, Optional)
- `FinancialTransaction` → `User` (Many-to-One)
- `FinancialTransaction` → `Claim` (One-to-Many, Optional)

---

#### 29. Claim

**Entity ID:** `CLAIM`  
**UUID:** `550e8400-e29b-41d4-a716-446655440091`  
**Canonical Name:** Claim  
**Aliases:** InsuranceClaim, MedicalClaim  
**Description:** Insurance claim for reimbursement.  
**Owner Domain:** Revenue Cycle  
**Lifecycle States:** Draft, Submitted, Accepted, Denied, Pending, Paid, Closed

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| claimId | UUID | Yes | Unique identifier | Primary Key |
| claimNumber | String | Yes | Claim number | Unique, CLM-YYYY-NNNNNN |
| patientId | UUID | Yes | Patient | FK to Patient |
| encounterId | UUID | Yes | Encounter | FK to Encounter |
| insurancePlanId | UUID | Yes | Insurance plan | FK to InsurancePlan |
| claimType | Enum | Yes | Claim type | Professional, Institutional, Pharmacy |
| totalAmount | Decimal | Yes | Total claim amount | Positive decimal |
| submittedAmount | Decimal | Yes | Submitted amount | Positive decimal |
| paidAmount | Decimal | No | Paid amount | Positive decimal |
| submitDate | DateTime | Yes | Submission date | ISO 8601 |
| receivedDate | DateTime | No | Received by payer | ISO 8601 |
| status | Enum | Yes | Claim status | Draft, Submitted, Accepted, Denied, Pending, Paid, Closed |
| denialReason | String | No | Denial reason | 1-500 chars |
| payerId | String | Yes | Payer identifier | 1-50 chars |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Claim` → `Patient` (Many-to-One)
- `Claim` → `Encounter` (Many-to-One)
- `Claim` → `InsurancePlan` (Many-to-One)
- `Claim` → `FinancialTransaction` (One-to-Many)
- `Claim` → `ClaimItem` (One-to-Many)

---

#### 30. Payment

**Entity ID:** `PAYMENT`  
**UUID:** `550e8400-e29b-41d4-a716-446655440092`  
**Canonical Name:** Payment  
**Aliases:** PatientPayment, InsurancePayment  
**Description:** Payment received from patient or insurance.  
**Owner Domain:** Finance  
**Lifecycle States:** Received, Applied, Refunded

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| paymentId | UUID | Yes | Unique identifier | Primary Key |
| paymentNumber | String | Yes | Payment number | Unique, PAY-YYYY-NNNNNN |
| patientId | UUID | Yes | Patient | FK to Patient |
| paymentType | Enum | Yes | Payment type | Patient, Insurance, Refund |
| paymentMethod | Enum | Yes | Payment method | Cash, Check, CreditCard, DebitCard, EFT, Insurance |
| amount | Decimal | Yes | Payment amount | Positive decimal |
| currency | String | Yes | Currency | ISO 4217 |
| paymentDate | DateTime | Yes | Payment date | ISO 8601 |
| referenceNumber | String | No | Reference number | 1-100 chars |
| checkNumber | String | No | Check number | 1-50 chars |
| cardLastFour | String | No | Card last 4 digits | 4 digits |
| status | Enum | Yes | Payment status | Received, Applied, Refunded |
| appliedAmount | Decimal | Yes | Amount applied | Positive decimal |
| unappliedAmount | Decimal | Yes | Unapplied amount | Positive decimal |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Payment` → `Patient` (Many-to-One)
- `Payment` → `FinancialTransaction` (One-to-Many)
- `Payment` → `PaymentApplication` (One-to-Many)

---

### Additional Core Entities

#### 31. Allergy

**Entity ID:** `ALLERGY`  
**UUID:** `550e8400-e29b-41d4-a716-446655440100`  
**Canonical Name:** Allergy  
**Aliases:** PatientAllergy, DrugAllergy  
**Description:** Patient allergy or adverse reaction.  
**Owner Domain:** Patient  
**Lifecycle States:** Active, Inactive, Resolved

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| allergyId | UUID | Yes | Unique identifier | Primary Key |
| patientId | UUID | Yes | Patient | FK to Patient |
| allergenType | Enum | Yes | Allergen type | Drug, Food, Environmental, Other |
| allergenName | String | Yes | Allergen name | 1-200 chars |
| reaction | String | Yes | Reaction description | 1-500 chars |
| severity | Enum | Yes | Severity | Mild, Moderate, Severe, LifeThreatening |
| status | Enum | Yes | Allergy status | Active, Inactive, Resolved |
| onsetDate | Date | No | Onset date | Valid date |
| recordedBy | UUID | Yes | Recorder | FK to User |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Allergy` → `Patient` (Many-to-One)
- `Allergy` → `User` (Many-to-One)

---

#### 32. Consent

**Entity ID:** `CONSENT`  
**UUID:** `550e8400-e29b-41d4-a716-446655440101`  
**Canonical Name:** Consent  
**Aliases:** PatientConsent, TreatmentConsent  
**Description:** Patient consent for treatment or data sharing.  
**Owner Domain:** Patient  
**Lifecycle States:** Active, Expired, Revoked

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| consentId | UUID | Yes | Unique identifier | Primary Key |
| patientId | UUID | Yes | Patient | FK to Patient |
| consentType | Enum | Yes | Consent type | Treatment, Research, DataSharing, Imaging |
| description | String | Yes | Consent description | 1-500 chars |
| grantedDate | DateTime | Yes | Grant date | ISO 8601 |
| expirationDate | DateTime | No | Expiration date | ISO 8601 |
| revokedDate | DateTime | No | Revocation date | ISO 8601 |
| status | Enum | Yes | Consent status | Active, Expired, Revoked |
| witnessId | UUID | No | Witness | FK to User |
| documentId | UUID | No | Consent document | FK to Document |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Consent` → `Patient` (Many-to-One)
- `Consent` → `User` (Many-to-One, Witness)
- `Consent` → `Document` (Many-to-One, Optional)

---

#### 33. InsurancePlan

**Entity ID:** `INSURANCE_PLAN`  
**UUID:** `550e8400-e29b-41d4-a716-446655440110`  
**Canonical Name:** InsurancePlan  
**Aliases:** HealthInsurancePlan, PayerPlan  
**Description:** Health insurance plan definition.  
**Owner Domain:** Insurance  
**Lifecycle States:** Active, Inactive

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| planId | UUID | Yes | Unique identifier | Primary Key |
| payerId | String | Yes | Payer identifier | 1-50 chars |
| planName | String | Yes | Plan name | 1-200 chars |
| planType | Enum | Yes | Plan type | HMO, PPO, EPO, POS, Medicare, Medicaid |
| coverageType | Enum | Yes | Coverage type | Individual, Family, Group |
| effectiveDate | Date | Yes | Effective date | Valid date |
| terminationDate | Date | No | Termination date | Future date |
| status | Enum | Yes | Plan status | Active, Inactive |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `InsurancePlan` → `InsuranceCoverage` (One-to-Many)
- `InsurancePlan` → `Claim` (One-to-Many)

---

#### 34. Department

**Entity ID:** `DEPARTMENT`  
**UUID:** `550e8400-e29b-41d4-a716-446655440120`  
**Canonical Name:** Department  
**Aliases:** OrganizationDepartment  
**Description:** Organizational department within hospital.  
**Owner Domain:** Hospital  
**Lifecycle States:** Active, Inactive

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| departmentId | UUID | Yes | Unique identifier | Primary Key |
| departmentCode | String | Yes | Department code | Unique, 1-20 chars |
| hospitalId | UUID | Yes | Hospital | FK to Hospital |
| name | String | Yes | Department name | 1-200 chars |
| departmentType | Enum | Yes | Department type | Clinical, Administrative, Support |
| status | Enum | Yes | Department status | Active, Inactive |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Department` → `Hospital` (Many-to-One)
- `Department` → `Encounter` (One-to-Many)
- `Department` → `Bed` (One-to-Many)

---

#### 35. MedicalDevice

**Entity ID:** `MEDICAL_DEVICE`  
**UUID:** `550e8400-e29b-41d4-a716-446655440130`  
**Canonical Name:** MedicalDevice  
**Aliases:** Device, Equipment  
**Description:** Medical device or equipment record.  
**Owner Domain:** Medical Devices  
**Lifecycle States:** Active, Inactive, Maintenance, Retired

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| deviceId | UUID | Yes | Unique identifier | Primary Key |
| deviceNumber | String | Yes | Device number | Unique, DEV-YYYY-NNNNNN |
| deviceName | String | Yes | Device name | 1-200 chars |
| deviceType | Enum | Yes | Device type | Diagnostic, Therapeutic, Monitoring, LifeSupport |
| manufacturer | String | Yes | Manufacturer | 1-200 chars |
| model | String | Yes | Model | 1-100 chars |
| serialNumber | String | Yes | Serial number | Unique, 1-100 chars |
| locationId | UUID | Yes | Current location | FK to Department |
| status | Enum | Yes | Device status | Active, Inactive, Maintenance, Retired |
| lastMaintenanceDate | Date | No | Last maintenance | Valid date |
| nextMaintenanceDate | Date | No | Next maintenance | Valid date |
| calibrationDate | Date | No | Last calibration | Valid date |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `MedicalDevice` → `Department` (Many-to-One)
- `MedicalDevice` → `DeviceMaintenance` (One-to-Many)
- `MedicalDevice` → `DeviceCalibration` (One-to-Many)

---

#### 36. Notification

**Entity ID:** `NOTIFICATION`  
**UUID:** `550e8400-e29b-41d4-a716-446655440140`  
**Canonical Name:** Notification  
**Aliases:** Alert, Message  
**Description:** System notification or alert.  
**Owner Domain:** Notifications  
**Lifecycle States:** Created, Sent, Delivered, Read, Failed

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| notificationId | UUID | Yes | Unique identifier | Primary Key |
| userId | UUID | Yes | Recipient | FK to User |
| notificationType | Enum | Yes | Notification type | Clinical, Operational, System, Patient |
| channel | Enum | Yes | Delivery channel | Email, SMS, Push, InApp |
| subject | String | Yes | Notification subject | 1-200 chars |
| message | String | Yes | Notification message | 1-5000 chars |
| priority | Enum | Yes | Priority | Low, Normal, High, Urgent |
| status | Enum | Yes | Delivery status | Created, Sent, Delivered, Read, Failed |
| readAt | DateTime | No | Read time | ISO 8601 |
| sentAt | DateTime | No | Send time | ISO 8601 |
| deliveredAt | DateTime | No | Delivery time | ISO 8601 |
| expiresAt | DateTime | No | Expiration time | ISO 8601 |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |

**Relationships:**

- `Notification` → `User` (Many-to-One)

---

#### 37. Document

**Entity ID:** `DOCUMENT`  
**UUID:** `550e8400-e29b-41d4-a716-446655440150`  
**Canonical Name:** Document  
**Aliases:** SystemDocument, ClinicalDocument  
**Description:** System document or file.  
**Owner Domain:** Documents  
**Lifecycle States:** Draft, Published, Archived, Deleted

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| documentId | UUID | Yes | Unique identifier | Primary Key |
| documentNumber | String | Yes | Document number | Unique, DOC-YYYY-NNNNNN |
| title | String | Yes | Document title | 1-200 chars |
| documentType | Enum | Yes | Document type | Clinical, Administrative, Legal, Consent |
| patientId | UUID | No | Associated patient | FK to Patient |
| encounterId | UUID | No | Associated encounter | FK to Encounter |
| ownerId | UUID | Yes | Document owner | FK to User |
| fileUrl | String | Yes | File location | Valid URL |
| fileSize | Integer | Yes | File size (bytes) | 1+ |
| mimeType | String | Yes | MIME type | Valid MIME |
| status | Enum | Yes | Document status | Draft, Published, Archived, Deleted |
| version | Integer | Yes | Version number | 1+ |
| isConfidential | Boolean | Yes | Confidential flag | Default: false |
| retentionDate | Date | No | Retention date | Valid date |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Document` → `User` (Many-to-One, Owner)
- `Document` → `Patient` (Many-to-One, Optional)
- `Document` → `Encounter` (Many-to-One, Optional)
- `Document` → `DocumentVersion` (One-to-Many)
- `Document` → `DocumentAccess` (One-to-Many)

---

#### 38. Workflow

**Entity ID:** `WORKFLOW`  
**UUID:** `550e8400-e29b-41d4-a716-446655440160`  
**Canonical Name:** Workflow  
**Aliases:** ProcessWorkflow, TaskWorkflow  
**Description:** Workflow definition and instance tracking.  
**Owner Domain:** Workflow  
**Lifecycle States:** Draft, Active, Completed, Failed, Cancelled

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| workflowId | UUID | Yes | Unique identifier | Primary Key |
| workflowName | String | Yes | Workflow name | 1-200 chars |
| workflowType | Enum | Yes | Workflow type | Clinical, Operational, Administrative |
| description | String | Yes | Description | 1-1000 chars |
| initiatedBy | UUID | Yes | Initiator | FK to User |
| patientId | UUID | No | Associated patient | FK to Patient |
| encounterId | UUID | No | Associated encounter | FK to Encounter |
| status | Enum | Yes | Workflow status | Draft, Active, Completed, Failed, Cancelled |
| startedAt | DateTime | No | Start time | ISO 8601 |
| completedAt | DateTime | No | Completion time | ISO 8601 |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Workflow` → `User` (Many-to-One, Initiator)
- `Workflow` → `Patient` (Many-to-One, Optional)
- `Workflow` → `WorkflowStep` (One-to-Many)
- `Workflow` → `Task` (One-to-Many)

---

#### 39. Task

**Entity ID:** `TASK`  
**UUID:** `550e8400-e29b-41d4-a716-446655440161`  
**Canonical Name:** Task  
**Aliases:** WorkflowTask, SystemTask  
**Description:** Task within a workflow.  
**Owner Domain:** Workflow  
**Lifecycle States:** Created, Assigned, InProgress, Completed, Failed, Cancelled

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| taskId | UUID | Yes | Unique identifier | Primary Key |
| taskName | String | Yes | Task name | 1-200 chars |
| workflowId | UUID | Yes | Parent workflow | FK to Workflow |
| assignedTo | UUID | No | Assigned user | FK to User |
| dueDate | DateTime | No | Due date | ISO 8601 |
| priority | Enum | Yes | Task priority | Low, Normal, High, Urgent |
| status | Enum | Yes | Task status | Created, Assigned, InProgress, Completed, Failed, Cancelled |
| completedAt | DateTime | No | Completion time | ISO 8601 |
| completedBy | UUID | No | Completer | FK to User |
| result | String | No | Task result | 1-2000 chars |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Task` → `Workflow` (Many-to-One)
- `Task` → `User` (Many-to-One, Assignee)
- `Task` → `User` (Many-to-One, Completer)

---

#### 40. Report

**Entity ID:** `REPORT`  
**UUID:** `550e8400-e29b-41d4-a716-446655440170`  
**Canonical Name:** Report  
**Aliases:** SystemReport, GeneratedReport  
**Description:** Generated report instance.  
**Owner Domain:** Reporting  
**Lifecycle States:** Generating, Completed, Failed, Archived

**Attributes:**

| Attribute | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| reportId | UUID | Yes | Unique identifier | Primary Key |
| reportName | String | Yes | Report name | 1-200 chars |
| reportType | Enum | Yes | Report type | Clinical, Financial, Operational, Regulatory |
| parameters | JSON | Yes | Report parameters | Valid JSON |
| generatedBy | UUID | Yes | Generator | FK to User |
| fileUrl | String | No | Report file URL | Valid URL |
| status | Enum | Yes | Report status | Generating, Completed, Failed, Archived |
| generatedAt | DateTime | No | Generation time | ISO 8601 |
| expiresAt | DateTime | No | Expiration time | ISO 8601 |
| createdAt | DateTime | Yes | Creation timestamp | ISO 8601 |
| updatedAt | DateTime | Yes | Last update timestamp | ISO 8601 |

**Relationships:**

- `Report` → `User` (Many-to-One, Generator)
- `Report` → `ReportSchedule` (Many-to-One, Optional)

---

## Entity Relationship Diagrams

### Core Clinical Entities ERD

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        CORE CLINICAL ENTITIES ERD                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────────┐        ┌──────────────┐        ┌──────────────┐             │
│  │    Patient    │        │   Encounter   │        │     Order     │             │
│  ├──────────────┤        ├──────────────┤        ├──────────────┤             │
│  │ patientId PK │───┐    │ encounterIdPK│───┐    │ orderId PK   │───┐         │
│  │ mrn          │   │    │ patientId FK │   │    │ encounterIdFK│   │         │
│  │ firstName    │   │    │ encounterType│   │    │ patientId FK │   │         │
│  │ lastName     │   │    │ status       │   │    │ orderType    │   │         │
│  │ dateOfBirth  │   │    │ scheduledDate│   │    │ status       │   │         │
│  │ gender       │   │    │ departmentId │   │    │ priority     │   │         │
│  │ status       │   │    └──────────────┘   │    └──────────────┘   │         │
│  └──────────────┘   │           │            │           │            │         │
│         │           │           │            │           │            │         │
│         │           │    ┌──────┴──────┐     │    ┌──────┴──────┐   │         │
│         │           │    │             │     │    │             │   │         │
│         ▼           │    ▼             ▼     │    ▼             ▼   │         │
│  ┌──────────────┐   │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │    Address    │   │  │ Clinical │ │ Vital    │ │ LabOrder │ │ RxOrder  │   │
│  ├──────────────┤   │  │ Document │ │ Signs    │ ├──────────┤ ├──────────┤   │
│  │ addressId PK │   │  ├──────────┤ ├──────────┤ │ labOrderId│ │ rxOrderId│   │
│  │ patientId FK │   │  │ docId PK │ │ vitalId  │ │ orderId  │ │ orderId  │   │
│  │ addressType  │   │  │ encId FK │ │ encId FK │ │ labTest  │ │ medId FK │   │
│  │ addressLine1 │   │  │ authorId │ │ patientId│ │ status   │ │ dosage   │   │
│  │ city         │   │  │ content  │ │ temp     │ └──────────┘ └──────────┘   │
│  │ state        │   │  │ status   │ │ heartRate│        │            │         │
│  └──────────────┘   │  └──────────┘ └──────────┘        │            │         │
│         │           │       │              │             │            │         │
│         │           │       │              │             ▼            ▼         │
│         │           │       │              │        ┌──────────┐ ┌──────────┐  │
│         │           │       │              │        │ Specimen │ │Medication│  │
│         │           │       │              │        ├──────────┤ ├──────────┤  │
│         │           │       │              │        │ specimenId│ │ medId PK │  │
│         │           │       │              │        │ labOrderId│ │ name     │  │
│         │           │       │              │        │ patientId│ │ generic  │  │
│         │           │       │              │        │ type     │ │ ndcCode  │  │
│         │           │       │              │        └──────────┘ └──────────┘  │
│         │           │       │              │             │            │         │
│         │           │       │              │             ▼            ▼         │
│         │           │       │              │        ┌──────────┐ ┌──────────┐  │
│         │           │       │              │        │LabResult │ │AdminRec  │  │
│         │           │       │              │        ├──────────┤ ├──────────┤  │
│         │           │       │              │        │ resultId │ │ adminId  │  │
│         │           │       │              │        │ specId FK│ │ rxOrdId  │  │
│         │           │       │              │        │ value    │ │ patientId│  │
│         │           │       │              │        │ unit     │ │ medId FK │  │
│         │           │       │              │        └──────────┘ └──────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Financial Entities ERD

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        FINANCIAL ENTITIES ERD                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────────┐        ┌──────────────┐        ┌──────────────┐             │
│  │   Patient     │        │  Encounter   │        │   Charge     │             │
│  ├──────────────┤        ├──────────────┤        ├──────────────┤             │
│  │ patientId PK │───┐    │ encounterIdPK│───┐    │ chargeId PK  │───┐         │
│  │ mrn          │   │    │ patientId FK │   │    │ encounterIdFK│   │         │
│  └──────────────┘   │    └──────────────┘   │    │ patientId FK │   │         │
│         │           │           │            │    │ amount       │   │         │
│         │           │           │            │    └──────────────┘   │         │
│         │           │           │            │           │            │         │
│         ▼           │           ▼            │           ▼            │         │
│  ┌──────────────┐   │  ┌──────────────┐     │    ┌──────────────┐   │         │
│  │InsurancePlan │   │  │    Claim      │     │    │  Financial   │   │         │
│  ├──────────────┤   │  ├──────────────┤     │    │ Transaction  │   │         │
│  │ planId PK    │   │  │ claimId PK   │     │    ├──────────────┤   │         │
│  │ payerId      │   │  │ patientId FK │     │    │ transactionId│   │         │
│  │ planName     │   │  │ encounterIdFK│     │    │ patientId FK │   │         │
│  │ planType     │   │  │ insuranceFK  │     │    │ type         │   │         │
│  └──────────────┘   │  │ totalAmount  │     │    │ amount       │   │         │
│         │           │  │ status       │     │    │ status       │   │         │
│         │           │  └──────────────┘     │    └──────────────┘   │         │
│         │           │        │               │           │            │         │
│         │           │        ▼               │           │            │         │
│         │           │  ┌──────────────┐     │           │            │         │
│         │           │  │  ClaimItem   │     │           │            │         │
│         │           │  ├──────────────┤     │           │            │         │
│         │           │  │ claimItemId  │     │           │            │         │
│         │           │  │ claimId FK   │     │           │            │         │
│         │           │  │ chargeId FK  │     │           │            │         │
│         │           │  │ amount       │     │           │            │         │
│         │           │  └──────────────┘     │           │            │         │
│         │           │                       │           │            │         │
│         │           │           │           │           │            │         │
│         │           │           ▼           │           ▼            │         │
│         │           │  ┌──────────────┐     │    ┌──────────────┐   │         │
│         │           │  │   Payment    │     │    │   Refund     │   │         │
│         │           │  ├──────────────┤     │    ├──────────────┤   │         │
│         │           │  │ paymentId PK │     │    │ refundId PK  │   │         │
│         │           │  │ patientId FK │     │    │ paymentId FK │   │         │
│         │           │  │ amount       │     │    │ amount       │   │         │
│         │           │  │ method       │     │    │ reason       │   │         │
│         │           │  └──────────────┘     │    └──────────────┘   │         │
│         │           │        │               │                       │         │
│         │           │        ▼               │                       │         │
│         │           │  ┌──────────────┐     │                       │         │
│         │           │  │  PaymentApp  │     │                       │         │
│         │           │  ├──────────────┤     │                       │         │
│         │           │  │ paymentAppId │     │                       │         │
│         │           │  │ paymentId FK │     │                       │         │
│         │           │  │ claimId FK   │     │                       │         │
│         │           │  │ amount       │     │                       │         │
│         │           │  └──────────────┘     │                       │         │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Relationship Patterns

### 1. Inheritance Pattern (Generalization/Specialization)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         INHERITANCE PATTERN                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Base Entity: Order                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                              Order                                      │   │
│  │  orderId, orderNumber, encounterId, patientId, status, priority        │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                               │                                                 │
│            ┌──────────────────┼──────────────────┐                              │
│            │                  │                  │                              │
│            ▼                  ▼                  ▼                              │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐                  │
│  │    LabOrder     │ │ RadiologyOrder  │ │ MedicationOrder │                  │
│  ├─────────────────┤ ├─────────────────┤ ├─────────────────┤                  │
│  │ labOrderId      │ │ radiologyOrderId│ │ medicationOrdId │                  │
│  │ labTestCode     │ │ modality        │ │ medicationId    │                  │
│  │ specimenType    │ │ bodyPart        │ │ dosage          │                  │
│  │ status          │ │ contrastRequired│ │ route           │                  │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘                  │
│                                                                                 │
│  Implementation: Single Table Inheritance (STI) or Table Per Type (TPT)        │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2. Composition Pattern

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        COMPOSITION PATTERN                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Composite: Encounter                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                             Encounter                                    │   │
│  │  encounterId, patientId, status, scheduledDateTime                      │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                               │                                                 │
│            ┌──────────────────┼──────────────────┐                              │
│            │                  │                  │                              │
│            ▼                  ▼                  ▼                              │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐                  │
│  │ClinicalDocument │ │   VitalSigns    │ │    Diagnosis    │                  │
│  ├─────────────────┤ ├─────────────────┤ ├─────────────────┤                  │
│  │ documentationId │ │ vitalSignsId    │ │ diagnosisId     │                  │
│  │ encounterId FK  │ │ encounterId FK  │ │ encounterId FK  │                  │
│  │ content         │ │ temperature     │ │ icd10Code       │                  │
│  │ status          │ │ heartRate       │ │ status          │                  │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘                  │
│                                                                                 │
│  Rule: Components cannot exist without composite                               │
│  Cascade: Delete composite → Delete all components                             │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 3. Aggregation Pattern

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         AGGREGATION PATTERN                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Aggregate Root: Patient                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                              Patient                                     │   │
│  │  patientId, mrn, firstName, lastName, dateOfBirth, gender               │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                               │                                                 │
│            ┌──────────────────┼──────────────────┐                              │
│            │                  │                  │                              │
│            ▼                  ▼                  ▼                              │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐                  │
│  │     Address     │ │     Allergy     │ │    Consent      │                  │
│  ├─────────────────┤ ├─────────────────┤ ├─────────────────┤                  │
│  │ addressId       │ │ allergyId       │ │ consentId       │                  │
│  │ patientId FK    │ │ patientId FK    │ │ patientId FK    │                  │
│  │ addressLine1    │ │ allergenName    │ │ consentType     │                  │
│  │ city            │ │ severity        │ │ status          │                  │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘                  │
│                                                                                 │
│  Rule: Aggregates can exist independently                                      │
│  Reference: By ID only (not direct object reference)                           │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 4. Association Patterns

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       ASSOCIATION PATTERNS                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ONE-TO-ONE                                                                     │
│  ┌──────────────┐     1:1      ┌──────────────┐                               │
│  │     User     │──────────────│  UserProfile  │                               │
│  └──────────────┘              └──────────────┘                               │
│                                                                                 │
│  ONE-TO-MANY                                                                   │
│  ┌──────────────┐     1:N      ┌──────────────┐                               │
│  │    Patient   │──────────────│  Encounter   │                               │
│  └──────────────┘              └──────────────┘                               │
│                                                                                 │
│  MANY-TO-MANY                                                                  │
│  ┌──────────────┐     M:N      ┌──────────────┐                               │
│  │     Role     │──────────────│  Permission  │                               │
│  └──────────────┘     via       └──────────────┘                               │
│                 ┌──────────────┐                                               │
│                 │RolePermission│                                               │
│                 └──────────────┘                                               │
│                                                                                 │
│  SELF-REFERENCING                                                              │
│  ┌──────────────┐              ┌──────────────┐                               │
│  │  Department  │──────────────│  Department  │                               │
│  │  (Parent)    │     1:N      │  (Child)     │                               │
│  └──────────────┘              └──────────────┘                               │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Aggregate Root Definitions

### Patient Aggregate

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        PATIENT AGGREGATE ROOT                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Aggregate Root: Patient                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                              Patient                                     │   │
│  │  patientId (UUID) - Primary Key                                         │   │
│  │  mrn (String) - Medical Record Number, Unique                           │   │
│  │  firstName (String)                                                     │   │
│  │  lastName (String)                                                      │   │
│  │  dateOfBirth (Date)                                                     │   │
│  │  gender (Enum)                                                          │   │
│  │  status (Enum) - Active, Inactive, Deceased, Merged                     │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  Child Entities (Composition):                                                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐          │
│  │   Address    │ │   Allergy    │ │  Medication  │ │   Consent    │          │
│  │ 1:N, Cascade │ │ 1:N, Cascade │ │ 1:N, Cascade │ │ 1:N, Cascade │          │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘          │
│                                                                                 │
│  Related Entities (Aggregation):                                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                           │
│  │  Encounter   │ │  Insurance   │ │   Consent    │                           │
│  │ 1:N, By ID   │ │ 1:N, By ID   │ │ 1:N, By ID   │                           │
│  └──────────────┘ └──────────────┘ └──────────────┘                           │
│                                                                                 │
│  Invariants:                                                                   │
│  1. MRN must be unique across system                                           │
│  2. Date of birth cannot be in the future                                      │
│  3. Deceased patients cannot have future encounters                            │
│  4. Merged patients must reference surviving patient                           │
│                                                                                 │
│  Business Rules:                                                               │
│  1. Patient must have at least one address                                     │
│  2. Emergency contact recommended                                              │
│  3. Insurance information optional but recommended                             │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Encounter Aggregate

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        ENCOUNTER AGGREGATE ROOT                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Aggregate Root: Encounter                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                             Encounter                                    │   │
│  │  encounterId (UUID) - Primary Key                                       │   │
│  │  encounterNumber (String) - Unique                                      │   │
│  │  patientId (UUID) - Foreign Key                                         │   │
│  │  encounterType (Enum)                                                   │   │
│  │  status (Enum) - Scheduled, CheckedIn, InProgress, Completed           │   │
│  │  scheduledDateTime (DateTime)                                           │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  Child Entities (Composition):                                                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐          │
│  │   Clinical   │ │  VitalSigns  │ │  Diagnosis   │ │    Order     │          │
│  │ Documentation│ │ 1:N, Cascade │ │ 1:N, Cascade │ │ 1:N, Cascade │          │
│  │ 1:N, Cascade │ └──────────────┘ └──────────────┘ └──────────────┘          │
│  └──────────────┘                                                              │
│                                                                                 │
│  Related Entities (Aggregation):                                               │
│  ┌──────────────┐ ┌──────────────┐                                            │
│  │  Department  │ │   Hospital   │                                            │
│  │ 1:1, By ID   │ │ 1:1, By ID   │                                            │
│  └──────────────┘ └──────────────┘                                            │
│                                                                                 │
│  Invariants:                                                                   │
│  1. Encounter must be associated with active patient                           │
│  2. Completed encounters cannot be cancelled                                   │
│  3. Inpatient encounters require bed assignment                                │
│                                                                                 │
│  State Transitions:                                                            │
│  Scheduled → CheckedIn → InProgress → Completed                                │
│  Scheduled → Cancelled                                                         │
│  CheckedIn → NoShow                                                            │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Order Aggregate

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          ORDER AGGREGATE ROOT                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Aggregate Root: Order                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                               Order                                     │   │
│  │  orderId (UUID) - Primary Key                                           │   │
│  │  orderNumber (String) - Unique                                          │   │
│  │  encounterId (UUID) - Foreign Key                                       │   │
│  │  patientId (UUID) - Foreign Key                                         │   │
│  │  orderType (Enum) - Laboratory, Radiology, Pharmacy, Consult           │   │
│  │  status (Enum) - Draft, Submitted, Accepted, Completed, Cancelled      │   │
│  │  priority (Enum) - Routine, Urgent, Stat                                │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  Specialized Subtypes (Inheritance):                                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                          │
│  │   LabOrder   │ │RadiologyOrder│ │MedicationOrder│                          │
│  │ labTestCode  │ │ modality     │ │ medicationId  │                          │
│  │ specimenType │ │ bodyPart     │ │ dosage        │                          │
│  └──────────────┘ └──────────────┘ └──────────────┘                          │
│                                                                                 │
│  Child Entities (Composition):                                                 │
│  ┌──────────────┐                                                              │
│  │   Result     │                                                              │
│  │ 1:N, Cascade │                                                              │
│  └──────────────┘                                                              │
│                                                                                 │
│  Invariants:                                                                   │
│  1. Order must be associated with active encounter                             │
│  2. Cancelled orders cannot be reactivated                                     │
│  3. Stat orders must be processed within 1 hour                                │
│                                                                                 │
│  State Transitions:                                                            │
│  Draft → Submitted → Accepted → InProgress → Completed                         │
│  Draft → Cancelled                                                             │
│  Submitted → Rejected                                                          │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Value Object Definitions

### Address Value Object

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         ADDRESS VALUE OBJECT                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Value Object: Address                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                              Address                                     │   │
│  │  addressType (Enum) - Home, Work, Temporary, Mailing                    │   │
│  │  addressLine1 (String) - Street address                                 │   │
│  │  addressLine2 (String) - Apartment/Suite (Optional)                     │   │
│  │  city (String)                                                          │   │
│  │  state (String) - State/Province                                        │   │
│  │  postalCode (String) - ZIP/Postal code                                  │   │
│  │  country (String) - ISO 3166-1                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  Properties:                                                                   │
│  - Immutable (no setters)                                                      │
│  - Equality by all attributes                                                  │
│  - Can be null (optional address)                                              │
│                                                                                 │
│  Methods:                                                                      │
│  - getFullAddress() → String                                                   │
│  - getFormattedAddress() → String                                              │
│  - isUSAddress() → Boolean                                                     │
│  - getValidationErrors() → List<String>                                        │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### BloodType Value Object

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        BLOOD TYPE VALUE OBJECT                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Value Object: BloodType                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                             BloodType                                    │   │
│  │  aboGroup (Enum) - A, B, AB, O                                          │   │
│  │  rhFactor (Enum) - Positive, Negative                                   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  Properties:                                                                   │
│  - Immutable                                                                   │
│  - Equality by ABO + Rh                                                       │
│  - 8 valid combinations                                                       │
│                                                                                 │
│  Valid Types:                                                                  │
│  A+, A-, B+, B-, AB+, AB-, O+, O-                                             │
│                                                                                 │
│  Methods:                                                                      │
│  - canReceiveFrom(BloodType) → Boolean                                         │
│  - canDonateTo(BloodType) → Boolean                                            │
│  - toString() → String (e.g., "A+")                                            │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Dosage Value Object

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         DOSAGE VALUE OBJECT                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Value Object: Dosage                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                              Dosage                                      │   │
│  │  value (Decimal) - Numeric value                                         │   │
│  │  unit (String) - Unit of measure                                        │   │
│  │  route (Enum) - Oral, IV, IM, SC, Topical, Inhaled                     │   │
│  │  frequency (String) - Dosing frequency                                  │   │
│  │  duration (String) - Treatment duration                                 │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  Properties:                                                                   │
│  - Immutable                                                                   │
│  - Equality by all attributes                                                  │
│                                                                                 │
│  Methods:                                                                      │
│  - getDailyDose() → Decimal                                                    │
│  - getTotalDose() → Decimal                                                    │
│  - getFrequencyPerDay() → Integer                                              │
│  - isValid() → Boolean                                                         │
│  - toString() → String                                                         │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Entity Lifecycle Management

### Lifecycle State Machine

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    ENTITY LIFECYCLE STATE MACHINE                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  PATIENT LIFECYCLE                                                              │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐                    │
│  │ Pending │───►│ Active  │───►│Inactive │    │Deceased │                    │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘                    │
│                       │                │             ▲                         │
│                       │                │             │                         │
│                       └────────────────┴─────────────┘                         │
│                                                                                 │
│  ENCOUNTER LIFECYCLE                                                            │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐            │
│  │ Scheduled │───►│ CheckedIn │───►│InProgress │───►│ Completed │            │
│  └───────────┘    └───────────┘    └───────────┘    └───────────┘            │
│        │                │                                                  │    │
│        │                ▼                                                  │    │
│        │           ┌───────────┐                                           │    │
│        └──────────►│  NoShow   │                                           │    │
│                    └───────────┘                                           │    │
│                                                                                 │
│  ORDER LIFECYCLE                                                                │
│  ┌─────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐              │
│  │  Draft  │───►│ Submitted │───►│ Accepted  │───►│InProgress │              │
│  └─────────┘    └───────────┘    └───────────┘    └───────────┘              │
│        │                │                              │                       │
│        │                ▼                              ▼                       │
│        │           ┌───────────┐              ┌───────────┐                   │
│        └──────────►│ Cancelled │              │ Completed │                   │
│                    └───────────┘              └───────────┘                   │
│                                                                                 │
│  DOCUMENT LIFECYCLE                                                             │
│  ┌─────────┐    ┌───────────┐    ┌─────────┐    ┌─────────┐                  │
│  │  Draft  │───►│ Published │───►│Archived │───►│ Deleted │                  │
│  └─────────┘    └───────────┘    └─────────┘    └─────────┘                  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Lifecycle Rules

| Entity | Valid Transitions | Triggers |
|--------|-------------------|----------|
| Patient | Pending → Active | Registration complete |
| Patient | Active → Inactive | Inactivity period |
| Patient | Active → Deceased | Death recorded |
| Encounter | Scheduled → CheckedIn | Patient arrives |
| Encounter | CheckedIn → InProgress | Provider starts visit |
| Encounter | InProgress → Completed | Visit finished |
| Encounter | Scheduled → Cancelled | Cancellation requested |
| Encounter | CheckedIn → NoShow | Patient no-show |
| Order | Draft → Submitted | Provider submits |
| Order | Submitted → Accepted | Department accepts |
| Order | Accepted → InProgress | Processing started |
| Order | InProgress → Completed | Order fulfilled |
| Order | Draft → Cancelled | Cancellation requested |
| Document | Draft → Published | Publication approved |
| Document | Published → Archived | Retention period |
| Document | Archived → Deleted | Deletion approved |

---

## Appendix: Entity Reference Table

| Entity ID | Entity Name | Domain | Aggregate Root | Lifecycle States |
|-----------|-------------|--------|----------------|------------------|
| USER | User | Identity | Yes | Pending, Active, Inactive, Suspended, Deleted |
| USER_PROFILE | UserProfile | Identity | No | Draft, Complete, Archived |
| ROLE | Role | Authorization | Yes | Draft, Active, Inactive, Archived |
| PERMISSION | Permission | Authorization | Yes | Active, Inactive |
| AUDIT_LOG | AuditLog | Audit | Yes | Created |
| SESSION | Session | Identity | Yes | Active, Expired, Revoked |
| PATIENT | Patient | Patient | Yes | Active, Inactive, Deceased, Merged |
| ADDRESS | Address | Patient | No | Active, Inactive |
| ENCOUNTER | Encounter | Encounter | Yes | Scheduled, CheckedIn, InProgress, Completed, Cancelled, NoShow |
| CLINICAL_DOCUMENTATION | ClinicalDocumentation | Encounter | No | Draft, InReview, Signed, Amended, Voided |
| VITAL_SIGNS | VitalSigns | Encounter | No | Recorded |
| DIAGNOSIS | Diagnosis | Encounter | No | Active, Inactive, Resolved |
| ORDER | Order | Orders | Yes | Draft, Submitted, Accepted, InProgress, Completed, Cancelled, Expired |
| LAB_ORDER | LabOrder | Laboratory | No | Submitted, Accepted, Rejected, InProgress, Completed |
| SPECIMEN | Specimen | Laboratory | Yes | Collected, Received, Processed, Tested, Archived, Rejected |
| LAB_RESULT | LabResult | Laboratory | No | Preliminary, Final, Amended, Cancelled |
| RADIOLOGY_ORDER | RadiologyOrder | Radiology | No | Submitted, Scheduled, InProgress, Completed |
| IMAGING_STUDY | ImagingStudy | Radiology | Yes | Started, Completed, Archived |
| RADIOLOGY_REPORT | RadiologyReport | Radiology | No | Dictated, Transcribed, Signed, Amended |
| MEDICATION_ORDER | MedicationOrder | Pharmacy | No | Submitted, Verified, Dispensed, Administered, Completed, Cancelled |
| MEDICATION | Medication | Pharmacy | Yes | Active, Inactive, Discontinued |
| DISPENSING_RECORD | DispensingRecord | Pharmacy | No | Dispensed, PickedUp, Returned |
| ADMINISTRATION_RECORD | AdministrationRecord | Pharmacy | No | Scheduled, Administered, Missed, Refused |
| HOSPITAL | Hospital | Hospital | Yes | Active, Inactive, Closed |
| DEPARTMENT | Department | Hospital | No | Active, Inactive, Merged |
| BED | Bed | Hospital | No | Available, Occupied, Reserved, Maintenance, OutOfService |
| APPOINTMENT | Appointment | Scheduling | Yes | Scheduled, Confirmed, CheckedIn, InProgress, Completed, Cancelled, NoShow |
| FINANCIAL_TRANSACTION | FinancialTransaction | Finance | Yes | Pending, Posted, Reversed, Voided |
| CLAIM | Claim | Revenue Cycle | Yes | Draft, Submitted, Accepted, Denied, Pending, Paid, Closed |
| PAYMENT | Payment | Finance | Yes | Received, Applied, Refunded |
| ALLERGY | Allergy | Patient | No | Active, Inactive, Resolved |
| CONSENT | Consent | Patient | No | Active, Expired, Revoked |
| INSURANCE_PLAN | InsurancePlan | Insurance | Yes | Active, Inactive |
| MEDICAL_DEVICE | MedicalDevice | Medical Devices | Yes | Active, Inactive, Maintenance, Retired |
| NOTIFICATION | Notification | Notifications | Yes | Created, Sent, Delivered, Read, Failed |
| DOCUMENT | Document | Documents | Yes | Draft, Published, Archived, Deleted |
| WORKFLOW | Workflow | Workflow | Yes | Draft, Active, Completed, Failed, Cancelled |
| TASK | Task | Workflow | No | Created, Assigned, InProgress, Completed, Failed, Cancelled |
| REPORT | Report | Reporting | Yes | Generating, Completed, Failed, Archived |

---

**Document Classification:** CANONICAL MODEL  
**Review Cycle:** Quarterly  
**Next Review Date:** 2026-09-25  
**Approved By:** NHDOS Architecture Board