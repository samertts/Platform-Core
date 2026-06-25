# ARCHIVING POLICY

**NHDOS Platform-Core — Archiving Policy**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS Archiving Policy defines procedures for moving inactive data to cost-effective storage while maintaining accessibility for compliance and audit purposes. It establishes archiving schedules, storage tiers, and retrieval procedures.

---

## 2. Architecture Overview

### 2.1 Archiving Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Archiving System                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Archive   │  │   Storage   │  │  Retrieval  │     │
│  │   Manager   │  │   Tiering   │  │   Service   │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │              │
│         └────────┬───────┴────────┬───────┘              │
│                  │                │                       │
│         ┌────────▼────────┐ ┌────▼────────────┐         │
│         │  Archive Store  │ │  Metadata Index │         │
│         │  (S3/Glacier)   │ │  (Elasticsearch)│         │
│         └─────────────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Storage Tiers

| Tier | Storage Type | Access Time | Cost | Use Case |
|------|--------------|-------------|------|----------|
| Hot | SSD/NVMe | Milliseconds | $$$ | Active data |
| Warm | HDD | Seconds | $$ | Recent archive |
| Cold | Object Storage | Minutes | $ | Long-term archive |
| Deep Archive | Glacier | Hours | ¢ | Compliance |

---

## 3. Archiving Rules

### 3.1 Archive Triggers

| Trigger | Condition | Action |
|---------|-----------|--------|
| Time-based | Inactive > 90 days | Move to Warm |
| Time-based | Inactive > 1 year | Move to Cold |
| Time-based | Inactive > 3 years | Move to Deep Archive |
| Size-based | Database > 80% capacity | Archive oldest data |
| Compliance | Retention period met | Archive per policy |

### 3.2 Archive Schedule

| Data Type | Archive After | Storage Tier | Retrieval SLA |
|-----------|---------------|--------------|---------------|
| Patient Records | 3 years | Cold | 4 hours |
| Lab Results | 3 years | Cold | 4 hours |
| Prescriptions | 2 years | Cold | 4 hours |
| Appointments | 1 year | Warm | 1 hour |
| Audit Logs | 1 year | Cold | 4 hours |
| System Logs | 30 days | Warm | 1 hour |

---

## 4. Archive Process

### 4.1 Archive Workflow

```
1. Identify eligible records
   - Last access > threshold
   - Not in active transaction
   - Meets archive criteria

2. Prepare for archival
   - Compress data
   - Generate checksums
   - Create metadata index

3. Move to storage tier
   - Upload to target storage
   - Verify upload integrity
   - Update metadata store

4. Update source system
   - Mark as archived
   - Remove from active storage
   - Maintain reference pointer

5. Verify and log
   - Verify archive integrity
   - Log archive operation
   - Update audit trail
```

### 4.2 Archive Implementation

```python
class ArchiveManager:
    def archive(self, record_id: str, target_tier: str) -> ArchiveResult:
        # 1. Get record
        record = self.get_record(record_id)
        
        # 2. Validate eligibility
        if not self.is_eligible(record):
            raise ArchiveNotAllowed("Record not eligible")
        
        # 3. Prepare archive
        archive_data = self.prepare_archive(record)
        
        # 4. Upload to storage
        storage_location = self.upload_to_storage(
            archive_data, 
            target_tier
        )
        
        # 5. Update metadata
        self.update_metadata(
            record_id=record_id,
            archive_location=storage_location,
            archive_tier=target_tier
        )
        
        # 6. Mark source as archived
        self.mark_archived(record_id)
        
        return ArchiveResult(
            record_id=record_id,
            location=storage_location,
            tier=target_tier
        )
```

---

## 5. Retrieval Process

### 5.1 Retrieval Methods

| Method | Use Case | SLA | Cost |
|--------|----------|-----|------|
| Standard | Normal requests | 4 hours | Low |
| Bulk | Large datasets | 12 hours | Lowest |
| Expedited | Urgent requests | 5 minutes | High |

### 5.2 Retrieval Implementation

```python
class ArchiveRetriever:
    def retrieve(self, record_id: str, priority: str = "standard") -> Record:
        # 1. Check metadata store
        metadata = self.get_metadata(record_id)
        
        if not metadata:
            raise RecordNotFound("Record not in archive")
        
        # 2. Initiate retrieval
        retrieval_job = self.initiate_retrieval(
            location=metadata.archive_location,
            priority=priority
        )
        
        # 3. Wait for completion
        self.wait_for_completion(retrieval_job)
        
        # 4. Download and restore
        record = self.download_and_restore(retrieval_job)
        
        # 5. Log retrieval
        self.audit_log.log(
            action="archive_retrieval",
            record_id=record_id,
            priority=priority
        )
        
        return record
```

---

## 6. APIs

### 6.1 Archive Management API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/archive/jobs` | GET | List archive jobs |
| `/api/v1/archive/jobs` | POST | Create archive job |
| `/api/v1/archive/jobs/{id}` | GET | Get job status |
| `/api/v1/archive/records/{id}/retrieve` | POST | Retrieve record |
| `/api/v1/archive/storage/usage` | GET | Get storage usage |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
