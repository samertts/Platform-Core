# National Healthcare Digital Operating System (NHDOS) - Entity Event Catalog

**Version:** 1.0.0  
**Status:** CANONICAL MODEL  
**Last Updated:** 2026-06-25  
**Classification:** Production-Ready Documentation

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Event Naming Conventions](#event-naming-conventions)
3. [Event Types](#event-types)
4. [Complete Event Registry](#complete-event-registry)
5. [Event Payload Specifications](#event-payload-specifications)
6. [Event Versioning Strategy](#event-versioning-strategy)
7. [Event Immutability Rules](#event-immutability-rules)
8. [Event Processing Patterns](#event-processing-patterns)

---

## Executive Summary

This document serves as the **CANONICAL EVENT CATALOG** for the National Healthcare Digital Operating System (NHDOS). It defines 130+ domain events with complete specifications including triggers, payload schemas, and processing rules.

### Event Categories

| Category | Event Count | Description |
|----------|-------------|-------------|
| **Foundation** | 15 | Identity and access events |
| **Clinical Care** | 45 | Patient care events |
| **Business Operations** | 35 | Financial and operational |
| **Intelligence** | 15 | Analytics and AI events |
| **Engagement** | 10 | Patient engagement events |
| **System** | 10 | Platform and integration events |
| **Total** | **130** | Complete event inventory |

---

## Event Naming Conventions

### Naming Pattern

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         EVENT NAMING CONVENTION                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Format: EntityPastTenseVerb                                                    │
│                                                                                 │
│  Examples:                                                                     │
│  • PatientRegistered                                                            │
│  • EncounterCompleted                                                           │
│  • LabResultFinal                                                               │
│  • MedicationAdministered                                                       │
│  • ClaimSubmitted                                                               │
│                                                                                 │
│  Rules:                                                                        │
│  1. PascalCase formatting                                                       │
│  2. Past tense verb (Registered, Completed, Final)                             │
│  3. Entity name as subject                                                     │
│  4. No abbreviations                                                            │
│  5. Maximum 50 characters                                                      │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Verb Categories

| Verb Type | Examples | Use Case |
|-----------|----------|----------|
| **Created** | PatientRegistered, OrderCreated | Entity creation |
| **Updated** | PatientDemographicsUpdated, StatusChanged | Entity modification |
| **Completed** | EncounterCompleted, LabResultFinal | Process completion |
| **Cancelled** | AppointmentCancelled, OrderCancelled | Process cancellation |
| **StatusChanged** | BedStatusChanged, ClaimStatusChanged | State transitions |
| **Reported** | SafetyEventReported, CriticalValueReported | Reporting events |
| **Assigned** | BedAssigned, TaskAssigned | Assignment events |
| **Revoked** | ConsentRevoked, RoleRevoked | Revocation events |

---

## Event Types

### Event Type Classification

| Type | Description | Immutability | Retention |
|------|-------------|--------------|-----------|
| **Domain Event** | Business state change | Immutable | 7 years |
| **Integration Event** | Cross-domain communication | Immutable | 3 years |
| **System Event** | Platform operations | Immutable | 1 year |
| **Audit Event** | Compliance logging | Immutable | 10 years |

### Event Structure

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         EVENT STRUCTURE                                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  {                                                                              │
│    "eventId": "550e8400-e29b-41d4-a716-446655440000",                         │
│    "eventType": "PatientRegistered",                                            │
│    "eventVersion": "1.0.0",                                                     │
│    "timestamp": "2026-06-25T14:30:00Z",                                        │
│    "source": "patient-service",                                                 │
│    "correlationId": "abc-123-def-456",                                         │
│    "causationId": "evt-789-ghi-012",                                           │
│    "tenantId": "tenant-001",                                                    │
│    "aggregateId": "patient-uuid-123",                                          │
│    "payload": {                                                                 │
│      // Event-specific data                                                    │
│    },                                                                           │
│    "metadata": {                                                                │
│      "userId": "user-uuid-456",                                                │
│      "ipAddress": "192.168.1.100",                                             │
│      "userAgent": "Mozilla/5.0"                                                │
│    }                                                                            │
│  }                                                                              │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Complete Event Registry

### Foundation Domain Events

#### 1. UserRegistered

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-001 |
| **Event Name** | `UserRegistered` |
| **Trigger Entity** | User |
| **Event Type** | Created |
| **Description** | New user account created in the system |
| **Trigger Action** | POST /auth/register |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "UserRegistered",
  "timestamp": "ISO 8601",
  "payload": {
    "userId": "UUID",
    "username": "string",
    "email": "string",
    "firstName": "string",
    "lastName": "string",
    "status": "Pending",
    "createdBy": "UUID"
  }
}
```

---

#### 2. UserActivated

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-002 |
| **Event Name** | `UserActivated` |
| **Trigger Entity** | User |
| **Event Type** | StatusChanged |
| **Description** | User account activated and ready for use |
| **Trigger Action** | Email verification complete |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "UserActivated",
  "timestamp": "ISO 8601",
  "payload": {
    "userId": "UUID",
    "activatedAt": "ISO 8601",
    "activatedBy": "UUID",
    "previousStatus": "Pending",
    "newStatus": "Active"
  }
}
```

---

#### 3. UserDeactivated

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-003 |
| **Event Name** | `UserDeactivated` |
| **Trigger Entity** | User |
| **Event Type** | StatusChanged |
| **Description** | User account deactivated |
| **Trigger Action** | Admin action or inactivity |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "UserDeactivated",
  "timestamp": "ISO 8601",
  "payload": {
    "userId": "UUID",
    "deactivatedAt": "ISO 8601",
    "deactivatedBy": "UUID",
    "reason": "string",
    "previousStatus": "Active",
    "newStatus": "Inactive"
  }
}
```

---

#### 4. PasswordChanged

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-004 |
| **Event Name** | `PasswordChanged` |
| **Trigger Entity** | User |
| **Event Type** | Updated |
| **Description** | User password updated |
| **Trigger Action** | PUT /auth/password |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "PasswordChanged",
  "timestamp": "ISO 8601",
  "payload": {
    "userId": "UUID",
    "changedAt": "ISO 8601",
    "changedBy": "UUID",
    "ipAddress": "string",
    "forceLogout": "boolean"
  }
}
```

---

#### 5. MFATokenGenerated

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-005 |
| **Event Name** | `MFATokenGenerated` |
| **Trigger Entity** | MFAConfiguration |
| **Event Type** | Created |
| **Description** | Multi-factor authentication token generated |
| **Trigger Action** | POST /auth/mfa/generate |
| **Immutability** | Immutable |
| **Retention** | 1 year |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "MFATokenGenerated",
  "timestamp": "ISO 8601",
  "payload": {
    "userId": "UUID",
    "mfaType": "string",
    "generatedAt": "ISO 8601",
    "expiresAt": "ISO 8601"
  }
}
```

---

#### 6. SessionCreated

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-006 |
| **Event Name** | `SessionCreated` |
| **Trigger Entity** | Session |
| **Event Type** | Created |
| **Description** | User session started |
| **Trigger Action** | POST /auth/login |
| **Immutability** | Immutable |
| **Retention** | 1 year |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "SessionCreated",
  "timestamp": "ISO 8601",
  "payload": {
    "sessionId": "UUID",
    "userId": "UUID",
    "ipAddress": "string",
    "userAgent": "string",
    "expiresAt": "ISO 8601"
  }
}
```

---

#### 7. SessionExpired

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-007 |
| **Event Name** | `SessionExpired` |
| **Trigger Entity** | Session |
| **Event Type** | StatusChanged |
| **Description** | User session expired |
| **Trigger Action** | Automatic expiration |
| **Immutability** | Immutable |
| **Retention** | 1 year |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "SessionExpired",
  "timestamp": "ISO 8601",
  "payload": {
    "sessionId": "UUID",
    "userId": "UUID",
    "expiredAt": "ISO 8601",
    "duration": "integer"
  }
}
```

---

#### 8. RoleAssigned

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-008 |
| **Event Name** | `RoleAssigned` |
| **Trigger Entity** | UserRoleAssignment |
| **Event Type** | Created |
| **Description** | Role assigned to user |
| **Trigger Action** | POST /roles/{roleId}/assign |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "RoleAssigned",
  "timestamp": "ISO 8601",
  "payload": {
    "userId": "UUID",
    "roleId": "UUID",
    "roleName": "string",
    "assignedAt": "ISO 8601",
    "assignedBy": "UUID"
  }
}
```

---

#### 9. RoleRevoked

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-009 |
| **Event Name** | `RoleRevoked` |
| **Trigger Entity** | UserRoleAssignment |
| **Event Type** | Deleted |
| **Description** | Role revoked from user |
| **Trigger Action** | DELETE /roles/{roleId}/revoke |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "RoleRevoked",
  "timestamp": "ISO 8601",
  "payload": {
    "userId": "UUID",
    "roleId": "UUID",
    "roleName": "string",
    "revokedAt": "ISO 8601",
    "revokedBy": "UUID",
    "reason": "string"
  }
}
```

---

#### 10. LoginFailed

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-010 |
| **Event Name** | `LoginFailed` |
| **Trigger Entity** | User |
| **Event Type** | SecurityEvent |
| **Description** | Failed login attempt detected |
| **Trigger Action** | POST /auth/login (failed) |
| **Immutability** | Immutable |
| **Retention** | 1 year |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "LoginFailed",
  "timestamp": "ISO 8601",
  "payload": {
    "userId": "UUID",
    "username": "string",
    "ipAddress": "string",
    "userAgent": "string",
    "failureReason": "string",
    "attemptNumber": "integer"
  }
}
```

---

### Patient Domain Events

#### 11. PatientRegistered

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-011 |
| **Event Name** | `PatientRegistered` |
| **Trigger Entity** | Patient |
| **Event Type** | Created |
| **Description** | New patient registered in the system |
| **Trigger Action** | POST /patients |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "PatientRegistered",
  "timestamp": "ISO 8601",
  "payload": {
    "patientId": "UUID",
    "mrn": "string",
    "firstName": "string",
    "lastName": "string",
    "dateOfBirth": "ISO 8601",
    "gender": "string",
    "status": "Active",
    "createdBy": "UUID"
  }
}
```

---

#### 12. PatientDemographicsUpdated

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-012 |
| **Event Name** | `PatientDemographicsUpdated` |
| **Trigger Entity** | Patient |
| **Event Type** | Updated |
| **Description** | Patient demographic information changed |
| **Trigger Action** | PUT /patients/{patientId} |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "PatientDemographicsUpdated",
  "timestamp": "ISO 8601",
  "payload": {
    "patientId": "UUID",
    "updatedFields": ["string"],
    "previousValues": {},
    "newValues": {},
    "updatedBy": "UUID"
  }
}
```

---

#### 13. PatientMerged

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-013 |
| **Event Name** | `PatientMerged` |
| **Trigger Entity** | Patient |
| **Event Type** | StatusChanged |
| **Description** | Duplicate patient records merged |
| **Trigger Action** | POST /patients/merge |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "PatientMerged",
  "timestamp": "ISO 8601",
  "payload": {
    "survivingPatientId": "UUID",
    "mergedPatientId": "UUID",
    "mergedAt": "ISO 8601",
    "mergedBy": "UUID",
    "reason": "string"
  }
}
```

---

#### 14. AllergyRecorded

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-014 |
| **Event Name** | `AllergyRecorded` |
| **Trigger Entity** | Allergy |
| **Event Type** | Created |
| **Description** | New allergy documented for patient |
| **Trigger Action** | POST /patients/{patientId}/allergies |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "AllergyRecorded",
  "timestamp": "ISO 8601",
  "payload": {
    "allergyId": "UUID",
    "patientId": "UUID",
    "allergenType": "string",
    "allergenName": "string",
    "reaction": "string",
    "severity": "string",
    "recordedBy": "UUID"
  }
}
```

