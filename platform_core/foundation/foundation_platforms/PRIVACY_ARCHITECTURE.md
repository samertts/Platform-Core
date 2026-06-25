# PRIVACY ARCHITECTURE

**NHDOS Platform-Core — Foundation Platform 6: Privacy Architecture**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The Privacy Architecture defines the data protection framework for NHDOS, implementing privacy by design principles, data classification, data minimization, purpose limitation, storage limitation, and accountability measures for 44 million citizens' health data across 18 governorates.

---

## 2. Architecture

### 2.1 Core Principles

| Principle | Description |
|-----------|-------------|
| Privacy by Design | Privacy embedded into system design |
| Data Minimization | Collect only necessary data |
| Purpose Limitation | Use data only for consented purposes |
| Storage Limitation | Retain data only as long as needed |
| Integrity | Protect data from unauthorized changes |
| Confidentiality | Protect data from unauthorized access |
| Accountability | Document all data processing activities |

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRIVACY ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Data        │  │   Purpose    │  │   Consent    │          │
│  │  Classification│▶│   Limitation │──▶│   Engine     │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │  Data        │  │   Access     │  │   Audit      │          │
│  │  Minimization│  │   Control    │  │   Trail      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Classification

### 3.1 Classification Levels

| Level | Description | Consent Required | Encryption |
|-------|-------------|------------------|------------|
| Public | Non-sensitive data | No | Optional |
| Internal | Organization-internal data | No | Recommended |
| Confidential | Sensitive health data | Yes | Required |
| Restricted | Highly sensitive data | Explicit Yes | Required + HSM |
| Secret | National security data | Special Authorization | Required + HSM + Air-gap |

### 3.2 Data Categories

| Category | Classification | Examples |
|----------|---------------|----------|
| Demographics | Confidential | Name, DOB, Gender |
| Health Records | Restricted | Diagnoses, Treatments |
| Lab Results | Restricted | Test Results, Reports |
| Financial | Confidential | Insurance, Payments |
| Research Data | Confidential | De-identified datasets |
| Audit Logs | Internal | System logs, Access logs |

---

## 4. Privacy Controls

### 4.1 Technical Controls

| Control | Description | Implementation |
|---------|-------------|----------------|
| Encryption at Rest | AES-256 encryption | Storage layer |
| Encryption in Transit | TLS 1.3 | Network layer |
| Access Control | RBAC + ABAC | Authorization layer |
| Data Masking | Dynamic masking | Query layer |
| Pseudonymization | Token-based identifiers | Identity layer |
| De-identification | K-anonymity, L-diversity | Analytics layer |

### 4.2 Organizational Controls

| Control | Description | Implementation |
|---------|-------------|----------------|
| Privacy Impact Assessment | PIA for new systems | Process |
| Data Protection Officer | DPO oversight | Organization |
| Training | Privacy awareness training | Annual |
| Incident Response | Breach notification | 72-hour window |

---

## 5. Data Retention

### 5.1 Retention Policies

| Data Type | Retention Period | Archive Period |
|-----------|-----------------|----------------|
| Patient Records | 10 years | 20 years |
| Lab Results | 5 years | 10 years |
| Imaging Data | 10 years | 20 years |
| Financial Records | 7 years | 10 years |
| Audit Logs | 3 years | 7 years |
| Research Data | Study duration + 5 years | Indefinite |

### 5.2 Retention Enforcement

| Action | Description | Automation |
|--------|-------------|------------|
| Auto-Archive | Move to archive after retention | Automated |
| Auto-Delete | Delete after archive period | Automated |
| Manual Review | Review before deletion | Manual |
| Legal Hold | Override retention for legal | Manual |

---

## 6. Privacy APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/privacy/classify | POST | Classify data |
| /api/v1/privacy/assess | POST | Privacy impact assessment |
| /api/v1/privacy/mask | POST | Apply data masking |
| /api/v1/privacy/deidentify | POST | De-identify data |
| /api/v1/privacy/retention | GET | Get retention policy |
| /api/v1/privacy/audit | GET | Get privacy audit trail |

---

## 7. Offline Support

| Capability | Implementation |
|------------|----------------|
| Local Classification | Classification enforced locally |
| Encryption | Local encryption at rest |
| Access Control | Local RBAC enforcement |
| Audit Trail | Local audit with sync |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
