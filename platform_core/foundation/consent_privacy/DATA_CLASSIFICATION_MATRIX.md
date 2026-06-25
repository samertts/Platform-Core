# DATA CLASSIFICATION MATRIX

**NHDOS Platform-Core — Data Classification Framework**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Classification Levels

| Level | Name | Description | Examples |
|-------|------|-------------|----------|
| 1 | Public | Non-sensitive, publicly available | Facility locations, public health statistics |
| 2 | Internal | Organization-internal data | Internal policies, organizational charts |
| 3 | Confidential | Sensitive health data | Patient records, lab results, prescriptions |
| 4 | Restricted | Highly sensitive data | Mental health, HIV/AIDS, genetic data |
| 5 | Secret | National security data | National health security intelligence |

---

## 2. Entity Classification

### 2.1 Citizen & Patient Data

| Entity | Classification | Encryption | Access Control |
|--------|----------------|------------|----------------|
| Citizen.PII | Level 5 | AES-256-GCM + Field-level | RBAC + ABAC |
| Citizen.Contact | Level 4 | AES-256-GCM | RBAC + ABAC |
| Patient.Record | Level 5 | AES-256-GCM + Field-level | RBAC + ABAC |
| Patient.Clinical | Level 5 | AES-256-GCM + Field-level | RBAC + ABAC |
| Patient.Financial | Level 4 | AES-256-GCM | RBAC + ABAC |

### 2.2 Clinical Data

| Entity | Classification | Encryption | Access Control |
|--------|----------------|------------|----------------|
| Encounter | Level 5 | AES-256-GCM | RBAC + ABAC |
| Diagnosis | Level 5 | AES-256-GCM | RBAC + ABAC |
| Prescription | Level 5 | AES-256-GCM | RBAC + ABAC |
| Lab Result | Level 5 | AES-256-GCM | RBAC + ABAC |
| Imaging | Level 5 | AES-256-GCM | RBAC + ABAC |

### 2.3 Professional Data

| Entity | Classification | Encryption | Access Control |
|--------|----------------|------------|----------------|
| Professional.License | Level 4 | AES-256-GCM | RBAC |
| Professional.Contact | Level 3 | AES-256-GCM | RBAC |
| Professional.Credentials | Level 4 | AES-256-GCM | RBAC |

### 2.4 Organizational Data

| Entity | Classification | Encryption | Access Control |
|--------|----------------|------------|----------------|
| Organization.Details | Level 2 | AES-256-GCM | RBAC |
| Facility.Details | Level 2 | AES-256-GCM | RBAC |
| Department.Details | Level 2 | AES-256-GCM | RBAC |

### 2.5 Reference Data

| Entity | Classification | Encryption | Access Control |
|--------|----------------|------------|----------------|
| ICD-11 Codes | Level 1 | None | Public |
| SNOMED CT Codes | Level 1 | None | Public |
| LOINC Codes | Level 1 | None | Public |
| Geographic Data | Level 1 | None | Public |

---

## 3. Handling Requirements

### 3.1 Storage Requirements

| Level | Storage | Backup | Retention |
|-------|---------|--------|-----------|
| 1 | Standard | Standard | As needed |
| 2 | Encrypted | Encrypted | Policy-based |
| 3 | Encrypted + Access Logged | Encrypted | Policy-based |
| 4 | Encrypted + Field-level + Access Logged | Encrypted + Access Logged | Strict policy |
| 5 | Encrypted + Field-level + Access Logged + Audit | Encrypted + Access Logged + Audit | National regulation |

### 3.2 Transmission Requirements

| Level | Protocol | Authentication |
|-------|----------|----------------|
| 1 | HTTPS | API Key |
| 2 | HTTPS | JWT |
| 3 | HTTPS + Encryption | JWT + MFA |
| 4 | HTTPS + Encryption + Signing | JWT + MFA + Certificate |
| 5 | HTTPS + Encryption + Signing + HSM | JWT + MFA + HSM |

### 3.3 Access Requirements

| Level | Authorization | Approval | Audit |
|-------|---------------|----------|-------|
| 1 | Public | None | None |
| 2 | RBAC | Role-based | Basic |
| 3 | RBAC + Purpose | Purpose-based | Full |
| 4 | RBAC + Purpose + Time | Time-limited | Full + Alert |
| 5 | RBAC + Purpose + Time + Location | Multi-level | Full + Alert + Review |

---

## 4. Data Masking Rules

### 4.1 Masking Levels

| Level | Description | Example |
|-------|-------------|---------|
| None | No masking | Full data visible |
| Partial | Partial masking | 123***789 |
| Full | Full masking | ********* |
| Redacted | Data removed | [REDACTED] |

### 4.2 Field Masking Rules

| Field | Production | Non-Production | Test |
|-------|------------|----------------|------|
| National ID | None | Partial | Full |
| Full Name | None | Partial | Full |
| Phone | None | Partial | Full |
| Email | None | Partial | Full |
| Address | None | Partial | Full |
| DOB | None | Partial | Full |
| Lab Results | None | None | None |
| Diagnoses | None | None | None |

---

## 5. Compliance Requirements

| Regulation | Classification Required | Audit Required |
|------------|-------------------------|----------------|
| National Health Data Law | Yes | Yes |
| Privacy Regulation | Yes | Yes |
| GDPR (if applicable) | Yes | Yes |
| HIPAA (if applicable) | Yes | Yes |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