---

#### 15. AllergyUpdated

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-015 |
| **Event Name** | `AllergyUpdated` |
| **Trigger Entity** | Allergy |
| **Event Type** | Updated |
| **Description** | Existing allergy information modified |
| **Trigger Action** | PUT /patients/{patientId}/allergies/{allergyId} |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "AllergyUpdated",
  "timestamp": "ISO 8601",
  "payload": {
    "allergyId": "UUID",
    "patientId": "UUID",
    "updatedFields": ["string"],
    "previousValues": {},
    "newValues": {},
    "updatedBy": "UUID"
  }
}
```

---

#### 16. MedicationRecorded

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-016 |
| **Event Name** | `MedicationRecorded` |
| **Trigger Entity** | Medication |
| **Event Type** | Created |
| **Description** | New medication documented for patient |
| **Trigger Action** | POST /patients/{patientId}/medications |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "MedicationRecorded",
  "timestamp": "ISO 8601",
  "payload": {
    "medicationId": "UUID",
    "patientId": "UUID",
    "medicationName": "string",
    "dosage": "string",
    "frequency": "string",
    "recordedBy": "UUID"
  }
}
```

---

#### 17. MedicationDiscontinued

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-017 |
| **Event Name** | `MedicationDiscontinued` |
| **Trigger Entity** | Medication |
| **Event Type** | StatusChanged |
| **Description** | Patient medication discontinued |
| **Trigger Action** | PUT /patients/{patientId}/medications/{medicationId} |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "MedicationDiscontinued",
  "timestamp": "ISO 8601",
  "payload": {
    "medicationId": "UUID",
    "patientId": "UUID",
    "discontinuedAt": "ISO 8601",
    "discontinuedBy": "UUID",
    "reason": "string"
  }
}
```

---

#### 18. ImmunizationRecorded

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-018 |
| **Event Name** | `ImmunizationRecorded` |
| **Trigger Entity** | Immunization |
| **Event Type** | Created |
| **Description** | New immunization documented for patient |
| **Trigger Action** | POST /patients/{patientId}/immunizations |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "ImmunizationRecorded",
  "timestamp": "ISO 8601",
  "payload": {
    "immunizationId": "UUID",
    "patientId": "UUID",
    "vaccineName": "string",
    "administrationDate": "ISO 8601",
    "lotNumber": "string",
    "administeredBy": "UUID"
  }
}
```

---

#### 19. PatientConsentGranted

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-019 |
| **Event Name** | `PatientConsentGranted` |
| **Trigger Entity** | Consent |
| **Event Type** | Created |
| **Description** | Patient consent obtained |
| **Trigger Action** | POST /patients/{patientId}/consents |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "PatientConsentGranted",
  "timestamp": "ISO 8601",
  "payload": {
    "consentId": "UUID",
    "patientId": "UUID",
    "consentType": "string",
    "grantedAt": "ISO 8601",
    "expirationDate": "ISO 8601",
    "witnessId": "UUID"
  }
}
```

---

#### 20. PatientConsentRevoked

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-020 |
| **Event Name** | `PatientConsentRevoked` |
| **Trigger Entity** | Consent |
| **Event Type** | StatusChanged |
| **Description** | Patient consent withdrawn |
| **Trigger Action** | DELETE /patients/{patientId}/consents/{consentId} |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "PatientConsentRevoked",
  "timestamp": "ISO 8601",
  "payload": {
    "consentId": "UUID",
    "patientId": "UUID",
    "revokedAt": "ISO 8601",
    "revokedBy": "UUID",
    "reason": "string"
  }
}
```

---

#### 21. PatientDeceased

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-021 |
| **Event Name** | `PatientDeceased` |
| **Trigger Entity** | Patient |
| **Event Type** | StatusChanged |
| **Description** | Patient death recorded |
| **Trigger Action** | PUT /patients/{patientId}/deceased |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "PatientDeceased",
  "timestamp": "ISO 8601",
  "payload": {
    "patientId": "UUID",
    "deceasedDate": "ISO 8601",
    "causeOfDeath": "string",
    "reportedBy": "UUID"
  }
}
```

---

### Encounter Domain Events

#### 22. EncounterScheduled

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-022 |
| **Event Name** | `EncounterScheduled` |
| **Trigger Entity** | Encounter |
| **Event Type** | Created |
| **Description** | New healthcare encounter scheduled |
| **Trigger Action** | POST /encounters |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "EncounterScheduled",
  "timestamp": "ISO 8601",
  "payload": {
    "encounterId": "UUID",
    "encounterNumber": "string",
    "patientId": "UUID",
    "encounterType": "string",
    "scheduledDateTime": "ISO 8601",
    "departmentId": "UUID",
    "primaryProviderId": "UUID"
  }
}
```

---

#### 23. EncounterCheckedIn

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-023 |
| **Event Name** | `EncounterCheckedIn` |
| **Trigger Entity** | Encounter |
| **Event Type** | StatusChanged |
| **Description** | Patient checked in for encounter |
| **Trigger Action** | POST /encounters/{encounterId}/checkin |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "EncounterCheckedIn",
  "timestamp": "ISO 8601",
  "payload": {
    "encounterId": "UUID",
    "patientId": "UUID",
    "checkedInAt": "ISO 8601",
    "checkedInBy": "UUID",
    "previousStatus": "Scheduled",
    "newStatus": "CheckedIn"
  }
}
```

---

#### 24. EncounterInProgress

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-024 |
| **Event Name** | `EncounterInProgress` |
| **Trigger Entity** | Encounter |
| **Event Type** | StatusChanged |
| **Description** | Encounter actively in progress |
| **Trigger Action** | POST /encounters/{encounterId}/start |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "EncounterInProgress",
  "timestamp": "ISO 8601",
  "payload": {
    "encounterId": "UUID",
    "patientId": "UUID",
    "startedAt": "ISO 8601",
    "startedBy": "UUID",
    "previousStatus": "CheckedIn",
    "newStatus": "InProgress"
  }
}
```

---

