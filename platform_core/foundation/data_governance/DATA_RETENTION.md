# DATA RETENTION

**NHDOS Platform-Core — Data Retention**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS Data Retention policy defines data lifecycle management across all platform services, including retention periods, deletion procedures, and compliance requirements. It ensures regulatory compliance while optimizing storage costs.

---

## 2. Architecture Overview

### 2.1 Data Retention Architecture

```
┌─────────────────────────────────────────────────────────┐
│                Data Retention System                      │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Retention │  │   Deletion  │  │  Archive    │     │
│  │   Policy    │  │   Engine    │  │  Manager    │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │              │
│         └────────┬───────┴────────┬───────┘              │
│                  │                │                       │
│         ┌────────▼────────┐ ┌────▼────────────┐         │
│         │  Policy Store   │ │  Audit Log      │         │
│         │  (PostgreSQL)   │ │  (Elasticsearch) │        │
│         └─────────────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Retention Policies

### 3.1 Data Classification Retention

| Classification | Retention Period | Deletion Method | Legal Basis |
|----------------|------------------|-----------------|-------------|
| Public | No limit | Soft delete | - |
| Internal | 3 years | Soft delete | - |
| Confidential | 5 years | Cryptographic erase | - |
| Restricted | 7 years | Certified deletion | Regulatory |
| PHI | 10 years | Certified deletion | HIPAA |
| Financial | 7 years | Certified deletion | Tax law |

### 3.2 Data Type Retention

| Data Type | Retention | Archive After | Delete After |
|-----------|-----------|---------------|--------------|
| Patient Records | 10 years | 3 years | 10 years |
| Lab Results | 10 years | 3 years | 10 years |
| Prescriptions | 7 years | 2 years | 7 years |
| Appointments | 5 years | 1 year | 5 years |
| Audit Logs | 7 years | 1 year | 7 years |
| System Logs | 90 days | 30 days | 90 days |
| Session Data | 30 days | - | 30 days |

---

## 4. Retention Lifecycle

### 4.1 Lifecycle States

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Active    │───▶│   Archive   │───▶│   Pending   │───▶│   Deleted   │
│             │    │             │    │  Deletion   │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │                  │
       ▼                  ▼                  ▼                  ▼
  Read/Write         Read Only        Confirmation        Permanent
  Full Access        Compressed       Required            Removal
```

### 4.2 Lifecycle Rules

| State | Duration | Access | Storage |
|-------|----------|--------|---------|
| Active | Policy period | Full access | Hot storage |
| Archive | 3 years after active | Read-only | Cold storage |
| Pending Deletion | 30 days | Admin only | Cold storage |
| Deleted | Permanent | None | Removed |

---

## 5. Deletion Procedures

### 5.1 Soft Delete

```python
class SoftDeletion:
    def delete(self, record_id: str, reason: str) -> None:
        # 1. Mark record as deleted
        record = self.get(record_id)
        record.is_deleted = True
        record.deleted_at = datetime.utcnow()
        record.deleted_by = self.current_user
        record.deletion_reason = reason
        
        # 2. Preserve record for retention period
        self.archive(record)
        
        # 3. Log deletion
        self.audit_log.log(
            action="soft_delete",
            record_id=record_id,
            reason=reason
        )
```

### 5.2 Cryptographic Erasure

```python
class CryptographicErasure:
    def erase(self, record_id: str, reason: str) -> None:
        # 1. Get encryption key reference
        key_ref = self.get_encryption_key(record_id)
        
        # 2. Destroy encryption key
        self.key_manager.destroy(key_ref)
        
        # 3. Mark record as unrecoverable
        record = self.get(record_id)
        record.is_erased = True
        record.erased_at = datetime.utcnow()
        
        # 4. Log erasure
        self.audit_log.log(
            action="cryptographic_erasure",
            record_id=record_id,
            key_id=key_ref,
            reason=reason
        )
```

### 5.3 Certified Deletion

```python
class CertifiedDeletion:
    def delete(self, record_id: str, reason: str) -> Certificate:
        # 1. Verify deletion eligibility
        if not self.is_eligible_for_deletion(record_id):
            raise DeletionNotAllowed("Record not eligible")
        
        # 2. Create deletion request
        request = self.create_deletion_request(record_id, reason)
        
        # 3. Execute deletion
        self.execute_deletion(request)
        
        # 4. Generate certificate
        certificate = self.generate_certificate(request)
        
        # 5. Store certificate
        self.store_certificate(certificate)
        
        return certificate
```

---

## 6. APIs

### 6.1 Retention Management API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/retention/policies` | GET | List retention policies |
| `/api/v1/retention/policies/{id}` | GET | Get policy details |
| `/api/v1/retention/records/{id}/status` | GET | Get record retention status |
| `/api/v1/retention/records/{id}/delete` | POST | Request deletion |
| `/api/v1/retention/records/{id}/certificate` | GET | Get deletion certificate |
| `/api/v1/retention/reports/compliance` | GET | Get compliance report |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
