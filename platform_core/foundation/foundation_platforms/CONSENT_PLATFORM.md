# CONSENT PLATFORM

**NHDOS Platform-Core — Foundation Platform 5: Sovereign Consent Engine**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The Consent Platform is the sovereign consent engine for NHDOS, providing patient consent management, guardian consent, emergency override, break glass, delegation, consent revocation, consent expiration, purpose-based access, privacy policies, and consent audit across 44 million citizens and 4,800 healthcare facilities.

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

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONSENT PLATFORM                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Consent     │  │   Purpose    │  │   Emergency  │          │
│  │  Manager     │──▶│   Engine     │──▶│   Override   │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │  Delegation  │  │   Revocation │  │   Audit      │          │
│  │  Engine      │  │   Manager    │  │   Trail      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Consent Lifecycle

### 3.1 Consent States

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

## 4. Consent Types

### 4.1 Consent Categories

| Type | Description | Scope |
|------|-------------|-------|
| Treatment | Consent for medical treatment | Per encounter |
| Data Sharing | Consent to share data with other providers | Per provider |
| Research | Consent for research use | Per study |
| Marketing | Consent for marketing communications | Organization-wide |
| Emergency | Emergency access override | Time-limited |
| Guardian | Consent by legal guardian | Per patient |

### 4.2 Consent Granularity

| Level | Description | Example |
|-------|-------------|---------|
| Global | Consent for all purposes | "Share all my data" |
| Category | Consent for data category | "Share lab results" |
| Specific | Consent for specific data | "Share CBC results from Lab X" |
| Time-limited | Consent with expiration | "Share for 30 days" |

---

## 5. Emergency Access (Break Glass)

### 5.1 Emergency Protocol

| Attribute | Description |
|-----------|-------------|
| Trigger | Life-threatening emergency |
| Authorization | Physician + Emergency Code |
| Duration | 24 hours (renewable) |
| Audit | Full audit trail required |
| Notification | Patient notified post-emergency |

### 5.2 Emergency Override Rules

| Rule | Description | Enforcement |
|------|-------------|-------------|
| Emergency Code Required | Valid emergency code required | Blocking |
| Physician Authorization | Licensed physician required | Blocking |
| Time Limit | 24-hour maximum | Automatic |
| Audit Required | Full audit trail mandatory | Blocking |
| Patient Notification | Notify patient within 24 hours | Automatic |

---

## 6. Delegation

### 6.1 Delegation Rules

| Rule | Description |
|------|-------------|
| Legal Guardian | Parents/legal guardians for minors |
| Healthcare Proxy | Designated healthcare proxy |
| Power of Attorney | Legal power of attorney |
| Time-limited | Delegation with expiration |
| Scope-limited | Delegation for specific purposes |

---

## 7. Consent Policies

### 7.1 Policy Rules

| Rule | Description | Enforcement |
|------|-------------|-------------|
| Explicit Consent Required | Patient must explicitly consent | Blocking |
| Consent Expiry | Consent expires after defined period | Warning |
| Purpose Match | Data use must match consent purpose | Blocking |
| Guardian Consent | Minors require guardian consent | Blocking |
| Emergency Override | Break glass for emergencies | Audit + Warning |
| Revocation | Patient can revoke consent anytime | Immediate |

---

## 8. Privacy Architecture

### 8.1 Privacy Principles

| Principle | Implementation |
|-----------|----------------|
| Data Minimization | Collect only necessary data |
| Purpose Limitation | Use data only for consented purposes |
| Storage Limitation | Retain data only as long as needed |
| Integrity | Protect data from unauthorized changes |
| Confidentiality | Protect data from unauthorized access |
| Accountability | Document all data processing activities |

---

## 9. Consent Management APIs

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
| /api/v1/consent/delegate | POST | Create delegation |
| /api/v1/consent/delegate/{id} | DELETE | Revoke delegation |

---

## 10. Offline Support

| Capability | Implementation |
|------------|----------------|
| Consent Cache | Local cache of consent status |
| Emergency Access | Offline break glass with sync |
| Audit Trail | Local audit with sync on reconnect |
| Conflict Resolution | Latest consent wins |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