#### 25. EncounterCompleted

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-025 |
| **Event Name** | `EncounterCompleted` |
| **Trigger Entity** | Encounter |
| **Event Type** | StatusChanged |
| **Description** | Encounter finished |
| **Trigger Action** | POST /encounters/{encounterId}/complete |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "EncounterCompleted",
  "timestamp": "ISO 8601",
  "payload": {
    "encounterId": "UUID",
    "patientId": "UUID",
    "completedAt": "ISO 8601",
    "completedBy": "UUID",
    "duration": "integer",
    "previousStatus": "InProgress",
    "newStatus": "Completed"
  }
}
```

---

#### 26. EncounterCancelled

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-026 |
| **Event Name** | `EncounterCancelled` |
| **Trigger Entity** | Encounter |
| **Event Type** | StatusChanged |
| **Description** | Encounter cancelled |
| **Trigger Action** | POST /encounters/{encounterId}/cancel |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "EncounterCancelled",
  "timestamp": "ISO 8601",
  "payload": {
    "encounterId": "UUID",
    "patientId": "UUID",
    "cancelledAt": "ISO 8601",
    "cancelledBy": "UUID",
    "reason": "string",
    "previousStatus": "string",
    "newStatus": "Cancelled"
  }
}
```

---

#### 27. EncounterNoShow

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-027 |
| **Event Name** | `EncounterNoShow` |
| **Trigger Entity** | Encounter |
| **Event Type** | StatusChanged |
| **Description** | Patient did not attend scheduled encounter |
| **Trigger Action** | Automatic (after grace period) |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "EncounterNoShow",
  "timestamp": "ISO 8601",
  "payload": {
    "encounterId": "UUID",
    "patientId": "UUID",
    "scheduledDateTime": "ISO 8601",
    "detectedAt": "ISO 8601",
    "previousStatus": "Scheduled",
    "newStatus": "NoShow"
  }
}
```

---

#### 28. ClinicalDocumentationCreated

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-028 |
| **Event Name** | `ClinicalDocumentationCreated` |
| **Trigger Entity** | ClinicalDocumentation |
| **Event Type** | Created |
| **Description** | New clinical document created |
| **Trigger Action** | POST /encounters/{encounterId}/documents |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "ClinicalDocumentationCreated",
  "timestamp": "ISO 8601",
  "payload": {
    "documentationId": "UUID",
    "encounterId": "UUID",
    "patientId": "UUID",
    "documentType": "string",
    "authorId": "UUID",
    "status": "Draft"
  }
}
```

---

#### 29. ClinicalDocumentationSigned

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-029 |
| **Event Name** | `ClinicalDocumentationSigned` |
| **Trigger Entity** | ClinicalDocumentation |
| **Event Type** | StatusChanged |
| **Description** | Clinical document signed and finalized |
| **Trigger Action** | POST /encounters/{encounterId}/documents/{docId}/sign |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "ClinicalDocumentationSigned",
  "timestamp": "ISO 8601",
  "payload": {
    "documentationId": "UUID",
    "encounterId": "UUID",
    "patientId": "UUID",
    "signedAt": "ISO 8601",
    "signedBy": "UUID",
    "previousStatus": "InReview",
    "newStatus": "Signed"
  }
}
```

---

#### 30. DiagnosisAdded

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-030 |
| **Event Name** | `DiagnosisAdded` |
| **Trigger Entity** | Diagnosis |
| **Event Type** | Created |
| **Description** | New diagnosis documented |
| **Trigger Action** | POST /encounters/{encounterId}/diagnoses |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "DiagnosisAdded",
  "timestamp": "ISO 8601",
  "payload": {
    "diagnosisId": "UUID",
    "encounterId": "UUID",
    "patientId": "UUID",
    "icd10Code": "string",
    "diagnosisName": "string",
    "diagnosisType": "string",
    "clinicianId": "UUID"
  }
}
```

---

#### 31. VitalSignsRecorded

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-031 |
| **Event Name** | `VitalSignsRecorded` |
| **Trigger Entity** | VitalSigns |
| **Event Type** | Created |
| **Description** | Vital signs captured during encounter |
| **Trigger Action** | POST /encounters/{encounterId}/vitals |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "VitalSignsRecorded",
  "timestamp": "ISO 8601",
  "payload": {
    "vitalSignsId": "UUID",
    "encounterId": "UUID",
    "patientId": "UUID",
    "temperature": "decimal",
    "heartRate": "integer",
    "bloodPressureSystolic": "integer",
    "bloodPressureDiastolic": "integer",
    "oxygenSaturation": "decimal",
    "recordedBy": "UUID"
  }
}
```

---

#### 32. DischargeSummaryGenerated

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-032 |
| **Event Name** | `DischargeSummaryGenerated` |
| **Trigger Entity** | ClinicalDocumentation |
| **Event Type** | Created |
| **Description** | Discharge summary created for inpatient |
| **Trigger Action** | POST /encounters/{encounterId}/discharge-summary |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "DischargeSummaryGenerated",
  "timestamp": "ISO 8601",
  "payload": {
    "documentationId": "UUID",
    "encounterId": "UUID",
    "patientId": "UUID",
    "generatedAt": "ISO 8601",
    "generatedBy": "UUID",
    "dischargeDisposition": "string"
  }
}
```

---

### Laboratory Domain Events

#### 33. LabOrderPlaced

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-033 |
| **Event Name** | `LabOrderPlaced` |
| **Trigger Entity** | LabOrder |
| **Event Type** | Created |
| **Description** | New laboratory test order placed |
| **Trigger Action** | POST /lab/orders |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "LabOrderPlaced",
  "timestamp": "ISO 8601",
  "payload": {
    "labOrderId": "UUID",
    "orderId": "UUID",
    "patientId": "UUID",
    "encounterId": "UUID",
    "labTestCode": "string",
    "labTestName": "string",
    "specimenType": "string",
    "priority": "string",
    "orderingProviderId": "UUID"
  }
}
```

---

#### 34. LabOrderAccepted

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-034 |
| **Event Name** | `LabOrderAccepted` |
| **Trigger Entity** | LabOrder |
| **Event Type** | StatusChanged |
| **Description** | Lab order accepted by laboratory |
| **Trigger Action** | PUT /lab/orders/{orderId}/accept |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "LabOrderAccepted",
  "timestamp": "ISO 8601",
  "payload": {
    "labOrderId": "UUID",
    "patientId": "UUID",
    "acceptedAt": "ISO 8601",
    "acceptedBy": "UUID",
    "previousStatus": "Submitted",
    "newStatus": "Accepted"
  }
}
```

---

#### 35. LabOrderRejected

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-035 |
| **Event Name** | `LabOrderRejected` |
| **Trigger Entity** | LabOrder |
| **Event Type** | StatusChanged |
| **Description** | Lab order rejected by laboratory |
| **Trigger Action** | PUT /lab/orders/{orderId}/reject |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "LabOrderRejected",
  "timestamp": "ISO 8601",
  "payload": {
    "labOrderId": "UUID",
    "patientId": "UUID",
    "rejectedAt": "ISO 8601",
    "rejectedBy": "UUID",
    "rejectionReason": "string",
    "previousStatus": "Submitted",
    "newStatus": "Rejected"
  }
}
```

---

#### 36. SpecimenCollected

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-036 |
| **Event Name** | `SpecimenCollected` |
| **Trigger Entity** | Specimen |
| **Event Type** | Created |
| **Description** | Specimen collected from patient |
| **Trigger Action** | POST /lab/specimens |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "SpecimenCollected",
  "timestamp": "ISO 8601",
  "payload": {
    "specimenId": "UUID",
    "specimenNumber": "string",
    "labOrderId": "UUID",
    "patientId": "UUID",
    "specimenType": "string",
    "collectionMethod": "string",
    "collectedAt": "ISO 8601",
    "collectedBy": "UUID"
  }
}
```

---

#### 37. SpecimenReceived

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-037 |
| **Event Name** | `SpecimenReceived` |
| **Trigger Entity** | Specimen |
| **Event Type** | StatusChanged |
| **Description** | Specimen received at laboratory |
| **Trigger Action** | PUT /lab/specimens/{specimenId}/receive |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "SpecimenReceived",
  "timestamp": "ISO 8601",
  "payload": {
    "specimenId": "UUID",
    "patientId": "UUID",
    "receivedAt": "ISO 8601",
    "receivedBy": "UUID",
    "condition": "string",
    "previousStatus": "Collected",
    "newStatus": "Received"
  }
}
```

---

#### 38. SpecimenProcessed

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-038 |
| **Event Name** | `SpecimenProcessed` |
| **Trigger Entity** | Specimen |
| **Event Type** | StatusChanged |
| **Description** | Specimen processed for testing |
| **Trigger Action** | PUT /lab/specimens/{specimenId}/process |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "SpecimenProcessed",
  "timestamp": "ISO 8601",
  "payload": {
    "specimenId": "UUID",
    "patientId": "UUID",
    "processedAt": "ISO 8601",
    "processedBy": "UUID",
    "processingSteps": ["string"],
    "previousStatus": "Received",
    "newStatus": "Processed"
  }
}
```

---

