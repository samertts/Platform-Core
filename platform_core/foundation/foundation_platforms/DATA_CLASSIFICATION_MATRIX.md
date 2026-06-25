# DATA CLASSIFICATION MATRIX

**NHDOS Platform-Core — Foundation Platform 16: Data Classification Matrix**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The Data Classification Matrix defines data classification levels and corresponding security controls for all NHDOS data, ensuring appropriate protection for 44 million citizens' health data across 18 governorates.

---

## 2. Architecture

### 2.1 Classification Levels

| Level | Description | Consent Required | Encryption | Access Control |
|-------|-------------|------------------|------------|----------------|
| Public | Non-sensitive data | No | Optional | Public |
| Internal | Organization-internal data | No | Recommended | RBAC |
| Confidential | Sensitive health data | Yes | Required | RBAC + MFA |
| Restricted | Highly sensitive data | Explicit Yes | Required + HSM | RBAC + MFA + Audit |
| Secret | National security data | Special Auth | Required + HSM + Air-gap | RBAC + MFA + Audit + Clearance |

---

## 3. Classification Matrix

### 3.1 Patient Data

| Data Element | Classification | Justification |
|--------------|----------------|---------------|
| Patient ID | Internal | Identifier |
| Name | Confidential | PII |
| Date of Birth | Confidential | PII |
| Gender | Confidential | PII |
| Address | Confidential | PII |
| Phone Number | Confidential | PII |
| National ID | Restricted | National identifier |
| Diagnoses | Restricted | Health data |
| Medications | Restricted | Health data |
| Lab Results | Restricted | Health data |
| Imaging Data | Restricted | Health data |
| Genetic Data | Secret | Highly sensitive |

### 3.2 Clinical Data

| Data Element | Classification | Justification |
|--------------|----------------|---------------|
| Encounter Type | Internal | Operational |
| Encounter Date | Confidential | Health data |
| Provider Name | Internal | Professional |
| Clinical Notes | Restricted | Health data |
| Procedures | Restricted | Health data |
| Allergies | Restricted | Health data |
| Vital Signs | Confidential | Health data |

### 3.3 Financial Data

| Data Element | Classification | Justification |
|--------------|----------------|---------------|
| Insurance ID | Confidential | Financial |
| Coverage Type | Confidential | Financial |
| Claims Data | Confidential | Financial |
| Payment Data | Restricted | Financial |
| Bank Details | Restricted | Financial |

### 3.4 Operational Data

| Data Element | Classification | Justification |
|--------------|----------------|---------------|
| Facility Name | Public | Public info |
| Facility Address | Public | Public info |
| Provider Specialty | Internal | Professional |
| System Logs | Internal | Operational |
| Audit Logs | Confidential | Security |
| Error Logs | Internal | Operational |

---

## 4. Security Controls by Classification

### 4.1 Access Controls

| Level | Authentication | Authorization | Monitoring |
|-------|----------------|---------------|------------|
| Public | None | None | Basic |
| Internal | Single factor | RBAC | Standard |
| Confidential | MFA | RBAC + Purpose | Enhanced |
| Restricted | MFA + Biometric | RBAC + MFA + Purpose | Full |
| Secret | MFA + Biometric + Physical | RBAC + MFA + Purpose + Clearance | Full + Real-time |

### 4.2 Encryption Controls

| Level | At Rest | In Transit | Key Management |
|-------|---------|------------|----------------|
| Public | Optional | TLS 1.2+ | Standard |
| Internal | AES-128 | TLS 1.2+ | Standard |
| Confidential | AES-256 | TLS 1.3 | HSM |
| Restricted | AES-256 | TLS 1.3 | HSM |
| Secret | AES-256 + Air-gap | TLS 1.3 + Air-gap | HSM + Physical |

### 4.3 Retention Controls

| Level | Retention | Archive | Deletion |
|-------|-----------|---------|----------|
| Public | Indefinite | None | Manual |
| Internal | 7 years | 10 years | Automated |
| Confidential | 10 years | 20 years | Automated |
| Restricted | 10 years | 20 years | Manual + Audit |
| Secret | Indefinite | Indefinite | Manual + Audit + Clearance |

---

## 5. APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/classification | GET | Get classification matrix |
| /api/v1/classification/{element} | GET | Get element classification |
| /api/v1/classification/{element}/controls | GET | Get security controls |
| /api/v1/classification/validate | POST | Validate classification |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
