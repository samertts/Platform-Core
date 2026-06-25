# CONSENT PLATFORM

**NHDOS Platform-Core — Consent & Privacy Platform**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The Consent & Privacy Platform provides sovereign consent management for the National Healthcare Digital Operating System. It supports patient consent, guardian consent, emergency override, break glass, delegation, consent revocation, consent expiration, purpose-based access, privacy policies, and consent audit.

---

## 2. Architecture

### 2.1 Core Principles

| Principle | Description |
|-----------|-------------|
| Patient Ownership | Patients own their health data |
| Explicit Consent | Consent must be explicit and informed |
| Purpose Limitation | Data used only for consented purposes |
| Granular Control | Consent can be granted per purpose |
| Audit Trail | All consent actions are auditable |
| Emergency Override | Break glass for life-threatening emergencies |

### 2.2 Consent Lifecycle

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Draft   │────▶│  Active  │────▶│ Expired  │────▶│ Archived │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
      │               │               │               │
      ▼               ▼               ▼               ▼
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Rejected │     │ Revoked  │     │ Suspended│     │ Deleted  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
```

---

## 3. Consent Types

### 3.1 Consent Categories

| Type | Description | Scope |
|------|-------------|-------|
| Treatment | Consent for medical treatment | Per encounter |
| Data Sharing | Consent to share data with other providers | Per provider |
| Research | Consent for research use | Per study |
| Marketing | Consent for marketing communications | Organization-wide |
| Emergency | Emergency access override | Time-limited |
| Guardian | Consent by legal guardian | Per patient |

### 3.2 Consent Granularity

| Level | Description | Example |
|-------|-------------|---------|
| Global | Consent for all purposes | "Share all my data" |
| Category | Consent for data category | "Share lab results" |
| Specific | Consent for specific data | "Share CBC results from Lab X" |
| Time-limited | Consent with expiration | "Share for 30 days" |

---

## 4. Consent Policies

### 4.1 Policy Rules

| Rule | Description | Enforcement |
|------|-------------|-------------|
| Explicit Consent Required | Patient must explicitly consent | Blocking |
| Consent Expiry | Consent expires after defined period | Warning |
| Purpose Match | Data use must match consent purpose | Blocking |
| Guardian Consent | Minors require guardian consent | Blocking |
| Emergency Override | Break glass for emergencies | Audit + Warning |
| Revocation | Patient can revoke consent anytime | Immediate |

### 4.2 Emergency Access (Break Glass)

| Attribute | Description |
|-----------|-------------|
| Trigger | Life-threatening emergency |
| Authorization | Physician + Emergency Code |
| Duration | 24 hours (renewable) |
| Audit | Full audit trail required |
| Notification | Patient notified post-emergency |

---

## 5. Privacy Architecture

### 5.1 Privacy Principles

| Principle | Implementation |
|-----------|----------------|
| Data Minimization | Collect only necessary data |
| Purpose Limitation | Use data only for consented purposes |
| Storage Limitation | Retain data only as long as needed |
| Integrity | Protect data from unauthorized changes |
| Confidentiality | Protect data from unauthorized access |
| Accountability | Document all data processing activities |

### 5.2 Data Classification

| Level | Description | Consent Required |
|-------|-------------|------------------|
| Public | Non-sensitive data | No |
| Internal | Organization-internal data | No |
| Confidential | Sensitive health data | Yes |
| Restricted | Highly sensitive data | Explicit Yes |
| Secret | National security data | Special Authorization |

---

## 6. Consent Management APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/consent | POST | Create consent |
| /api/v1/consent/{id} | GET | Get consent |
| /api/v1/consent/{id} | PUT | Update consent |
| /api/v1/consent/{id}/revoke | PUT | Revoke consent |
| /api/v1/consent/patient/{id} | GET | Get patient consents |
| /api/v1/consent/check | GET | Check consent status |
| /api/v1/consent/emergency | POST | Emergency override |
| /api/v1/consent/audit | GET | Get consent audit trail |

---

## 7. Delegation

### 7.1 Delegation Rules

| Rule | Description |
|------|-------------|
| Legal Guardian | Parents/legal guardians for minors |
| Healthcare Proxy | Designated healthcare proxy |
| Power of Attorney | Legal power of attorney |
| Time-limited | Delegation with expiration |
| Scope-limited | Delegation for specific purposes |

---

## 8. Offline Support

| Capability | Implementation |
|------------|----------------|
| Consent Cache | Local cache of consent status |
| Emergency Access | Offline break glass with sync |
| Audit Trail | Local audit with sync on reconnect |
| Conflict Resolution | Latest consent wins |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