#### 39. LabResultPreliminary

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-039 |
| **Event Name** | `LabResultPreliminary` |
| **Trigger Entity** | LabResult |
| **Event Type** | Created |
| **Description** | Preliminary lab result available |
| **Trigger Action** | POST /lab/specimens/{specimenId}/results |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "LabResultPreliminary",
  "timestamp": "ISO 8601",
  "payload": {
    "labResultId": "UUID",
    "labOrderId": "UUID",
    "specimenId": "UUID",
    "patientId": "UUID",
    "resultCode": "string",
    "resultName": "string",
    "resultValue": "string",
    "resultUnit": "string",
    "abnormalFlag": "string",
    "performedAt": "ISO 8601",
    "status": "Preliminary"
  }
}
```

---

#### 40. LabResultFinal

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-040 |
| **Event Name** | `LabResultFinal` |
| **Trigger Entity** | LabResult |
| **Event Type** | StatusChanged |
| **Description** | Final lab result available |
| **Trigger Action** | PUT /lab/results/{resultId}/finalize |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "LabResultFinal",
  "timestamp": "ISO 8601",
  "payload": {
    "labResultId": "UUID",
    "labOrderId": "UUID",
    "patientId": "UUID",
    "resultCode": "string",
    "resultValue": "string",
    "abnormalFlag": "string",
    "verifiedAt": "ISO 8601",
    "verifiedBy": "UUID",
    "previousStatus": "Preliminary",
    "newStatus": "Final"
  }
}
```

---

#### 41. CriticalValueReported

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-041 |
| **Event Name** | `CriticalValueReported` |
| **Trigger Entity** | LabResult |
| **Event Type** | StatusChanged |
| **Description** | Critical lab value detected and reported |
| **Trigger Action** | Automatic (abnormal threshold) |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "CriticalValueReported",
  "timestamp": "ISO 8601",
  "payload": {
    "labResultId": "UUID",
    "patientId": "UUID",
    "resultCode": "string",
    "resultValue": "string",
    "criticalLevel": "string",
    "reportedTo": "UUID",
    "reportedAt": "ISO 8601",
    "acknowledgedAt": "ISO 8601"
  }
}
```

---

#### 42. QualityControlPerformed

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-042 |
| **Event Name** | `QualityControlPerformed` |
| **Trigger Entity** | QualityControl |
| **Event Type** | Created |
| **Description** | Quality control test performed |
| **Trigger Action** | POST /lab/quality-control |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "QualityControlPerformed",
  "timestamp": "ISO 8601",
  "payload": {
    "qualityControlId": "UUID",
    "controlType": "string",
    "lotNumber": "string",
    "resultValue": "string",
    "expectedRange": "string",
    "passed": "boolean",
    "performedAt": "ISO 8601",
    "performedBy": "UUID"
  }
}
```

---

### Radiology Domain Events

#### 43. RadiologyOrderPlaced

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-043 |
| **Event Name** | `RadiologyOrderPlaced` |
| **Trigger Entity** | RadiologyOrder |
| **Event Type** | Created |
| **Description** | New imaging order placed |
| **Trigger Action** | POST /radiology/orders |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "RadiologyOrderPlaced",
  "timestamp": "ISO 8601",
  "payload": {
    "radiologyOrderId": "UUID",
    "orderId": "UUID",
    "patientId": "UUID",
    "encounterId": "UUID",
    "modality": "string",
    "bodyPart": "string",
    "clinicalIndication": "string",
    "priority": "string",
    "orderingProviderId": "UUID"
  }
}
```

---

#### 44. RadiologyOrderScheduled

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-044 |
| **Event Name** | `RadiologyOrderScheduled` |
| **Trigger Entity** | RadiologyOrder |
| **Event Type** | StatusChanged |
| **Description** | Imaging study scheduled |
| **Trigger Action** | PUT /radiology/orders/{orderId}/schedule |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "RadiologyOrderScheduled",
  "timestamp": "ISO 8601",
  "payload": {
    "radiologyOrderId": "UUID",
    "patientId": "UUID",
    "scheduledAt": "ISO 8601",
    "scheduledBy": "UUID",
    "modality": "string",
    "room": "string",
    "previousStatus": "Submitted",
    "newStatus": "Scheduled"
  }
}
```

---

#### 45. ImagingStudyStarted

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-045 |
| **Event Name** | `ImagingStudyStarted` |
| **Trigger Entity** | ImagingStudy |
| **Event Type** | Created |
| **Description** | Patient arrived for imaging study |
| **Trigger Action** | POST /radiology/studies/{studyId}/start |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "ImagingStudyStarted",
  "timestamp": "ISO 8601",
  "payload": {
    "studyId": "UUID",
    "radiologyOrderId": "UUID",
    "patientId": "UUID",
    "startedAt": "ISO 8601",
    "startedBy": "UUID",
    "modality": "string"
  }
}
```

---

#### 46. ImageAcquired

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-046 |
| **Event Name** | `ImageAcquired` |
| **Trigger Entity** | Image |
| **Event Type** | Created |
| **Description** | DICOM image acquired |
| **Trigger Action** | Automatic (DICOM receiver) |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "ImageAcquired",
  "timestamp": "ISO 8601",
  "payload": {
    "imageId": "UUID",
    "studyId": "UUID",
    "patientId": "UUID",
    "seriesNumber": "integer",
    "instanceNumber": "integer",
    "acquiredAt": "ISO 8601",
    "modality": "string"
  }
}
```

---

#### 47. ImagingStudyCompleted

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-047 |
| **Event Name** | `ImagingStudyCompleted` |
| **Trigger Entity** | ImagingStudy |
| **Event Type** | StatusChanged |
| **Description** | All images acquired for study |
| **Trigger Action** | POST /radiology/studies/{studyId}/complete |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "ImagingStudyCompleted",
  "timestamp": "ISO 8601",
  "payload": {
    "studyId": "UUID",
    "patientId": "UUID",
    "completedAt": "ISO 8601",
    "imageCount": "integer",
    "previousStatus": "Started",
    "newStatus": "Completed"
  }
}
```

---

#### 48. RadiologyReportSigned

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-048 |
| **Event Name** | `RadiologyReportSigned` |
| **Trigger Entity** | RadiologyReport |
| **Event Type** | StatusChanged |
| **Description** | Radiologist interpretation finalized |
| **Trigger Action** | POST /radiology/reports/{reportId}/sign |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "RadiologyReportSigned",
  "timestamp": "ISO 8601",
  "payload": {
    "reportId": "UUID",
    "studyId": "UUID",
    "patientId": "UUID",
    "radiologistId": "UUID",
    "signedAt": "ISO 8601",
    "criticalFinding": "boolean",
    "previousStatus": "Dictated",
    "newStatus": "Signed"
  }
}
```

---

#### 49. CriticalFindingReported

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-049 |
| **Event Name** | `CriticalFindingReported` |
| **Trigger Entity** | RadiologyReport |
| **Event Type** | StatusChanged |
| **Description** | Critical finding communicated to ordering provider |
| **Trigger Action** | Automatic (critical finding flag) |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "CriticalFindingReported",
  "timestamp": "ISO 8601",
  "payload": {
    "reportId": "UUID",
    "studyId": "UUID",
    "patientId": "UUID",
    "finding": "string",
    "reportedTo": "UUID",
    "reportedAt": "ISO 8601",
    "acknowledgedAt": "ISO 8601"
  }
}
```

---

### Pharmacy Domain Events

#### 50. MedicationOrdered

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-050 |
| **Event Name** | `MedicationOrdered` |
| **Trigger Entity** | MedicationOrder |
| **Event Type** | Created |
| **Description** | New medication ordered for patient |
| **Trigger Action** | POST /pharmacy/orders |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "MedicationOrdered",
  "timestamp": "ISO 8601",
  "payload": {
    "medicationOrderId": "UUID",
    "orderId": "UUID",
    "patientId": "UUID",
    "encounterId": "UUID",
    "medicationId": "UUID",
    "dosage": "string",
    "route": "string",
    "frequency": "string",
    "orderingProviderId": "UUID"
  }
}
```

---

#### 51. MedicationOrderVerified

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-051 |
| **Event Name** | `MedicationOrderVerified` |
| **Trigger Entity** | MedicationOrder |
| **Event Type** | StatusChanged |
| **Description** | Medication order verified by pharmacist |
| **Trigger Action** | POST /pharmacy/orders/{orderId}/verify |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "MedicationOrderVerified",
  "timestamp": "ISO 8601",
  "payload": {
    "medicationOrderId": "UUID",
    "patientId": "UUID",
    "verifiedAt": "ISO 8601",
    "verifiedBy": "UUID",
    "previousStatus": "Submitted",
    "newStatus": "Verified"
  }
}
```

---

#### 52. MedicationDispensed

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-052 |
| **Event Name** | `MedicationDispensed` |
| **Trigger Entity** | DispensingRecord |
| **Event Type** | Created |
| **Description** | Medication dispensed to patient |
| **Trigger Action** | POST /pharmacy/dispensing |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "MedicationDispensed",
  "timestamp": "ISO 8601",
  "payload": {
    "dispensingId": "UUID",
    "dispensingNumber": "string",
    "medicationOrderId": "UUID",
    "patientId": "UUID",
    "medicationId": "UUID",
    "quantityDispensed": "integer",
    "lotNumber": "string",
    "pharmacistId": "UUID",
    "pharmacyId": "UUID"
  }
}
```

