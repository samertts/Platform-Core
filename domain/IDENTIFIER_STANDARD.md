# National Healthcare Digital Operating System (NHDOS) - Identifier Standards

**Version:** 1.0.0  
**Status:** CANONICAL MODEL  
**Last Updated:** 2026-06-25  
**Classification:** Production-Ready Documentation

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Identifier Design Principles](#identifier-design-principles)
3. [UUID Standards](#uuid-standards)
4. [Human-Readable ID Standards](#human-readable-id-standards)
5. [Entity Identifier Specifications](#entity-identifier-specifications)
6. [Validation Rules](#validation-rules)
7. [Collision Handling](#collision-handling)
8. [Migration & Compatibility](#migration--compatibility)

---

## Executive Summary

This document serves as the **CANONICAL IDENTIFIER STANDARD** for the National Healthcare Digital Operating System (NHDOS). It defines identifier formats, validation rules, and collision handling strategies for all entities within the platform.

### Identifier Categories

| Category | Format | Example | Use Case |
|----------|--------|---------|----------|
| **Primary Key** | UUID v4 | `550e8400-e29b-41d4-a716-446655440000` | System-wide unique identification |
| **Human-Readable ID** | PREFIX-YYYY-NNNNNN | `PAT-2026-000001` | User-facing display |
| **Business Key** | Domain-specific | `MRN-12345678` | External system integration |
| **External ID** | Standard format | `NPI-1234567890` | Regulatory compliance |

---

## Identifier Design Principles

### 1. Uniqueness

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         UNIQUENESS REQUIREMENTS                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Global Uniqueness:                                                            │
│  - UUIDs are globally unique across all domains                                │
│  - No two entities share the same UUID                                          │
│  - UUIDs are immutable (never change)                                           │
│                                                                                 │
│  Contextual Uniqueness:                                                        │
│  - Human-readable IDs unique within their entity type                          │
│  - Business keys unique within their domain                                    │
│  - External IDs unique within their standard                                   │
│                                                                                 │
│  Tenant Isolation:                                                             │
│  - IDs scoped to tenant in multi-tenant deployments                            │
│  - Cross-tenant ID conflicts prevented                                         │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2. Immutability

| Rule | Description | Example |
|------|-------------|---------|
| **UUID Never Changes** | Primary key UUID is permanent | `patientId` never updated |
| **Business Key Stable** | MRN assigned once, never reused | `MRN-2026-000001` |
| **Historical Reference** | Deleted entities retain ID | Audit trail references |
| **Merge Handling** | Merged IDs reference surviving | `mergedFrom` field |

### 3. Security

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          SECURITY CONSIDERATIONS                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Non-Sequential IDs:                                                           │
│  - UUIDs are random, not sequential                                            │
│  - Prevents enumeration attacks                                                │
│  - No predictable patterns                                                     │
│                                                                                 │
│  Masked Display:                                                               │
│  - Human-readable IDs partially masked in UI                                   │
│  - Full IDs only for authorized users                                          │
│  - Audit logging for ID access                                                 │
│                                                                                 │
│  No Sensitive Data in IDs:                                                     │
│  - No SSN, MRN in URL parameters                                               │
│  - Use UUIDs in API endpoints                                                  │
│  - Business keys only in specific contexts                                     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 4. Performance

| Consideration | Strategy | Implementation |
|---------------|----------|----------------|
| **Indexing** | UUID indexed efficiently | UUID v4 with index |
| **Storage** | 16 bytes for UUID | Binary storage preferred |
| **Display** | Human-readable for UX | Formatted display layer |
| **API** | UUID in API contracts | REST/GraphQL use UUIDs |
| **Database** | Primary key optimization | Clustered index on UUID |

---

## UUID Standards

### UUID v4 Format

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          UUID v4 STRUCTURE                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Format: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx                                  │
│                                                                                 │
│  ┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐    │
│  │   Time Low      │  Time Mid       │ Time Hi/Version │ Clock Seq/Node │    │
│  │   (8 chars)     │  (4 chars)      │ (4 chars)       │ (12 chars)     │    │
│  ├─────────────────┼─────────────────┼─────────────────┼─────────────────┤    │
│  │  550e8400       │  e29b           │  41d4           │  a71644665544  │    │
│  └─────────────────┴─────────────────┴─────────────────┴─────────────────┘    │
│                                                                                 │
│  Version: 4 (Random)                                                           │
│  Variant: 10xx (RFC 4122)                                                      │
│                                                                                 │
│  Example: 550e8400-e29b-41d4-a716-446655440000                                │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### UUID Generation Rules

| Rule | Description | Implementation |
|------|-------------|----------------|
| **Random Generation** | Cryptographically secure random | `crypto.randomUUID()` |
| **No Timestamp** | UUID v4 only (no v1) | Prevents time-based attacks |
| **No MAC Address** | No node identifier | Prevents hardware tracking |
| **Hyphenated Format** | Standard hyphenated display | `550e8400-e29b-41d4-a716-446655440000` |
| **Lowercase** | Lowercase hex digits | `550e8400` not `550E8400` |

### UUID Validation

```javascript
// UUID v4 Validation Pattern
const UUID_V4_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;

function isValidUUIDv4(uuid) {
  return UUID_V4_REGEX.test(uuid);
}
```

### UUID Storage

| Format | Size | Description |
|--------|------|-------------|
| **Binary** | 16 bytes | Optimal for storage/indexing |
| **String** | 36 bytes | Display format (with hyphens) |
| **Base64** | 24 bytes | URL-safe encoding |

---

## Human-Readable ID Standards

### ID Format Structure

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    HUMAN-READABLE ID FORMAT                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Format: PREFIX-YYYY-NNNNNN                                                    │
│                                                                                 │
│  ┌─────────────────┬─────────────────┬─────────────────┐                       │
│  │     PREFIX      │      YEAR       │    SEQUENCE     │                       │
│  │   (3-4 chars)   │   (4 digits)    │   (6 digits)    │                       │
│  ├─────────────────┼─────────────────┼─────────────────┤                       │
│  │      PAT        │      2026       │     000001      │                       │
│  └─────────────────┴─────────────────┴─────────────────┘                       │
│                                                                                 │
│  Full ID: PAT-2026-000001                                                     │
│                                                                                 │
│  Components:                                                                   │
│  - PREFIX: Entity type identifier (fixed length)                               │
│  - YEAR: Creation year (prevents sequence reuse)                               │
│  - SEQUENCE: Zero-padded sequential number                                     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Prefix Registry

| Entity | Prefix | Example | Description |
|--------|--------|---------|-------------|
| Patient | `PAT` | `PAT-2026-000001` | Patient identifier |
| Encounter | `ENC` | `ENC-2026-000001` | Healthcare encounter |
| Order | `ORD` | `ORD-2026-000001` | Clinical order |
| Lab Order | `LAB` | `LAB-2026-000001` | Laboratory order |
| Specimen | `SPC` | `SPC-2026-000001` | Biological specimen |
| Lab Result | `RES` | `RES-2026-000001` | Laboratory result |
| Radiology Order | `RAD` | `RAD-2026-000001` | Imaging order |
| Imaging Study | `STU` | `STU-2026-000001` | Imaging study |
| Radiology Report | `RPT` | `RPT-2026-000001` | Radiology report |
| Medication Order | `RX` | `RX-2026-000001` | Medication order |
| Dispensing | `DSP` | `DSP-2026-000001` | Dispensing record |
| Administration | `ADM` | `ADM-2026-000001` | Administration record |
| Appointment | `APT` | `APT-2026-000001` | Scheduled appointment |
| Claim | `CLM` | `CLM-2026-000001` | Insurance claim |
| Payment | `PAY` | `PAY-2026-000001` | Payment record |
| Invoice | `INV` | `INV-2026-000001` | Patient invoice |
| Document | `DOC` | `DOC-2026-000001` | System document |
| Notification | `NTF` | `NTF-2026-000001` | Notification |
| Report | `RPT` | `RPT-2026-000001` | Generated report |
| Workflow | `WRK` | `WRK-2026-000001` | Workflow instance |
| Task | `TSK` | `TSK-2026-000001` | Workflow task |
| Device | `DEV` | `DEV-2026-000001` | Medical device |
| Donor | `DON` | `DON-2026-000001` | Blood donor |
| Blood Unit | `BLD` | `BLD-2026-000001` | Blood unit |
| Transfusion | `TRN` | `TRN-2026-000001` | Transfusion event |
| Safety Event | `SAF` | `SAF-2026-000001` | Safety event |
| Incident | `INC` | `INC-2026-000001` | Incident report |
| Policy | `POL` | `POL-2026-000001` | Policy document |
| Guideline | `GDL` | `GDL-2026-000001` | Clinical guideline |
| Clinical Trial | `TRL` | `TRL-2026-000001` | Clinical trial |
| Enrollment | `ENR` | `ENR-2026-000001` | Trial enrollment |
| Consent | `CNS` | `CNS-2026-000001` | Patient consent |
| Diagnosis | `DX` | `DX-2026-000001` | Medical diagnosis |
| Vital Signs | `VIT` | `VIT-2026-000001` | Vital signs record |
| Care Plan | `CPL` | `CPL-2026-000001` | Patient care plan |
| Care Team | `CTM` | `CTM-2026-000001` | Care team |
| Appointment | `SCH` | `SCH-2026-000001` | Scheduled slot |
| Bed | `BED` | `BED-2026-000001` | Hospital bed |
| Department | `DEP` | `DEP-2026-000001` | Hospital department |
| Hospital | `HOS` | `HOS-2026-000001` | Healthcare facility |
| Supplier | `SUP` | `SUP-2026-000001` | Supply vendor |
| Purchase Order | `PO` | `PO-2026-000001` | Purchase order |
| Inventory Item | `ITM` | `ITM-2026-000001` | Inventory item |
| Batch/Lot | `LOT` | `LOT-2026-000001` | Batch/lot number |
| User | `USR` | `USR-2026-000001` | System user |
| Role | `ROL` | `ROL-2026-000001` | User role |
| Permission | `PRM` | `PRM-2026-000001` | System permission |
| Session | `SES` | `SES-2026-000001` | User session |
| Audit Log | `AUD` | `AUD-2026-000001` | Audit entry |
| Integration Message | `MSG` | `MSG-2026-000001` | Integration message |
| Partner | `PTR` | `PTR-2026-000001` | Integration partner |

### Year Component

| Rule | Description | Example |
|------|-------------|---------|
| **Calendar Year** | 4-digit year of creation | `2026` |
| **Rolling Year** | No reset, sequential continues | `2026-000001` → `2027-000001` |
| **No Overflow** | Year changes, sequence resets | New year = new sequence |

### Sequence Component

| Rule | Description | Example |
|------|-------------|---------|
| **Zero-Padded** | 6-digit zero-padded | `000001` |
| **Sequential** | Incremental numbers | `000001`, `000002`, `000003` |
| **Per-Year Reset** | Sequence resets each year | `2026-000001` → `2027-000001` |
| **No Gaps** | Strictly sequential | No skipping numbers |

---

## Entity Identifier Specifications

### Patient Entity

**Entity ID:** `PATIENT`  
**Primary Key:** `patientId` (UUID v4)  
**Human-Readable ID:** `mrn` (Medical Record Number)

#### MRN (Medical Record Number)

| Attribute | Specification |
|-----------|---------------|
| **Format** | `MRN-YYYY-NNNNNN` |
| **Prefix** | `MRN` |
| **Length** | 16 characters (with hyphens) |
| **Example** | `MRN-2026-000001` |
| **Uniqueness** | Globally unique |
| **Immutability** | Never changes after assignment |
| **Assignment** | Auto-generated at registration |

#### Validation Rules

```javascript
const MRN_REGEX = /^MRN-\d{4}-\d{6}$/;

function validateMRN(mrn) {
  if (!MRN_REGEX.test(mrn)) {
    throw new Error('Invalid MRN format');
  }
  const year = parseInt(mrn.substring(4, 8));
  const currentYear = new Date().getFullYear();
  if (year < 2020 || year > currentYear + 1) {
    throw new Error('Invalid MRN year');
  }
  return true;
}
```

#### Collision Handling

| Strategy | Description |
|----------|-------------|
| **Sequential Generation** | Database sequence ensures no gaps |
| **Year-Based Reset** | New sequence each calendar year |
| **Retry on Conflict** | Automatic retry with next sequence |
| **Audit Logging** | All generation attempts logged |

---

### Encounter Entity

**Entity ID:** `ENCOUNTER`  
**Primary Key:** `encounterId` (UUID v4)  
**Human-Readable ID:** `encounterNumber`

#### Encounter Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `ENC-YYYY-NNNNNN` |
| **Prefix** | `ENC` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `ENC-2026-000001` |
| **Uniqueness** | Globally unique |
| **Immutability** | Never changes |
| **Assignment** | Auto-generated at scheduling |

---

### Order Entity

**Entity ID:** `ORDER`  
**Primary Key:** `orderId` (UUID v4)  
**Human-Readable ID:** `orderNumber`

#### Order Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `ORD-YYYY-NNNNNN` |
| **Prefix** | `ORD` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `ORD-2026-000001` |
| **Uniqueness** | Globally unique |
| **Immutability** | Never changes |
| **Assignment** | Auto-generated at submission |

---

### Laboratory Domain Entities

#### Lab Order Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `LAB-YYYY-NNNNNN` |
| **Prefix** | `LAB` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `LAB-2026-000001` |
| **Uniqueness** | Globally unique |

#### Specimen Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `SPC-YYYY-NNNNNN` |
| **Prefix** | `SPC` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `SPC-2026-000001` |
| **Uniqueness** | Globally unique |

#### Lab Result Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `RES-YYYY-NNNNNN` |
| **Prefix** | `RES` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `RES-2026-000001` |
| **Uniqueness** | Globally unique |

---

### Radiology Domain Entities

#### Radiology Order Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `RAD-YYYY-NNNNNN` |
| **Prefix** | `RAD` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `RAD-2026-000001` |
| **Uniqueness** | Globally unique |

#### Imaging Study Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `STU-YYYY-NNNNNN` |
| **Prefix** | `STU` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `STU-2026-000001` |
| **Uniqueness** | Globally unique |
| **DICOM UID** | Separate DICOM UID for PACS |

#### Radiology Report Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `RPT-YYYY-NNNNNN` |
| **Prefix** | `RPT` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `RPT-2026-000001` |
| **Uniqueness** | Globally unique |

---

### Pharmacy Domain Entities

#### Medication Order Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `RX-YYYY-NNNNNN` |
| **Prefix** | `RX` |
| **Length** | 14 characters (with hyphens) |
| **Example** | `RX-2026-000001` |
| **Uniqueness** | Globally unique |

#### Dispensing Record Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `DSP-YYYY-NNNNNN` |
| **Prefix** | `DSP` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `DSP-2026-000001` |
| **Uniqueness** | Globally unique |

#### Administration Record Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `ADM-YYYY-NNNNNN` |
| **Prefix** | `ADM` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `ADM-2026-000001` |
| **Uniqueness** | Globally unique |

---

### Scheduling Domain Entities

#### Appointment Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `APT-YYYY-NNNNNN` |
| **Prefix** | `APT` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `APT-2026-000001` |
| **Uniqueness** | Globally unique |

---

### Finance Domain Entities

#### Claim Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `CLM-YYYY-NNNNNN` |
| **Prefix** | `CLM` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `CLM-2026-000001` |
| **Uniqueness** | Globally unique |
| **Payer Claim ID** | Separate payer-assigned ID |

#### Payment Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `PAY-YYYY-NNNNNN` |
| **Prefix** | `PAY` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `PAY-2026-000001` |
| **Uniqueness** | Globally unique |

#### Invoice Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `INV-YYYY-NNNNNN` |
| **Prefix** | `INV` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `INV-2026-000001` |
| **Uniqueness** | Globally unique |

---

### Document Domain Entities

#### Document Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `DOC-YYYY-NNNNNN` |
| **Prefix** | `DOC` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `DOC-2026-000001` |
| **Uniqueness** | Globally unique |

---

### Notification Domain Entities

#### Notification Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `NTF-YYYY-NNNNNN` |
| **Prefix** | `NTF` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `NTF-2026-000001` |
| **Uniqueness** | Globally unique |

---

### Workflow Domain Entities

#### Workflow Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `WRK-YYYY-NNNNNN` |
| **Prefix** | `WRK` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `WRK-2026-000001` |
| **Uniqueness** | Globally unique |

#### Task Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `TSK-YYYY-NNNNNN` |
| **Prefix** | `TSK` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `TSK-2026-000001` |
| **Uniqueness** | Globally unique |

---

### Hospital Domain Entities

#### Hospital Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `HOS-YYYY-NNNNNN` |
| **Prefix** | `HOS` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `HOS-2026-000001` |
| **Uniqueness** | Globally unique |

#### Department Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `DEP-YYYY-NNNNNN` |
| **Prefix** | `DEP` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `DEP-2026-000001` |
| **Uniqueness** | Globally unique |

#### Bed Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `BED-YYYY-NNNNNN` |
| **Prefix** | `BED` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `BED-2026-000001` |
| **Uniqueness** | Within department |

---

### Medical Device Domain Entities

#### Device Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `DEV-YYYY-NNNNNN` |
| **Prefix** | `DEV` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `DEV-2026-000001` |
| **Uniqueness** | Globally unique |
| **Serial Number** | Manufacturer serial (separate field) |

---

### Blood Bank Domain Entities

#### Donor Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `DON-YYYY-NNNNNN` |
| **Prefix** | `DON` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `DON-2026-000001` |
| **Uniqueness** | Globally unique |

#### Blood Unit Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `BLD-YYYY-NNNNNN` |
| **Prefix** | `BLD` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `BLD-2026-000001` |
| **Uniqueness** | Globally unique |

#### Transfusion Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `TRN-YYYY-NNNNNN` |
| **Prefix** | `TRN` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `TRN-2026-000001` |
| **Uniqueness** | Globally unique |

---

### Quality & Safety Domain Entities

#### Safety Event Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `SAF-YYYY-NNNNNN` |
| **Prefix** | `SAF` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `SAF-2026-000001` |
| **Uniqueness** | Globally unique |

#### Incident Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `INC-YYYY-NNNNNN` |
| **Prefix** | `INC` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `INC-2026-000001` |
| **Uniqueness** | Globally unique |

---

### Policy Domain Entities

#### Policy Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `POL-YYYY-NNNNNN` |
| **Prefix** | `POL` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `POL-2026-000001` |
| **Uniqueness** | Globally unique |

#### Guideline Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `GDL-YYYY-NNNNNN` |
| **Prefix** | `GDL` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `GDL-2026-000001` |
| **Uniqueness** | Globally unique |

---

### Research Domain Entities

#### Clinical Trial Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `TRL-YYYY-NNNNNN` |
| **Prefix** | `TRL` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `TRL-2026-000001` |
| **Uniqueness** | Globally unique |
| **NCT Number** | ClinicalTrials.gov ID (separate) |

#### Enrollment Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `ENR-YYYY-NNNNNN` |
| **Prefix** | `ENR` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `ENR-2026-000001` |
| **Uniqueness** | Within trial |

---

### Patient Engagement Domain Entities

#### Care Plan Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `CPL-YYYY-NNNNNN` |
| **Prefix** | `CPL` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `CPL-2026-000001` |
| **Uniqueness** | Globally unique |

#### Care Team Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `CTM-YYYY-NNNNNN` |
| **Prefix** | `CTM` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `CTM-2026-000001` |
| **Uniqueness** | Globally unique |

---

### Clinical Entities

#### Diagnosis Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `DX-YYYY-NNNNNN` |
| **Prefix** | `DX` |
| **Length** | 14 characters (with hyphens) |
| **Example** | `DX-2026-000001` |
| **Uniqueness** | Globally unique |

#### Vital Signs Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `VIT-YYYY-NNNNNN` |
| **Prefix** | `VIT` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `VIT-2026-000001` |
| **Uniqueness** | Per encounter |

#### Consent Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `CNS-YYYY-NNNNNN` |
| **Prefix** | `CNS` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `CNS-2026-000001` |
| **Uniqueness** | Globally unique |

---

### Identity Domain Entities

#### User Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `USR-YYYY-NNNNNN` |
| **Prefix** | `USR` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `USR-2026-000001` |
| **Uniqueness** | Globally unique |
| **Username** | Separate unique username |

#### Role Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `ROL-YYYY-NNNNNN` |
| **Prefix** | `ROL` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `ROL-2026-000001` |
| **Uniqueness** | Globally unique |

#### Permission Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `PRM-YYYY-NNNNNN` |
| **Prefix** | `PRM` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `PRM-2026-000001` |
| **Uniqueness** | Globally unique |

#### Session Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `SES-YYYY-NNNNNN` |
| **Prefix** | `SES` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `SES-2026-000001` |
| **Uniqueness** | Globally unique |

#### Audit Log Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `AUD-YYYY-NNNNNN` |
| **Prefix** | `AUD` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `AUD-2026-000001` |
| **Uniqueness** | Globally unique |

---

### Integration Domain Entities

#### Message Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `MSG-YYYY-NNNNNN` |
| **Prefix** | `MSG` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `MSG-2026-000001` |
| **Uniqueness** | Globally unique |

#### Partner Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `PTR-YYYY-NNNNNN` |
| **Prefix** | `PTR` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `PTR-2026-000001` |
| **Uniqueness** | Globally unique |

---

### Supply Chain Domain Entities

#### Purchase Order Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `PO-YYYY-NNNNNN` |
| **Prefix** | `PO` |
| **Length** | 14 characters (with hyphens) |
| **Example** | `PO-2026-000001` |
| **Uniqueness** | Globally unique |

#### Supplier Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `SUP-YYYY-NNNNNN` |
| **Prefix** | `SUP` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `SUP-2026-000001` |
| **Uniqueness** | Globally unique |

#### Inventory Item Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `ITM-YYYY-NNNNNN` |
| **Prefix** | `ITM` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `ITM-2026-000001` |
| **Uniqueness** | Globally unique |

#### Batch/Lot Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `LOT-YYYY-NNNNNN` |
| **Prefix** | `LOT` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `LOT-2026-000001` |
| **Uniqueness** | Within item |

---

### Reporting Domain Entities

#### Report Number

| Attribute | Specification |
|-----------|---------------|
| **Format** | `RPT-YYYY-NNNNNN` |
| **Prefix** | `RPT` |
| **Length** | 15 characters (with hyphens) |
| **Example** | `RPT-2026-000001` |
| **Uniqueness** | Globally unique |

---

## Validation Rules

### General Validation

| Rule | Description | Implementation |
|------|-------------|----------------|
| **Format Check** | Matches expected pattern | Regex validation |
| **Length Check** | Correct character count | String length |
| **Character Set** | Only valid characters | `[A-Z0-9-]` |
| **Prefix Match** | Correct entity prefix | Entity-specific |
| **Year Range** | Valid year component | 2020-2099 |
| **Sequence Range** | Valid sequence number | 000001-999999 |

### Entity-Specific Validation

```javascript
// Validation rules per entity type
const VALIDATION_RULES = {
  PATIENT: {
    format: /^PAT-\d{4}-\d{6}$/,
    prefix: 'PAT',
    yearRange: [2020, 2099],
    sequenceRange: [1, 999999]
  },
  ENCOUNTER: {
    format: /^ENC-\d{4}-\d{6}$/,
    prefix: 'ENC',
    yearRange: [2020, 2099],
    sequenceRange: [1, 999999]
  },
  ORDER: {
    format: /^ORD-\d{4}-\d{6}$/,
    prefix: 'ORD',
    yearRange: [2020, 2099],
    sequenceRange: [1, 999999]
  },
  LAB_ORDER: {
    format: /^LAB-\d{4}-\d{6}$/,
    prefix: 'LAB',
    yearRange: [2020, 2099],
    sequenceRange: [1, 999999]
  }
};
```

### Validation Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         VALIDATION FLOW                                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Input ID                                                                     │
│      │                                                                         │
│      ▼                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  1. FORMAT VALIDATION                                                    │   │
│  │     • Check regex pattern                                                │   │
│  │     • Verify length                                                      │   │
│  │     • Check character set                                                │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│      │                                                                         │
│      ▼                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  2. PREFIX VALIDATION                                                    │   │
│  │     • Verify entity prefix                                              │   │
│  │     • Check prefix registry                                              │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│      │                                                                         │
│      ▼                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  3. YEAR VALIDATION                                                      │   │
│  │     • Check year range                                                   │   │
│  │     • Verify reasonable date                                             │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│      │                                                                         │
│      ▼                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  4. SEQUENCE VALIDATION                                                  │   │
│  │     • Check sequence range                                               │   │
│  │     • Verify not zero                                                    │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│      │                                                                         │
│      ▼                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  5. EXISTENCE CHECK                                                      │   │
│  │     • Query database                                                     │   │
│  │     • Verify entity exists                                               │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│      │                                                                         │
│      ▼                                                                         │
│  Valid/Invalid                                                                 │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Collision Handling

### Collision Prevention Strategies

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    COLLISION PREVENTION STRATEGIES                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  1. SEQUENTIAL GENERATION                                                      │
│     ┌─────────────────────────────────────────────────────────────────────────┐│
│     │  • Database sequence per entity type                                    ││
│     │  • Atomic increment operation                                           ││
│     │  • No gaps in sequence                                                  ││
│     │  • Year-based reset                                                     ││
│     └─────────────────────────────────────────────────────────────────────────┘│
│                                                                                 │
│  2. UUID GENERATION                                                            │
│     ┌─────────────────────────────────────────────────────────────────────────┐│
│     │  • Cryptographically secure random                                      ││
│     │  • 128-bit space (2^128 combinations)                                  ││
│     │  • Collision probability negligible                                     ││
│     │  • No coordination required                                             ││
│     └─────────────────────────────────────────────────────────────────────────┘│
│                                                                                 │
│  3. DISTRIBUTED GENERATION                                                     │
│     ┌─────────────────────────────────────────────────────────────────────────┐│
│     │  • Snowflake-style IDs (optional)                                       ││
│     │  • Timestamp + Machine ID + Sequence                                   ││
│     │  • Globally unique without coordination                                ││
│     │  • Time-ordered                                                        ││
│     └─────────────────────────────────────────────────────────────────────────┘│
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Collision Detection

| Method | Description | Implementation |
|--------|-------------|----------------|
| **Database Constraint** | Unique constraint on ID column | `UNIQUE` constraint |
| **Application Check** | Pre-insert existence check | `SELECT COUNT(*)` |
| **Optimistic Locking** | Version-based conflict detection | `version` column |
| **Pessimistic Locking** | Exclusive lock during generation | `SELECT FOR UPDATE` |

### Collision Resolution

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       COLLISION RESOLUTION                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Detection                                                                     │
│      │                                                                         │
│      ▼                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  Unique Constraint Violation                                             │   │
│  │  • Database throws DuplicateKeyError                                     │   │
│  │  • Application catches exception                                         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│      │                                                                         │
│      ▼                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  Resolution Strategy                                                    │   │
│  │  • Retry with next sequence number                                      │   │
│  │  • Maximum 3 retry attempts                                             │   │
│  │  • Log collision event                                                  │   │
│  │  • Alert if persistent                                                  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│      │                                                                         │
│      ▼                                                                         │
│  Success or Escalate                                                           │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Collision Handling Code

```javascript
async function generateUniqueID(entityType, tenantId) {
  const MAX_RETRIES = 3;
  let attempt = 0;
  
  while (attempt < MAX_RETRIES) {
    try {
      const sequence = await getNextSequence(entityType, tenantId);
      const year = new Date().getFullYear();
      const prefix = ENTITY_PREFIXES[entityType];
      const id = `${prefix}-${year}-${sequence.toString().padStart(6, '0')}`;
      
      // Verify uniqueness
      const exists = await checkIDExists(entityType, id);
      if (!exists) {
        return id;
      }
      
      // Collision detected, retry
      attempt++;
      logCollision(entityType, id, attempt);
      
    } catch (error) {
      throw new Error(`ID generation failed: ${error.message}`);
    }
  }
  
  throw new Error(`ID generation failed after ${MAX_RETRIES} attempts`);
}
```

---

## Migration & Compatibility

### Legacy ID Migration

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    LEGACY ID MIGRATION STRATEGY                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Phase 1: Assessment                                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  • Inventory all legacy ID formats                                      │   │
│  │  • Map to new NHDOS format                                              │   │
│  │  • Identify conflicts                                                    │   │
│  │  • Plan migration sequence                                              │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  Phase 2: Dual-Write                                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  • Write both old and new IDs                                           │   │
│  │  • Maintain mapping table                                               │   │
│  │  • Support both formats during transition                               │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  Phase 3: Migration                                                            │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  • Batch update legacy IDs                                              │   │
│  │  • Update all references                                                │   │
│  │  • Validate data integrity                                              │   │
│  │  • Update documentation                                                 │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  Phase 4: Cleanup                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  • Remove legacy ID support                                             │   │
│  │  • Drop mapping tables                                                  │   │
│  │  • Update APIs to new format only                                       │   │
│  │  • Archive migration logs                                               │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Mapping Table Structure

| Legacy ID | New ID | Entity Type | Migration Date | Status |
|-----------|--------|-------------|----------------|--------|
| `OLD-12345` | `PAT-2026-000001` | Patient | 2026-06-25 | Migrated |
| `MRN-98765` | `PAT-2026-000002` | Patient | 2026-06-25 | Migrated |
| `VISIT-555` | `ENC-2026-000001` | Encounter | 2026-06-25 | Migrated |

### Compatibility Layers

| Layer | Purpose | Implementation |
|-------|---------|----------------|
| **API Gateway** | Translate IDs in requests | ID translation middleware |
| **Database Views** | Expose both formats | SQL views with ID mapping |
| **Cache Layer** | Cache ID mappings | Redis hash mapping |
| **Search Index** | Index both formats | Dual-field indexing |

### External System Integration

| System | ID Format | NHDOS Format | Mapping |
|--------|-----------|--------------|---------|
| **HL7 FHIR** | Resource ID | UUID | Direct mapping |
| **DICOM** | Study Instance UID | UUID | Direct mapping |
| **X12** | Subscriber ID | MRN | Custom mapping |
| **NPI** | NPI Number | NPI Number | Direct storage |
| **ICD-10** | Diagnosis Code | Diagnosis Code | Direct storage |
| **LOINC** | Test Code | Test Code | Direct storage |
| **SNOMED CT** | Concept ID | Concept ID | Direct storage |

---

## Appendix: ID Format Summary

| Entity | Format | Example | Length |
|--------|--------|---------|--------|
| Patient | `PAT-YYYY-NNNNNN` | `PAT-2026-000001` | 15 |
| Encounter | `ENC-YYYY-NNNNNN` | `ENC-2026-000001` | 15 |
| Order | `ORD-YYYY-NNNNNN` | `ORD-2026-000001` | 15 |
| Lab Order | `LAB-YYYY-NNNNNN` | `LAB-2026-000001` | 15 |
| Specimen | `SPC-YYYY-NNNNNN` | `SPC-2026-000001` | 15 |
| Lab Result | `RES-YYYY-NNNNNN` | `RES-2026-000001` | 15 |
| Radiology Order | `RAD-YYYY-NNNNNN` | `RAD-2026-000001` | 15 |
| Imaging Study | `STU-YYYY-NNNNNN` | `STU-2026-000001` | 15 |
| Radiology Report | `RPT-YYYY-NNNNNN` | `RPT-2026-000001` | 15 |
| Medication Order | `RX-YYYY-NNNNNN` | `RX-2026-000001` | 14 |
| Dispensing | `DSP-YYYY-NNNNNN` | `DSP-2026-000001` | 15 |
| Administration | `ADM-YYYY-NNNNNN` | `ADM-2026-000001` | 15 |
| Appointment | `APT-YYYY-NNNNNN` | `APT-2026-000001` | 15 |
| Claim | `CLM-YYYY-NNNNNN` | `CLM-2026-000001` | 15 |
| Payment | `PAY-YYYY-NNNNNN` | `PAY-2026-000001` | 15 |
| Invoice | `INV-YYYY-NNNNNN` | `INV-2026-000001` | 15 |
| Document | `DOC-YYYY-NNNNNN` | `DOC-2026-000001` | 15 |
| Notification | `NTF-YYYY-NNNNNN` | `NTF-2026-000001` | 15 |
| Report | `RPT-YYYY-NNNNNN` | `RPT-2026-000001` | 15 |
| Workflow | `WRK-YYYY-NNNNNN` | `WRK-2026-000001` | 15 |
| Task | `TSK-YYYY-NNNNNN` | `TSK-2026-000001` | 15 |
| Device | `DEV-YYYY-NNNNNN` | `DEV-2026-000001` | 15 |
| Donor | `DON-YYYY-NNNNNN` | `DON-2026-000001` | 15 |
| Blood Unit | `BLD-YYYY-NNNNNN` | `BLD-2026-000001` | 15 |
| Transfusion | `TRN-YYYY-NNNNNN` | `TRN-2026-000001` | 15 |
| Safety Event | `SAF-YYYY-NNNNNN` | `SAF-2026-000001` | 15 |
| Incident | `INC-YYYY-NNNNNN` | `INC-2026-000001` | 15 |
| Policy | `POL-YYYY-NNNNNN` | `POL-2026-000001` | 15 |
| Guideline | `GDL-YYYY-NNNNNN` | `GDL-2026-000001` | 15 |
| Clinical Trial | `TRL-YYYY-NNNNNN` | `TRL-2026-000001` | 15 |
| Enrollment | `ENR-YYYY-NNNNNN` | `ENR-2026-000001` | 15 |
| Consent | `CNS-YYYY-NNNNNN` | `CNS-2026-000001` | 15 |
| Diagnosis | `DX-YYYY-NNNNNN` | `DX-2026-000001` | 14 |
| Vital Signs | `VIT-YYYY-NNNNNN` | `VIT-2026-000001` | 15 |
| Care Plan | `CPL-YYYY-NNNNNN` | `CPL-2026-000001` | 15 |
| Care Team | `CTM-YYYY-NNNNNN` | `CTM-2026-000001` | 15 |
| User | `USR-YYYY-NNNNNN` | `USR-2026-000001` | 15 |
| Role | `ROL-YYYY-NNNNNN` | `ROL-2026-000001` | 15 |
| Permission | `PRM-YYYY-NNNNNN` | `PRM-2026-000001` | 15 |
| Session | `SES-YYYY-NNNNNN` | `SES-2026-000001` | 15 |
| Audit Log | `AUD-YYYY-NNNNNN` | `AUD-2026-000001` | 15 |
| Message | `MSG-YYYY-NNNNNN` | `MSG-2026-000001` | 15 |
| Partner | `PTR-YYYY-NNNNNN` | `PTR-2026-000001` | 15 |
| Purchase Order | `PO-YYYY-NNNNNN` | `PO-2026-000001` | 14 |
| Supplier | `SUP-YYYY-NNNNNN` | `SUP-2026-000001` | 15 |
| Inventory Item | `ITM-YYYY-NNNNNN` | `ITM-2026-000001` | 15 |
| Batch/Lot | `LOT-YYYY-NNNNNN` | `LOT-2026-000001` | 15 |

---

**Document Classification:** CANONICAL STANDARD  
**Review Cycle:** Quarterly  
**Next Review Date:** 2026-09-25  
**Approved By:** NHDOS Architecture Board