---

#### 53. MedicationAdministered

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-053 |
| **Event Name** | `MedicationAdministered` |
| **Trigger Entity** | AdministrationRecord |
| **Event Type** | Created |
| **Description** | Medication administered to patient |
| **Trigger Action** | POST /pharmacy/administration |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "MedicationAdministered",
  "timestamp": "ISO 8601",
  "payload": {
    "administrationId": "UUID",
    "medicationOrderId": "UUID",
    "patientId": "UUID",
    "medicationId": "UUID",
    "dosage": "string",
    "route": "string",
    "administeredBy": "UUID",
    "administeredAt": "ISO 8601",
    "site": "string"
  }
}
```

---

#### 54. MedicationAdministrationMissed

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-054 |
| **Event Name** | `MedicationAdministrationMissed` |
| **Trigger Entity** | AdministrationRecord |
| **Event Type** | StatusChanged |
| **Description** | Scheduled medication dose missed |
| **Trigger Action** | Automatic (schedule miss) |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "MedicationAdministrationMissed",
  "timestamp": "ISO 8601",
  "payload": {
    "administrationId": "UUID",
    "medicationOrderId": "UUID",
    "patientId": "UUID",
    "scheduledTime": "ISO 8601",
    "detectedAt": "ISO 8601",
    "previousStatus": "Scheduled",
    "newStatus": "Missed"
  }
}
```

---

#### 55. DrugInteractionDetected

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-055 |
| **Event Name** | `DrugInteractionDetected` |
| **Trigger Entity** | DrugInteraction |
| **Event Type** | Created |
| **Description** | Drug-drug interaction identified |
| **Trigger Action** | Automatic (CDS check) |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "DrugInteractionDetected",
  "timestamp": "ISO 8601",
  "payload": {
    "interactionId": "UUID",
    "patientId": "UUID",
    "medicationId1": "UUID",
    "medicationId2": "UUID",
    "severity": "string",
    "description": "string",
    "recommendation": "string",
    "detectedAt": "ISO 8601"
  }
}
```

---

### Hospital Domain Events

#### 56. BedStatusChanged

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-056 |
| **Event Name** | `BedStatusChanged` |
| **Trigger Entity** | Bed |
| **Event Type** | StatusChanged |
| **Description** | Hospital bed availability changed |
| **Trigger Action** | PUT /beds/{bedId}/status |
| **Immutability** | Immutable |
| **Retention** | 1 year |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "BedStatusChanged",
  "timestamp": "ISO 8601",
  "payload": {
    "bedId": "UUID",
    "hospitalId": "UUID",
    "departmentId": "UUID",
    "previousStatus": "string",
    "newStatus": "string",
    "patientId": "UUID",
    "changedBy": "UUID"
  }
}
```

---

#### 57. BedAssigned

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-057 |
| **Event Name** | `BedAssigned` |
| **Trigger Entity** | Bed |
| **Event Type** | StatusChanged |
| **Description** | Bed assigned to patient |
| **Trigger Action** | POST /beds/{bedId}/assign |
| **Immutability** | Immutable |
| **Retention** | 1 year |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "BedAssigned",
  "timestamp": "ISO 8601",
  "payload": {
    "bedId": "UUID",
    "patientId": "UUID",
    "encounterId": "UUID",
    "assignedAt": "ISO 8601",
    "assignedBy": "UUID",
    "previousStatus": "Available",
    "newStatus": "Occupied"
  }
}
```

---

### Scheduling Domain Events

#### 58. AppointmentScheduled

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-058 |
| **Event Name** | `AppointmentScheduled` |
| **Trigger Entity** | Appointment |
| **Event Type** | Created |
| **Description** | New appointment booked |
| **Trigger Action** | POST /scheduling/appointments |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "AppointmentScheduled",
  "timestamp": "ISO 8601",
  "payload": {
    "appointmentId": "UUID",
    "appointmentNumber": "string",
    "patientId": "UUID",
    "providerId": "UUID",
    "appointmentType": "string",
    "scheduledDate": "ISO 8601",
    "scheduledTime": "string",
    "duration": "integer",
    "departmentId": "UUID"
  }
}
```

---

#### 59. AppointmentConfirmed

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-059 |
| **Event Name** | `AppointmentConfirmed` |
| **Trigger Entity** | Appointment |
| **Event Type** | StatusChanged |
| **Description** | Appointment confirmed by patient or staff |
| **Trigger Action** | POST /scheduling/appointments/{appointmentId}/confirm |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "AppointmentConfirmed",
  "timestamp": "ISO 8601",
  "payload": {
    "appointmentId": "UUID",
    "patientId": "UUID",
    "confirmedAt": "ISO 8601",
    "confirmedBy": "UUID",
    "previousStatus": "Scheduled",
    "newStatus": "Confirmed"
  }
}
```

---

#### 60. AppointmentCancelled

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-060 |
| **Event Name** | `AppointmentCancelled` |
| **Trigger Entity** | Appointment |
| **Event Type** | StatusChanged |
| **Description** | Appointment cancelled |
| **Trigger Action** | POST /scheduling/appointments/{appointmentId}/cancel |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "AppointmentCancelled",
  "timestamp": "ISO 8601",
  "payload": {
    "appointmentId": "UUID",
    "patientId": "UUID",
    "cancelledAt": "ISO 8601",
    "cancelledBy": "UUID",
    "reason": "string",
    "previousStatus": "string",
    "newStatus": "Cancelled"
  }
}
```

---

### Finance Domain Events

#### 61. ChargeCreated

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-061 |
| **Event Name** | `ChargeCreated` |
| **Trigger Entity** | FinancialTransaction |
| **Event Type** | Created |
| **Description** | New charge posted |
| **Trigger Action** | POST /finance/charges |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "ChargeCreated",
  "timestamp": "ISO 8601",
  "payload": {
    "transactionId": "UUID",
    "transactionNumber": "string",
    "patientId": "UUID",
    "encounterId": "UUID",
    "amount": "decimal",
    "currency": "string",
    "description": "string",
    "createdBy": "UUID"
  }
}
```

---

#### 62. ClaimSubmitted

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-062 |
| **Event Name** | `ClaimSubmitted` |
| **Trigger Entity** | Claim |
| **Event Type** | StatusChanged |
| **Description** | Insurance claim submitted to payer |
| **Trigger Action** | POST /finance/claims |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "ClaimSubmitted",
  "timestamp": "ISO 8601",
  "payload": {
    "claimId": "UUID",
    "claimNumber": "string",
    "patientId": "UUID",
    "encounterId": "UUID",
    "insurancePlanId": "UUID",
    "totalAmount": "decimal",
    "submittedAt": "ISO 8601",
    "submittedBy": "UUID",
    "previousStatus": "Draft",
    "newStatus": "Submitted"
  }
}
```

---

#### 63. ClaimAccepted

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-063 |
| **Event Name** | `ClaimAccepted` |
| **Trigger Entity** | Claim |
| **Event Type** | StatusChanged |
| **Description** | Claim accepted by payer |
| **Trigger Action** | Automatic (remittance received) |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "ClaimAccepted",
  "timestamp": "ISO 8601",
  "payload": {
    "claimId": "UUID",
    "patientId": "UUID",
    "paidAmount": "decimal",
    "acceptedAt": "ISO 8601",
    "previousStatus": "Submitted",
    "newStatus": "Accepted"
  }
}
```

---

#### 64. ClaimDenied

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-064 |
| **Event Name** | `ClaimDenied` |
| **Trigger Entity** | Claim |
| **Event Type** | StatusChanged |
| **Description** | Claim denied by payer |
| **Trigger Action** | Automatic (denial received) |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "ClaimDenied",
  "timestamp": "ISO 8601",
  "payload": {
    "claimId": "UUID",
    "patientId": "UUID",
    "denialReason": "string",
    "deniedAt": "ISO 8601",
    "previousStatus": "Submitted",
    "newStatus": "Denied"
  }
}
```

---

#### 65. PaymentReceived

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-065 |
| **Event Name** | `PaymentReceived` |
| **Trigger Entity** | Payment |
| **Event Type** | Created |
| **Description** | Payment received from patient or insurer |
| **Trigger Action** | POST /finance/payments |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "PaymentReceived",
  "timestamp": "ISO 8601",
  "payload": {
    "paymentId": "UUID",
    "paymentNumber": "string",
    "patientId": "UUID",
    "paymentType": "string",
    "paymentMethod": "string",
    "amount": "decimal",
    "currency": "string",
    "receivedAt": "ISO 8601",
    "receivedBy": "UUID"
  }
}
```

---

### Quality & Safety Domain Events

#### 66. SafetyEventReported

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-066 |
| **Event Name** | `SafetyEventReported` |
| **Trigger Entity** | SafetyEvent |
| **Event Type** | Created |
| **Description** | Patient safety event reported |
| **Trigger Action** | POST /quality/safety-events |
| **Immutability** | Immutable |
| **Retention** | 10 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "SafetyEventReported",
  "timestamp": "ISO 8601",
  "payload": {
    "safetyEventId": "UUID",
    "patientId": "UUID",
    "encounterId": "UUID",
    "eventType": "string",
    "severity": "string",
    "description": "string",
    "reportedBy": "UUID",
    "reportedAt": "ISO 8601"
  }
}
```

---

#### 67. IncidentReportCreated

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-067 |
| **Event Name** | `IncidentReportCreated` |
| **Trigger Entity** | IncidentReport |
| **Event Type** | Created |
| **Description** | Incident report filed |
| **Trigger Action** | POST /quality/incidents |
| **Immutability** | Immutable |
| **Retention** | 10 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "IncidentReportCreated",
  "timestamp": "ISO 8601",
  "payload": {
    "incidentId": "UUID",
    "incidentNumber": "string",
    "incidentType": "string",
    "severity": "string",
    "description": "string",
    "reportedBy": "UUID",
    "reportedAt": "ISO 8601"
  }
}
```

---

### Notification Domain Events

#### 68. NotificationCreated

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-068 |
| **Event Name** | `NotificationCreated` |
| **Trigger Entity** | Notification |
| **Event Type** | Created |
| **Description** | New notification created |
| **Trigger Action** | POST /notifications |
| **Immutability** | Immutable |
| **Retention** | 1 year |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "NotificationCreated",
  "timestamp": "ISO 8601",
  "payload": {
    "notificationId": "UUID",
    "userId": "UUID",
    "notificationType": "string",
    "channel": "string",
    "subject": "string",
    "priority": "string"
  }
}
```

---

#### 69. NotificationDelivered

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-069 |
| **Event Name** | `NotificationDelivered` |
| **Trigger Entity** | Notification |
| **Event Type** | StatusChanged |
| **Description** | Notification delivered to recipient |
| **Trigger Action** | Automatic (delivery confirmation) |
| **Immutability** | Immutable |
| **Retention** | 1 year |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "NotificationDelivered",
  "timestamp": "ISO 8601",
  "payload": {
    "notificationId": "UUID",
    "userId": "UUID",
    "deliveredAt": "ISO 8601",
    "channel": "string",
    "previousStatus": "Sent",
    "newStatus": "Delivered"
  }
}
```

---

### Document Domain Events

#### 70. DocumentCreated

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-070 |
| **Event Name** | `DocumentCreated` |
| **Trigger Entity** | Document |
| **Event Type** | Created |
| **Description** | New document created |
| **Trigger Action** | POST /documents |
| **Immutability** | Immutable |
| **Retention** | 7 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "DocumentCreated",
  "timestamp": "ISO 8601",
  "payload": {
    "documentId": "UUID",
    "documentNumber": "string",
    "title": "string",
    "documentType": "string",
    "patientId": "UUID",
    "ownerId": "UUID",
    "createdBy": "UUID"
  }
}
```

---

### Workflow Domain Events

#### 71. WorkflowCreated

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-071 |
| **Event Name** | `WorkflowCreated` |
| **Trigger Entity** | Workflow |
| **Event Type** | Created |
| **Description** | New workflow started |
| **Trigger Action** | POST /workflow/workflows |
| **Immutability** | Immutable |
| **Retention** | 3 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "WorkflowCreated",
  "timestamp": "ISO 8601",
  "payload": {
    "workflowId": "UUID",
    "workflowName": "string",
    "workflowType": "string",
    "patientId": "UUID",
    "encounterId": "UUID",
    "initiatedBy": "UUID"
  }
}
```

---

#### 72. TaskCreated

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-072 |
| **Event Name** | `TaskCreated` |
| **Trigger Entity** | Task |
| **Event Type** | Created |
| **Description** | New task created |
| **Trigger Action** | POST /workflow/tasks |
| **Immutability** | Immutable |
| **Retention** | 3 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "TaskCreated",
  "timestamp": "ISO 8601",
  "payload": {
    "taskId": "UUID",
    "taskName": "string",
    "workflowId": "UUID",
    "assignedTo": "UUID",
    "dueDate": "ISO 8601",
    "priority": "string"
  }
}
```

---

#### 73. TaskAssigned

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-073 |
| **Event Name** | `TaskAssigned` |
| **Trigger Entity** | Task |
| **Event Type** | StatusChanged |
| **Description** | Task assigned to user |
| **Trigger Action** | PUT /workflow/tasks/{taskId}/assign |
| **Immutability** | Immutable |
| **Retention** | 3 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "TaskAssigned",
  "timestamp": "ISO 8601",
  "payload": {
    "taskId": "UUID",
    "assignedTo": "UUID",
    "assignedAt": "ISO 8601",
    "assignedBy": "UUID",
    "previousStatus": "Created",
    "newStatus": "Assigned"
  }
}
```

---

#### 74. TaskCompleted

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-074 |
| **Event Name** | `TaskCompleted` |
| **Trigger Entity** | Task |
| **Event Type** | StatusChanged |
| **Description** | Task finished |
| **Trigger Action** | POST /workflow/tasks/{taskId}/complete |
| **Immutability** | Immutable |
| **Retention** | 3 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "TaskCompleted",
  "timestamp": "ISO 8601",
  "payload": {
    "taskId": "UUID",
    "completedAt": "ISO 8601",
    "completedBy": "UUID",
    "result": "string",
    "previousStatus": "InProgress",
    "newStatus": "Completed"
  }
}
```

---

#### 75. TaskOverdue

| Attribute | Value |
|-----------|-------|
| **Event ID** | EVT-075 |
| **Event Name** | `TaskOverdue` |
| **Trigger Entity** | Task |
| **Event Type** | StatusChanged |
| **Description** | Task past due date |
| **Trigger Action** | Automatic (schedule check) |
| **Immutability** | Immutable |
| **Retention** | 3 years |

**Payload Schema:**

```json
{
  "eventId": "UUID",
  "eventType": "TaskOverdue",
  "timestamp": "ISO 8601",
  "payload": {
    "taskId": "UUID",
    "dueDate": "ISO 8601",
    "detectedAt": "ISO 8601",
    "assignedTo": "UUID",
    "overdueDuration": "integer"
  }
}
```

---

### Remaining Events (76-130)

| Event ID | Event Name | Entity | Type | Description |
|----------|------------|--------|------|-------------|
| EVT-076 | HandoffInitiated | Handoff | Created | Care handoff started |
| EVT-077 | EscalationTriggered | Escalation | Created | Escalation activated |
| EVT-078 | PolicyCreated | Policy | Created | New policy created |
| EVT-079 | PolicyUpdated | Policy | Updated | Policy modified |
| EVT-080 | GuidelinePublished | Guideline | Created | New guideline published |
| EVT-081 | CDSDeployed | CDSDeployment | Created | CDS rule deployed |
| EVT-082 | CDSTriggered | CDSTrigger | Created | CDS triggered for patient |
| EVT-083 | KnowledgeArticlePublished | KnowledgeArticle | Created | New article published |
| EVT-084 | ModelRegistered | AIModel | Created | New AI model registered |
| EVT-085 | ModelDeployed | AIModel | StatusChanged | Model deployed to production |
| EVT-086 | ModelDriftDetected | AIModel | StatusChanged | Performance drift detected |
| EVT-087 | PredictionMade | PredictionLog | Created | AI prediction logged |
| EVT-088 | DeviceRegistered | MedicalDevice | Created | New device registered |
| EVT-089 | DeviceAlertGenerated | DeviceAlert | Created | Device alert triggered |
| EVT-090 | MaintenanceScheduled | DeviceMaintenance | Created | Maintenance scheduled |
| EVT-091 | CalibrationCompleted | DeviceCalibration | StatusChanged | Calibration finished |
| EVT-092 | InventoryItemCreated | InventoryItem | Created | New item added |
| EVT-093 | StockReceived | StockMovement | Created | Stock received from supplier |
| EVT-094 | StockDispensed | StockMovement | Created | Stock dispensed to department |
| EVT-095 | ReorderAlertTriggered | ReorderAlert | Created | Low stock alert |
| EVT-096 | PurchaseOrderCreated | PurchaseOrder | Created | PO created |
| EVT-097 | PurchaseOrderApproved | PurchaseOrder | StatusChanged | PO approved |
| EVT-098 | ShipmentReceived | Shipment | StatusChanged | Shipment received |
| EVT-099 | SupplierRegistered | Supplier | Created | New supplier added |
| EVT-100 | ReportGenerated | Report | StatusChanged | Report generated |
| EVT-101 | DashboardCreated | Dashboard | Created | New dashboard created |
| EVT-102 | KPIUpdated | KPI | Updated | KPI value updated |
| EVT-103 | DatasetCreated | AnalyticsDataset | Created | New dataset |
| EVT-104 | PipelineCompleted | DataPipeline | StatusChanged | ETL pipeline finished |
| EVT-105 | CohortDefined | CohortDefinition | Created | Patient cohort created |
| EVT-106 | TelehealthVisitScheduled | TelehealthVisit | Created | Virtual visit booked |
| EVT-107 | TelehealthVisitConnected | TelehealthVisit | StatusChanged | Patient connected |
| EVT-108 | RPMReadingReceived | MonitoringReading | Created | RPM data received |
| EVT-109 | DigitalTherapeuticStarted | DigitalTherapeutic | Created | Treatment initiated |
| EVT-110 | PatientPortalActivated | PatientPortal | StatusChanged | Portal account created |
| EVT-111 | CarePlanCreated | CarePlan | Created | Care plan established |
| EVT-112 | CarePlanGoalMet | CarePlanGoal | StatusChanged | Goal achieved |
| EVT-113 | PROSubmitted | PatientReportedOutcome | Created | PRO survey completed |
| EVT-114 | PatientFeedbackSubmitted | PatientFeedback | Created | Feedback received |
| EVT-115 | IntegrationEndpointCreated | IntegrationEndpoint | Created | New endpoint |
| EVT-116 | InterfaceDeployed | Interface | StatusChanged | Interface activated |
| EVT-117 | MessageProcessed | Message | StatusChanged | Message processed |
| EVT-118 | PartnerOnboarded | Partner | Created | New partner added |
| EVT-119 | ConfigurationUpdated | SystemConfiguration | Updated | Setting changed |
| EVT-120 | FeatureFlagToggled | FeatureFlag | Updated | Feature toggled |
| EVT-121 | AuditLogCreated | AuditLog | Created | Audit entry logged |
| EVT-122 | DiseaseReported | DiseaseReport | Created | Notifiable disease reported |
| EVT-123 | OutbreakDetected | OutbreakEvent | Created | Outbreak identified |
| EVT-124 | VaccinationRecorded | Vaccination | Created | Vaccination documented |
| EVT-125 | ClinicalTrialRegistered | ClinicalTrial | Created | Trial initiated |
| EVT-126 | PatientEnrolled | Enrollment | Created | Patient enrolled in trial |
| EVT-127 | InformedConsentObtained | InformedConsent | Created | Consent signed |
| EVT-128 | AdverseEventReported | AdverseEvent | Created | AE reported |
| EVT-129 | QualityMetricCalculated | QualityMetric | Created | Metric computed |
| EVT-130 | CorrectiveActionAssigned | CorrectiveAction | Created | Action assigned |

---

## Event Payload Specifications

### Standard Payload Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| eventId | UUID | Yes | Unique event identifier |
| eventType | String | Yes | Event name (PascalCase) |
| eventVersion | String | Yes | Schema version (SemVer) |
| timestamp | ISO 8601 | Yes | Event occurrence time |
| source | String | Yes | Originating service |
| correlationId | UUID | Yes | Request correlation |
| causationId | UUID | No | Triggering event ID |
| tenantId | UUID | Yes | Tenant identifier |
| aggregateId | UUID | Yes | Root entity ID |
| payload | Object | Yes | Event-specific data |
| metadata | Object | No | Additional context |

### Payload Data Types

| Type | Description | Example |
|------|-------------|---------|
| UUID | Unique identifier | `550e8400-e29b-41d4-a716-446655440000` |
| String | Text data | `John Doe` |
| Integer | Whole numbers | `42` |
| Decimal | Precise numbers | `123.45` |
| Boolean | True/false | `true` |
| DateTime | ISO 8601 datetime | `2026-06-25T14:30:00Z` |
| Date | ISO 8601 date | `2026-06-25` |
| Enum | Predefined values | `ACTIVE` |
| Object | Nested object | `{ "key": "value" }` |
| Array | List of values | `["item1", "item2"]` |

### Payload Validation Rules

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      PAYLOAD VALIDATION RULES                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  1. Required Fields                                                            │
│     • All standard fields must be present                                      │
│     • Payload fields per event schema                                           │
│     • No null values in required fields                                        │
│                                                                                 │
│  2. Data Types                                                                 │
│     • Strict type checking                                                     │
│     • No type coercion                                                         │
│     • Validate format (email, phone, etc.)                                     │
│                                                                                 │
│  3. Length Limits                                                               │
│     • Strings: max 10,000 characters                                           │
│     • Arrays: max 1,000 elements                                               │
│     • Objects: max 100 nested levels                                           │
│                                                                                 │
│  4. Business Rules                                                             │
│     • Entity-specific validations                                              │
│     • Referential integrity checks                                             │
│     • State transition validation                                              │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Event Versioning Strategy

### Versioning Scheme

| Component | Description | Example |
|-----------|-------------|---------|
| **Major** | Breaking changes | `2.0.0` |
| **Minor** | New optional fields | `1.1.0` |
| **Patch** | Bug fixes, documentation | `1.0.1` |

### Version Change Rules

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       VERSION CHANGE RULES                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  MAJOR VERSION CHANGE (Breaking)                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  • Remove required field                                               │   │
│  │  • Rename field                                                        │   │
│  │  • Change field type                                                   │   │
│  │  • Change enum values                                                  │   │
│  │  • Change business rules                                               │   │
│  │                                                                        │   │
│  │  Migration: Create new event type, deprecate old                       │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  MINOR VERSION CHANGE (Additive)                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  • Add optional field                                                  │   │
│  │  • Add new enum value                                                  │   │
│  │  • Add new event type                                                  │   │
│  │                                                                        │   │
│  │  Migration: Backward compatible, no action required                    │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  PATCH VERSION CHANGE (Fix)                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  • Fix documentation                                                   │   │
│  │  • Fix example                                                         │   │
│  │  • Fix validation rule                                                 │   │
│  │                                                                        │   │
│  │  Migration: No action required                                         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Version Compatibility Matrix

| Consumer Version | Producer 1.0 | Producer 1.1 | Producer 2.0 |
|------------------|--------------|--------------|--------------|
| **1.0** | Compatible | Compatible | Incompatible |
| **1.1** | Compatible | Compatible | Incompatible |
| **2.0** | Compatible | Compatible | Compatible |

---

## Event Immutability Rules

### Immutability Principles

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      IMMUTABILITY PRINCIPLES                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  1. Write Once                                                                 │
│     • Events cannot be modified after creation                                 │
│     • No update operations allowed                                             │
│     • No delete operations allowed                                             │
│                                                                                 │
│  2. Append Only                                                                │
│     • Events are only added to the log                                         │
│     • No removal of events                                                     │
│     • Sequential ordering maintained                                           │
│                                                                                 │
│  3. Timestamp Immutability                                                     │
│     • Event timestamp is fixed at creation                                     │
│     • Cannot be backdated or modified                                          │
│     • UTC timezone enforced                                                    │
│                                                                                 │
│  4. Reference Immutability                                                     │
│     • Event IDs are permanent                                                  │
│     • Aggregate IDs cannot change                                              │
│     • Correlation IDs are fixed                                                │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Immutability Violations

| Violation | Detection | Response |
|-----------|-----------|----------|
| **Modified Event** | Hash mismatch | Reject, alert |
| **Deleted Event** | Gap in sequence | Investigate, restore |
| **Backdated Event** | Timestamp anomaly | Reject, alert |
| **Duplicate Event** | Duplicate ID | Reject, log |

### Storage Immutability

| Layer | Implementation | Guarantee |
|-------|----------------|-----------|
| **Database** | Append-only table | No UPDATE/DELETE |
| **Message Queue** | Retention policy | Time-based expiry |
| **Archive** | WORM storage | Write Once Read Many |
| **Backup** | Immutable backups | No modification |

---

## Event Processing Patterns

### 1. Event Sourcing

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         EVENT SOURCING PATTERN                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Command ──► Aggregate ──► Event Store ──► Event Bus ──► Projections           │
│                                                                                 │
│  Event Store:                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  eventId | aggregateId | eventType | payload | timestamp | version     │   │
│  │  ─────────┼────────────┼───────────┼─────────┼───────────┼────────     │   │
│  │  evt-001  | pat-123    | Created   | {...}   | 2026-06-25 | 1          │   │
│  │  evt-002  | pat-123    | Updated   | {...}   | 2026-06-25 | 2          │   │
│  │  evt-003  | pat-123    | Updated   | {...}   | 2026-06-25 | 3          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  State Reconstruction:                                                         │
│  State = Event1 + Event2 + Event3 + ... + EventN                              │
│                                                                                 │
│  Benefits:                                                                     │
│  • Complete audit trail                                                        │
│  • Temporal queries                                                            │
│  • Event replay                                                                │
│  • Debugging                                                                   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2. CQRS (Command Query Responsibility Segregation)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           CQRS PATTERN                                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Commands (Write Side)            Queries (Read Side)                          │
│  ┌────────────────────┐          ┌────────────────────┐                       │
│  │   Command Handler  │          │   Query Handler    │                       │
│  │   • Validate       │          │   • Read from      │                       │
│  │   • Execute        │          │     Read Model     │                       │
│  │   • Emit Events    │          │   • Return DTO     │                       │
│  └─────────┬──────────┘          └──────────▲─────────┘                       │
│            │                                │                                  │
│            ▼                                │                                  │
│  ┌────────────────────┐          ┌────────────────────┐                       │
│  │   Event Store      │──────────│   Read Model       │                       │
│  │   (Write DB)       │          │   (Read DB)        │                       │
│  └────────────────────┘          └────────────────────┘                       │
│                                                                                 │
│  Write Model: Normalized, transactional                                        │
│  Read Model: Denormalized, optimized for queries                               │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 3. Saga Pattern (Long-Running Processes)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           SAGA PATTERN                                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Order Saga:                                                                   │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐            │
│  │  Step 1   │───►│  Step 2   │───►│  Step 3   │───►│  Step 4   │            │
│  │  Create   │    │  Reserve  │    │  Payment  │    │  Fulfill  │            │
│  │  Order    │    │  Stock    │    │  Process  │    │  Order    │            │
│  └───────────┘    └───────────┘    └───────────┘    └───────────┘            │
│       │                │                │                │                     │
│       ▼                ▼                ▼                ▼                     │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐            │
│  │  Event:   │    │  Event:   │    │  Event:   │    │  Event:   │            │
│  │  Order    │    │  Stock    │    │  Payment  │    │  Order    │            │
│  │  Created  │    │  Reserved │    │  Received │    │ Completed │            │
│  └───────────┘    └───────────┘    └───────────┘    └───────────┘            │
│                                                                                 │
│  Compensation (on failure):                                                    │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐                              │
│  │  Step 3   │───►│  Step 2   │───►│  Step 1   │                              │
│  │  Refund   │    │  Release  │    │  Cancel   │                              │
│  │  Payment  │    │  Stock    │    │  Order    │                              │
│  └───────────┘    └───────────┘    └───────────┘                              │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 4. Event-Driven Microservices

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                   EVENT-DRIVEN MICROSERVICES                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Service A ──► Event Bus ◄── Service B                                         │
│       │              │              │                                           │
│       │              │              │                                           │
│       ▼              │              ▼                                           │
│  ┌───────────┐       │       ┌───────────┐                                    │
│  │  Service A│       │       │  Service B│                                    │
│  │  Database │       │       │  Database │                                    │
│  └───────────┘       │       └───────────┘                                    │
│                      │                                                          │
│                      ▼                                                          │
│               ┌───────────┐                                                    │
│               │  Service C│                                                    │
│               │  Database │                                                    │
│               └───────────┘                                                    │
│                                                                                 │
│  Benefits:                                                                     │
│  • Loose coupling                                                              │
│  • Independent deployment                                                      │
│  • Scalability                                                                 │
│  • Fault isolation                                                             │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Appendix: Event Summary Table

| Event ID | Event Name | Entity | Type | Retention |
|----------|------------|--------|------|-----------|
| EVT-001 | UserRegistered | User | Created | 7 years |
| EVT-002 | UserActivated | User | StatusChanged | 7 years |
| EVT-003 | UserDeactivated | User | StatusChanged | 7 years |
| EVT-004 | PasswordChanged | User | Updated | 7 years |
| EVT-005 | MFATokenGenerated | MFAConfiguration | Created | 1 year |
| EVT-006 | SessionCreated | Session | Created | 1 year |
| EVT-007 | SessionExpired | Session | StatusChanged | 1 year |
| EVT-008 | RoleAssigned | UserRoleAssignment | Created | 7 years |
| EVT-009 | RoleRevoked | UserRoleAssignment | Deleted | 7 years |
| EVT-010 | LoginFailed | User | SecurityEvent | 1 year |
| EVT-011 | PatientRegistered | Patient | Created | 7 years |
| EVT-012 | PatientDemographicsUpdated | Patient | Updated | 7 years |
| EVT-013 | PatientMerged | Patient | StatusChanged | 7 years |
| EVT-014 | AllergyRecorded | Allergy | Created | 7 years |
| EVT-015 | AllergyUpdated | Allergy | Updated | 7 years |
| EVT-016 | MedicationRecorded | Medication | Created | 7 years |
| EVT-017 | MedicationDiscontinued | Medication | StatusChanged | 7 years |
| EVT-018 | ImmunizationRecorded | Immunization | Created | 7 years |
| EVT-019 | PatientConsentGranted | Consent | Created | 7 years |
| EVT-020 | PatientConsentRevoked | Consent | StatusChanged | 7 years |
| EVT-021 | PatientDeceased | Patient | StatusChanged | 7 years |
| EVT-022 | EncounterScheduled | Encounter | Created | 7 years |
| EVT-023 | EncounterCheckedIn | Encounter | StatusChanged | 7 years |
| EVT-024 | EncounterInProgress | Encounter | StatusChanged | 7 years |
| EVT-025 | EncounterCompleted | Encounter | StatusChanged | 7 years |
| EVT-026 | EncounterCancelled | Encounter | StatusChanged | 7 years |
| EVT-027 | EncounterNoShow | Encounter | StatusChanged | 7 years |
| EVT-028 | ClinicalDocumentationCreated | ClinicalDocumentation | Created | 7 years |
| EVT-029 | ClinicalDocumentationSigned | ClinicalDocumentation | StatusChanged | 7 years |
| EVT-030 | DiagnosisAdded | Diagnosis | Created | 7 years |
| EVT-031 | VitalSignsRecorded | VitalSigns | Created | 7 years |
| EVT-032 | DischargeSummaryGenerated | ClinicalDocumentation | Created | 7 years |
| EVT-033 | LabOrderPlaced | LabOrder | Created | 7 years |
| EVT-034 | LabOrderAccepted | LabOrder | StatusChanged | 7 years |
| EVT-035 | LabOrderRejected | LabOrder | StatusChanged | 7 years |
| EVT-036 | SpecimenCollected | Specimen | Created | 7 years |
| EVT-037 | SpecimenReceived | Specimen | StatusChanged | 7 years |
| EVT-038 | SpecimenProcessed | Specimen | StatusChanged | 7 years |
| EVT-039 | LabResultPreliminary | LabResult | Created | 7 years |
| EVT-040 | LabResultFinal | LabResult | StatusChanged | 7 years |
| EVT-041 | CriticalValueReported | LabResult | StatusChanged | 7 years |
| EVT-042 | QualityControlPerformed | QualityControl | Created | 7 years |
| EVT-043 | RadiologyOrderPlaced | RadiologyOrder | Created | 7 years |
| EVT-044 | RadiologyOrderScheduled | RadiologyOrder | StatusChanged | 7 years |
| EVT-045 | ImagingStudyStarted | ImagingStudy | Created | 7 years |
| EVT-046 | ImageAcquired | Image | Created | 7 years |
| EVT-047 | ImagingStudyCompleted | ImagingStudy | StatusChanged | 7 years |
| EVT-048 | RadiologyReportSigned | RadiologyReport | StatusChanged | 7 years |
| EVT-049 | CriticalFindingReported | RadiologyReport | StatusChanged | 7 years |
| EVT-050 | MedicationOrdered | MedicationOrder | Created | 7 years |
| EVT-051 | MedicationOrderVerified | MedicationOrder | StatusChanged | 7 years |
| EVT-052 | MedicationDispensed | DispensingRecord | Created | 7 years |
| EVT-053 | MedicationAdministered | AdministrationRecord | Created | 7 years |
| EVT-054 | MedicationAdministrationMissed | AdministrationRecord | StatusChanged | 7 years |
| EVT-055 | DrugInteractionDetected | DrugInteraction | Created | 7 years |
| EVT-056 | BedStatusChanged | Bed | StatusChanged | 1 year |
| EVT-057 | BedAssigned | Bed | StatusChanged | 1 year |
| EVT-058 | AppointmentScheduled | Appointment | Created | 7 years |
| EVT-059 | AppointmentConfirmed | Appointment | StatusChanged | 7 years |
| EVT-060 | AppointmentCancelled | Appointment | StatusChanged | 7 years |
| EVT-061 | ChargeCreated | FinancialTransaction | Created | 7 years |
| EVT-062 | ClaimSubmitted | Claim | StatusChanged | 7 years |
| EVT-063 | ClaimAccepted | Claim | StatusChanged | 7 years |
| EVT-064 | ClaimDenied | Claim | StatusChanged | 7 years |
| EVT-065 | PaymentReceived | Payment | Created | 7 years |
| EVT-066 | SafetyEventReported | SafetyEvent | Created | 10 years |
| EVT-067 | IncidentReportCreated | IncidentReport | Created | 10 years |
| EVT-068 | NotificationCreated | Notification | Created | 1 year |
| EVT-069 | NotificationDelivered | Notification | StatusChanged | 1 year |
| EVT-070 | DocumentCreated | Document | Created | 7 years |
| EVT-071 | WorkflowCreated | Workflow | Created | 3 years |
| EVT-072 | TaskCreated | Task | Created | 3 years |
| EVT-073 | TaskAssigned | Task | StatusChanged | 3 years |
| EVT-074 | TaskCompleted | Task | StatusChanged | 3 years |
| EVT-075 | TaskOverdue | Task | StatusChanged | 3 years |

---

**Document Classification:** CANONICAL CATALOG  
**Review Cycle:** Quarterly  
**Next Review Date:** 2026-09-25  
**Approved By:** NHDOS Architecture Board