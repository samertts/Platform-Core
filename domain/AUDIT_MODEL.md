# AUDIT MODEL — NATIONAL HEALTHCARE DIGITAL OPERATING SYSTEM

**Document**: Canonical Audit Model
**Version**: 1.0.0
**Date**: 2026-06-25
**Status**: ACTIVE
**Constitution Reference**: Articles V, VI, XII, XV

---

## 1. OVERVIEW

This document defines the comprehensive audit model for the NHDOS. Every entity, relationship, and operation in the system produces an immutable audit record. The audit trail is the foundation of trust, accountability, and regulatory compliance.

**Core Principles**:
- Every mutation produces an audit record
- Audit records are immutable once created
- Audit records are cryptographically chained for tamper detection
- Audit records have defined retention periods
- Audit records are accessible for compliance and investigation
- Audit records cannot be deleted or modified by any user, including administrators

---

## 2. AUDIT EVENT TYPES

### 2.1 CRUD Operations

| Event Type | Description | Entities |
|------------|-------------|----------|
| `entity.created` | New entity created | All entities |
| `entity.read` | Entity accessed | All entities |
| `entity.updated` | Entity modified | All entities |
| `entity.deleted` | Entity removed | All entities |
| `entity.exported` | Entity data exported | Patient, Sample, Test Result |
| `entity.printed` | Entity data printed | Patient, Sample, Test Result, Report |

### 2.2 Authentication Events

| Event Type | Description |
|------------|-------------|
| `auth.login` | Successful login |
| `auth.login_failed` | Failed login attempt |
| `auth.logout` | User logout |
| `auth.session_expired` | Session timeout |
| `auth.password_changed` | Password changed |
| `auth.password_reset` | Password reset requested |
| `auth.mfa_enabled` | MFA enabled |
| `auth.mfa_disabled` | MFA disabled |
| `auth.account_locked` | Account locked |
| `auth.account_unlocked` | Account unlocked |

### 2.3 Authorization Events

| Event Type | Description |
|------------|-------------|
| `auth.access_granted` | Access allowed |
| `auth.access_denied` | Access denied |
| `auth.permission_changed` | User permissions modified |
| `auth.role_assigned` | Role assigned to user |
| `auth.role_removed` | Role removed from user |

### 2.4 Clinical Events

| Event Type | Description |
|------------|-------------|
| `clinical.order_placed` | Test order created |
| `clinical.order_cancelled` | Test order cancelled |
| `clinical.sample_collected` | Sample collected |
| `clinical.sample_received` | Sample received in lab |
| `clinical.sample_rejected` | Sample rejected |
| `clinical.result_recorded` | Test result entered |
| `clinical.result_verified` | Test result verified |
| `clinical.result_corrected` | Test result corrected |
| `clinical.result_released` | Result released to patient/doctor |

### 2.5 System Events

| Event Type | Description |
|------------|-------------|
| `system.config_changed` | Configuration modified |
| `system.user_created` | User account created |
| `system.user_deactivated` | User account deactivated |
| `system.role_created` | Role created |
| `system.role_modified` | Role modified |
| `system.backup_created` | Backup completed |
| `system.backup_restored` | Backup restored |
| `system.migration_executed` | Database migration run |

### 2.6 Security Events

| Event Type | Description |
|------------|-------------|
| `security.vulnerability_found` | Security scan finding |
| `security.policy_violation` | Policy violation detected |
| `security.data_breach` | Data breach detected |
| `security.encryption_key_rotated` | Encryption key rotated |
| `security.certificate_renewed` | Certificate renewed |

---

## 3. ENTITY-SPECIFIC AUDIT REQUIREMENTS

### 3.1 Patient Entity

| Event | Fields Audited | Retention | Legal Requirement |
|-------|---------------|-----------|-------------------|
| `patient.created` | All fields | 10 years | HIPAA, Local |
| `patient.read` | Access metadata | 7 years | HIPAA |
| `patient.updated` | Changed fields | 10 years | HIPAA, Local |
| `patient.deleted` | Soft delete marker | Permanent | Legal hold |
| `patient.exported` | Export metadata | 10 years | HIPAA |
| `patient.merged` | Merge details | Permanent | Clinical safety |

**Audit Record Example**:
```json
{
  "eventId": "audit-uuid-001",
  "eventType": "patient.created",
  "timestamp": "2026-06-25T10:00:00Z",
  "entity": {
    "type": "patient",
    "id": "patient-uuid",
    "identifier": "MRN-2026-0001"
  },
  "actor": {
    "userId": "user-uuid",
    "username": "ahmed.rashid",
    "role": "registration",
    "facility": "facility-uuid"
  },
  "changes": {
    "firstName": {"from": null, "to": "Ahmed"},
    "lastName": {"from": null, "to": "Al-Rashid"},
    "medicalRecordNumber": {"from": null, "to": "MRN-2026-0001"}
  },
  "context": {
    "ipAddress": "10.0.0.1",
    "userAgent": "Mozilla/5.0...",
    "correlationId": "corr-uuid",
    "requestId": "req-uuid"
  },
  "integrity": {
    "hash": "sha256:abc123...",
    "previousHash": "sha256:def456...",
    "sequenceNumber": 12345
  }
}
```

### 3.2 Sample Entity

| Event | Fields Audited | Retention | Legal Requirement |
|-------|---------------|-----------|-------------------|
| `sample.created` | All fields | 10 years | Clinical, ISO 15189 |
| `sample.read` | Access metadata | 7 years | ISO 15189 |
| `sample.updated` | Changed fields | 10 years | Clinical, ISO 15189 |
| `sample.status_changed` | Status transition | 10 years | Clinical, ISO 15189 |
| `sample.rejected` | Rejection reason | 10 years | Clinical |
| `sample.destroyed` | Destruction record | Permanent | Legal hold |

### 3.3 Test Result Entity

| Event | Fields Audited | Retention | Legal Requirement |
|-------|---------------|-----------|-------------------|
| `result.created` | All fields | 10 years | Clinical, ISO 15189 |
| `result.read` | Access metadata | 10 years | Clinical |
| `result.updated` | Changed fields | 10 years | Clinical, ISO 15189 |
| `result.verified` | Verification details | 10 years | Clinical, ISO 15189 |
| `result.corrected` | Correction details | Permanent | Clinical, Legal |
| `result.released` | Release metadata | 10 years | Clinical |
| `result.amended` | Amendment details | Permanent | Clinical, Legal |

### 3.4 Audit Event Entity (Meta-Audit)

| Event | Fields Audited | Retention | Legal Requirement |
|-------|---------------|-----------|-------------------|
| `audit.read` | Access metadata | Permanent | Compliance |
| `audit.exported` | Export metadata | Permanent | Compliance |
| `audit.tamper_detected` | Tamper details | Permanent | Security |

---

## 4. AUDIT RECORD STRUCTURE

### 4.1 Immutable Audit Record

```python
@dataclass(frozen=True)
class AuditRecord:
    """Immutable audit record."""
    event_id: str
    event_type: str
    timestamp: str
    entity_type: str
    entity_id: str
    actor_id: str
    actor_username: str
    actor_roles: list
    actor_facility: str
    action: str
    changes: dict
    context: dict
    integrity: dict
    metadata: dict
```

### 4.2 Audit Record Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AuditRecord",
  "type": "object",
  "required": [
    "eventId",
    "eventType",
    "timestamp",
    "entity",
    "actor",
    "action",
    "integrity"
  ],
  "properties": {
    "eventId": {
      "type": "string",
      "format": "uuid",
      "description": "Unique audit event identifier"
    },
    "eventType": {
      "type": "string",
      "enum": [
        "entity.created", "entity.read", "entity.updated", "entity.deleted",
        "entity.exported", "entity.printed",
        "auth.login", "auth.login_failed", "auth.logout",
        "clinical.order_placed", "clinical.sample_collected",
        "clinical.result_recorded", "clinical.result_verified",
        "system.config_changed", "system.user_created",
        "security.vulnerability_found", "security.policy_violation"
      ]
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Event timestamp in ISO 8601 format"
    },
    "entity": {
      "type": "object",
      "required": ["type", "id"],
      "properties": {
        "type": {"type": "string"},
        "id": {"type": "string", "format": "uuid"},
        "identifier": {"type": "string"},
        "classification": {"type": "string"}
      }
    },
    "actor": {
      "type": "object",
      "required": ["userId", "username"],
      "properties": {
        "userId": {"type": "string", "format": "uuid"},
        "username": {"type": "string"},
        "roles": {"type": "array", "items": {"type": "string"}},
        "facility": {"type": "string", "format": "uuid"},
        "department": {"type": "string"},
        "ipAddress": {"type": "string"},
        "userAgent": {"type": "string"},
        "sessionId": {"type": "string", "format": "uuid"}
      }
    },
    "action": {
      "type": "string",
      "enum": ["create", "read", "update", "delete", "export", "print", "verify", "approve"]
    },
    "changes": {
      "type": "object",
      "description": "Field-level changes",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "from": {},
          "to": {}
        }
      }
    },
    "context": {
      "type": "object",
      "properties": {
        "correlationId": {"type": "string", "format": "uuid"},
        "requestId": {"type": "string", "format": "uuid"},
        "facility": {"type": "string", "format": "uuid"},
        "department": {"type": "string"},
        "source": {"type": "string"}
      }
    },
    "integrity": {
      "type": "object",
      "required": ["hash", "sequenceNumber"],
      "properties": {
        "hash": {"type": "string"},
        "previousHash": {"type": "string"},
        "sequenceNumber": {"type": "integer"},
        "algorithm": {"type": "string", "default": "SHA-256"}
      }
    },
    "metadata": {
      "type": "object",
      "description": "Additional metadata"
    }
  }
}
```

### 4.3 Hash Chain Structure

```
Record N-1                    Record N                    Record N+1
┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
│ eventId: abc    │          │ eventId: def    │          │ eventId: ghi    │
│ timestamp: T1   │          │ timestamp: T2   │          │ timestamp: T3   │
│ hash: H1        │◄─────────│ previousHash: H1│◄─────────│ previousHash: H2│
│ previousHash: H0│          │ hash: H2        │          │ hash: H3        │
└─────────────────┘          └─────────────────┘          └─────────────────┘
```

---

## 5. IMMUTABLE AUDIT RECORDS

### 5.1 Immutability Guarantees

| Guarantee | Implementation | Verification |
|-----------|---------------|--------------|
| No modification | Append-only storage | Hash verification |
| No deletion | Permanent retention | Backup verification |
| No reordering | Sequence numbers | Chain verification |
| Tamper detection | Hash chain | Periodic verification |

### 5.2 Storage Implementation

```python
class ImmutableAuditStore:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def append(self, record: AuditRecord) -> dict:
        """Append audit record (never update or delete)."""
        # Get previous hash
        previous_record = self.get_latest_record()
        previous_hash = previous_record["integrity"]["hash"] if previous_record else "0" * 64
        
        # Compute hash
        record_dict = asdict(record)
        record_dict["integrity"]["previousHash"] = previous_hash
        record_dict["integrity"]["hash"] = self.compute_hash(record_dict)
        record_dict["integrity"]["sequenceNumber"] = self.get_next_sequence()
        
        # Insert (append only)
        self.db.execute("""
            INSERT INTO audit_events (
                event_id, event_type, timestamp, entity_type, entity_id,
                actor_id, actor_username, actor_roles, actor_facility,
                action, changes, context, integrity, metadata
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, self.serialize_record(record_dict))
        
        return {"success": True, "eventId": record.event_id}
    
    def verify_chain(self, from_sequence: int = 0, to_sequence: int = None) -> dict:
        """Verify audit chain integrity."""
        records = self.get_records_range(from_sequence, to_sequence)
        
        for i in range(1, len(records)):
            current = records[i]
            previous = records[i-1]
            
            # Verify previous hash link
            if current["integrity"]["previousHash"] != previous["integrity"]["hash"]:
                return {
                    "valid": False,
                    "error": f"Chain broken at sequence {current['integrity']['sequenceNumber']}",
                    "expected": previous["integrity"]["hash"],
                    "actual": current["integrity"]["previousHash"]
                }
            
            # Verify current hash
            computed_hash = self.compute_hash(current)
            if current["integrity"]["hash"] != computed_hash:
                return {
                    "valid": False,
                    "error": f"Hash mismatch at sequence {current['integrity']['sequenceNumber']}",
                    "expected": computed_hash,
                    "actual": current["integrity"]["hash"]
                }
        
        return {"valid": True, "recordsVerified": len(records)}
```

### 5.3 Tamper Detection

```python
class TamperDetector:
    def __init__(self, audit_store: ImmutableAuditStore):
        self.store = audit_store
    
    def detect_tampering(self) -> dict:
        """Detect any tampering in audit chain."""
        # Verify full chain
        chain_result = self.store.verify_chain()
        
        if not chain_result["valid"]:
            return {
                "tamperingDetected": True,
                "type": "chain_broken",
                "details": chain_result,
                "severity": "critical",
                "action": "IMMEDIATE_INVESTIGATION"
            }
        
        # Check for missing sequence numbers
        gaps = self.detect_sequence_gaps()
        if gaps:
            return {
                "tamperingDetected": True,
                "type": "sequence_gaps",
                "details": {"gaps": gaps},
                "severity": "high",
                "action": "INVESTIGATE_GAPS"
            }
        
        # Check for timestamps out of order
        anomalies = self.detect_timestamp_anomalies()
        if anomalies:
            return {
                "tamperingDetected": True,
                "type": "timestamp_anomaly",
                "details": {"anomalies": anomalies},
                "severity": "medium",
                "action": "REVIEW_ANOMALIES"
            }
        
        return {"tamperingDetected": False}
    
    def detect_sequence_gaps(self) -> list:
        """Detect gaps in sequence numbers."""
        max_sequence = self.store.get_max_sequence()
        existing_sequences = self.store.get_all_sequence_numbers()
        
        expected = set(range(1, max_sequence + 1))
        actual = set(existing_sequences)
        
        gaps = sorted(expected - actual)
        return gaps
    
    def detect_timestamp_anomalies(self) -> list:
        """Detect timestamps out of order."""
        records = self.store.get_recent_records(1000)
        anomalies = []
        
        for i in range(1, len(records)):
            if records[i]["timestamp"] < records[i-1]["timestamp"]:
                anomalies.append({
                    "sequenceA": records[i-1]["integrity"]["sequenceNumber"],
                    "sequenceB": records[i]["integrity"]["sequenceNumber"],
                    "timestampA": records[i-1]["timestamp"],
                    "timestampB": records[i]["timestamp"]
                })
        
        return anomalies
```

---

## 6. RETENTION POLICIES

### 6.1 Retention Periods by Entity

| Entity | Retention Period | Legal Basis | Disposition |
|--------|-----------------|-------------|-------------|
| Patient | 10 years after last encounter | HIPAA, Local law | Archive |
| Sample | 10 years after analysis | ISO 15189, Clinical | Archive |
| Test Result | 10 years after verification | ISO 15189, Clinical | Archive |
| Test Order | 10 years after completion | Clinical | Archive |
| Audit Event | 7 years | Compliance | Archive |
| User | 7 years after termination | Labor law | Archive |
| Credential | 7 years after expiry | Professional | Archive |
| Correspondence | 7 years | Government | Archive |
| Configuration | 3 years | Operational | Delete |
| Notification | 1 year | Operational | Delete |
| Telemetry | 1 year | Operational | Delete |
| Report | 7 years | Compliance | Archive |

### 6.2 Retention Policy Implementation

```python
from datetime import datetime, timedelta

class RetentionPolicy:
    POLICIES = {
        "patient": {"years": 10, "disposition": "archive"},
        "sample": {"years": 10, "disposition": "archive"},
        "test_result": {"years": 10, "disposition": "archive"},
        "test_order": {"years": 10, "disposition": "archive"},
        "audit_event": {"years": 7, "disposition": "archive"},
        "user": {"years": 7, "disposition": "archive"},
        "credential": {"years": 7, "disposition": "archive"},
        "correspondence": {"years": 7, "disposition": "archive"},
        "configuration": {"years": 3, "disposition": "delete"},
        "notification": {"years": 1, "disposition": "delete"},
        "telemetry": {"years": 1, "disposition": "delete"},
        "report": {"years": 7, "disposition": "archive"}
    }
    
    def get_retention_date(self, entity_type: str, entity_created_at: str) -> dict:
        """Calculate retention date for an entity."""
        policy = self.POLICIES.get(entity_type, {"years": 7, "disposition": "archive"})
        
        created = datetime.fromisoformat(entity_created_at)
        retention_date = created + timedelta(days=policy["years"] * 365)
        
        return {
            "entityType": entity_type,
            "createdAt": entity_created_at,
            "retentionYears": policy["years"],
            "retentionDate": retention_date.isoformat(),
            "disposition": policy["disposition"],
            "daysRemaining": (retention_date - datetime.now(timezone.utc)).days
        }
    
    def get_expired_entities(self) -> list:
        """Get entities that have exceeded retention period."""
        expired = []
        
        for entity_type, policy in self.POLICIES.items():
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=policy["years"] * 365)
            
            entities = self.get_entities_before_date(entity_type, cutoff_date)
            for entity in entities:
                expired.append({
                    "entityType": entity_type,
                    "entityId": entity["id"],
                    "createdAt": entity["createdAt"],
                    "disposition": policy["disposition"]
                })
        
        return expired
```

### 6.3 Retention Schedule

| Retention Period | Records Affected | Archive Location |
|-----------------|------------------|------------------|
| 1 year | Notifications, Telemetry | Cold storage |
| 3 years | Configuration | Cold storage |
| 7 years | Audit Events, User, Credential, Correspondence, Report | Archive storage |
| 10 years | Patient, Sample, Test Result, Test Order | Long-term archive |
| Permanent | Legal holds, Critical audit events | Permanent archive |

### 6.4 Archive Process

```python
class ArchiveManager:
    def archive_expired_records(self) -> dict:
        """Archive records that have exceeded retention period."""
        retention_manager = RetentionPolicy()
        expired = retention_manager.get_expired_entities()
        
        archived_count = 0
        errors = []
        
        for item in expired:
            try:
                if item["disposition"] == "archive":
                    self.archive_entity(item)
                    archived_count += 1
                elif item["disposition"] == "delete":
                    self.secure_delete_entity(item)
                    archived_count += 1
            except Exception as e:
                errors.append({
                    "entity": item,
                    "error": str(e)
                })
        
        return {
            "archivedCount": archived_count,
            "errorCount": len(errors),
            "errors": errors,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def archive_entity(self, item: dict):
        """Archive an entity to cold storage."""
        # Export entity data
        entity_data = self.export_entity(item["entityType"], item["entityId"])
        
        # Compress
        compressed = self.compress(entity_data)
        
        # Store in archive
        archive_location = self.store_in_archive(compressed, item)
        
        # Log archival
        self.log_archival(item, archive_location)
    
    def secure_delete_entity(self, item: dict):
        """Securely delete entity data."""
        # Overwrite data multiple times
        self.overwrite_data(item["entityId"], passes=3)
        
        # Delete record
        self.delete_record(item["entityId"])
        
        # Log deletion
        self.log_deletion(item)
```

---

## 7. LEGAL REQUIREMENTS

### 7.1 Legal Hold

When litigation or investigation is pending, entities cannot be deleted or archived:

```python
class LegalHoldManager:
    def __init__(self):
        self.holds = {}
    
    def place_hold(self, entity_type: str, entity_id: str, reason: str, 
                   placed_by: str, case_reference: str) -> dict:
        """Place legal hold on entity."""
        hold_id = str(uuid.uuid4())
        
        self.holds[hold_id] = {
            "holdId": hold_id,
            "entityType": entity_type,
            "entityId": entity_id,
            "reason": reason,
            "placedBy": placed_by,
            "caseReference": case_reference,
            "placedAt": datetime.now(timezone.utc).isoformat(),
            "expiresAt": None,  # Manual release only
            "status": "active"
        }
        
        return self.holds[hold_id]
    
    def check_hold(self, entity_type: str, entity_id: str) -> bool:
        """Check if entity has active legal hold."""
        for hold in self.holds.values():
            if (hold["entityType"] == entity_type and 
                hold["entityId"] == entity_id and
                hold["status"] == "active"):
                return True
        return False
    
    def release_hold(self, hold_id: str, released_by: str) -> dict:
        """Release legal hold."""
        if hold_id in self.holds:
            self.holds[hold_id]["status"] = "released"
            self.holds[hold_id]["releasedBy"] = released_by
            self.holds[hold_id]["releasedAt"] = datetime.now(timezone.utc).isoformat()
            return {"released": True}
        return {"released": False, "error": "Hold not found"}
```

### 7.2 Regulatory Requirements Matrix

| Regulation | Audit Required | Retention | Access Log | Export Log | Tamper Detection |
|------------|---------------|-----------|------------|------------|------------------|
| HIPAA | Yes | 6 years | Yes | Yes | Recommended |
| GDPR | Yes | Variable | Yes | Yes | Recommended |
| ISO 15189 | Yes | 10 years | Yes | Yes | Required |
| NIST 800-53 | Yes | 3 years | Yes | Yes | Required |
| SOX | Yes | 7 years | Yes | Yes | Required |
| Local (Iraq) | Yes | 10 years | Yes | Yes | Required |

### 7.3 Data Subject Rights (GDPR)

```python
class GDPRAuditManager:
    def log_data_subject_request(self, request_type: str, subject_id: str, 
                                  requested_by: str) -> dict:
        """Log GDPR data subject request."""
        event = {
            "eventType": "gdpr.request_received",
            "requestType": request_type,  # access, rectification, erasure, portability
            "subjectId": subject_id,
            "requestedBy": requested_by,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "received",
            "deadline": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
        }
        
        return self.audit_store.append(event)
    
    def log_data_erasure(self, subject_id: str, erasure_type: str,
                         performed_by: str) -> dict:
        """Log GDPR data erasure (right to be forgotten)."""
        # Check for legal holds
        if self.legal_hold_manager.check_hold("patient", subject_id):
            return {"success": False, "error": "Entity has legal hold"}
        
        # Check for retention requirements
        if self.retention_manager.has_active_retention("patient", subject_id):
            return {"success": False, "error": "Retention period not expired"}
        
        event = {
            "eventType": "gdpr.data_erased",
            "subjectId": subject_id,
            "erasureType": erasure_type,  # full, partial
            "performedBy": performed_by,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        return self.audit_store.append(event)
```

---

## 8. AUDIT TRAIL STRUCTURE

### 8.1 Audit Trail Components

```
┌─────────────────────────────────────────────────────────────────┐
│                      AUDIT TRAIL ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    EVENT SOURCES                            │ │
│  │  API Gateway │ Application │ Database │ External Systems    │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                            │                                      │
│                            ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                 AUDIT EVENT COLLECTOR                       │ │
│  │  Validation │ Enrichment │ Deduplication │ Routing          │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                            │                                      │
│                            ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                 AUDIT EVENT STORE                           │ │
│  │  PostgreSQL │ Immutable │ Hash-Chained │ Indexed            │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                            │                                      │
│              ┌─────────────┼─────────────┐                       │
│              ▼             ▼             ▼                        │
│  ┌────────────────┐ ┌──────────────┐ ┌────────────────┐         │
│  │  Real-time     │ │  Compliance  │ │  Investigation │         │
│  │  Monitoring    │ │  Reporting   │ │  Dashboard     │         │
│  └────────────────┘ └──────────────┘ └────────────────┘         │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Audit Event Collection

```python
class AuditEventCollector:
    def __init__(self, audit_store: ImmutableAuditStore):
        self.store = audit_store
        self.validators = []
        self.enrichers = []
    
    async def collect(self, event: dict) -> dict:
        """Collect and process audit event."""
        # Validate event
        for validator in self.validators:
            if not validator.validate(event):
                return {"success": False, "error": "Validation failed"}
        
        # Enrich event
        enriched_event = event.copy()
        for enricher in self.enrichers:
            enriched_event = enricher.enrich(enriched_event)
        
        # Store
        result = self.store.append(enriched_event)
        
        # Notify listeners
        await self.notify_listeners(enriched_event)
        
        return result
    
    async def notify_listeners(self, event: dict):
        """Notify audit event listeners."""
        # Real-time monitoring
        if event.get("severity") in ("critical", "high"):
            await self.alert_security_team(event)
        
        # Compliance reporting
        await self.update_compliance_dashboard(event)
```

### 8.3 Audit Event Enrichment

```python
class AuditEventEnricher:
    def enrich(self, event: dict) -> dict:
        """Enrich audit event with additional context."""
        # Add geolocation
        if "ipAddress" in event.get("actor", {}):
            event["actor"]["geoLocation"] = self.get_geolocation(
                event["actor"]["ipAddress"]
            )
        
        # Add user details
        if "userId" in event.get("actor", {}):
            user = self.get_user_details(event["actor"]["userId"])
            event["actor"]["department"] = user.get("department")
            event["actor"]["clearanceLevel"] = user.get("clearanceLevel")
        
        # Add entity classification
        if "entity" in event:
            classification = self.get_entity_classification(
                event["entity"]["type"]
            )
            event["entity"]["classification"] = classification
        
        # Add risk score
        event["metadata"] = event.get("metadata", {})
        event["metadata"]["riskScore"] = self.calculate_risk_score(event)
        
        return event
    
    def calculate_risk_score(self, event: dict) -> float:
        """Calculate risk score for audit event."""
        score = 0.0
        
        # High-risk actions
        high_risk_actions = ["delete", "export", "print"]
        if event.get("action") in high_risk_actions:
            score += 0.3
        
        # Sensitive entities
        sensitive_entities = ["patient", "test_result", "audit_event"]
        if event.get("entity", {}).get("type") in sensitive_entities:
            score += 0.3
        
        # After hours access
        timestamp = datetime.fromisoformat(event.get("timestamp", ""))
        if timestamp.hour < 7 or timestamp.hour > 19:
            score += 0.2
        
        # Failed operations
        if event.get("result", {}).get("status") == "failure":
            score += 0.2
        
        return min(score, 1.0)
```

---

## 9. TAMPER DETECTION

### 9.1 Tamper Detection Methods

| Method | Description | Frequency | Alert Level |
|--------|-------------|-----------|-------------|
| Hash Chain Verification | Verify sequential hash chain | Every 5 minutes | Critical |
| Sequence Gap Detection | Detect missing sequence numbers | Every hour | High |
| Timestamp Anomaly | Detect out-of-order timestamps | Every hour | Medium |
| Storage Integrity | Verify storage hasn't been modified | Daily | Critical |
| Backup Verification | Verify backups against live data | Weekly | High |

### 9.2 Tamper Detection Implementation

```python
class TamperDetectionService:
    def __init__(self, audit_store: ImmutableAuditStore):
        self.store = audit_store
    
    async def run_full_scan(self) -> dict:
        """Run comprehensive tamper detection scan."""
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "checks": []
        }
        
        # Check 1: Hash chain integrity
        chain_result = await self.check_hash_chain()
        results["checks"].append(chain_result)
        
        # Check 2: Sequence gaps
        gap_result = await self.check_sequence_gaps()
        results["checks"].append(gap_result)
        
        # Check 3: Timestamp anomalies
        timestamp_result = await self.check_timestamp_anomalies()
        results["checks"].append(timestamp_result)
        
        # Check 4: Storage integrity
        storage_result = await self.check_storage_integrity()
        results["checks"].append(storage_result)
        
        # Check 5: Backup verification
        backup_result = await self.check_backup_integrity()
        results["checks"].append(backup_result)
        
        # Determine overall status
        results["overallStatus"] = "secure" if all(
            check["passed"] for check in results["checks"]
        ) else "compromised"
        
        # Generate alerts if needed
        if results["overallStatus"] == "compromised":
            await self.generate_security_alert(results)
        
        return results
    
    async def check_hash_chain(self) -> dict:
        """Check hash chain integrity."""
        try:
            result = self.store.verify_chain()
            return {
                "check": "hash_chain",
                "passed": result["valid"],
                "recordsChecked": result.get("recordsVerified", 0),
                "error": result.get("error")
            }
        except Exception as e:
            return {
                "check": "hash_chain",
                "passed": False,
                "error": str(e)
            }
    
    async def check_sequence_gaps(self) -> dict:
        """Check for sequence number gaps."""
        max_seq = self.store.get_max_sequence()
        existing_seqs = self.store.get_all_sequence_numbers()
        
        expected = set(range(1, max_seq + 1))
        actual = set(existing_seqs)
        gaps = sorted(expected - actual)
        
        return {
            "check": "sequence_gaps",
            "passed": len(gaps) == 0,
            "gapsFound": gaps,
            "gapCount": len(gaps)
        }
    
    async def generate_security_alert(self, results: dict):
        """Generate security alert for tamper detection."""
        failed_checks = [c for c in results["checks"] if not c["passed"]]
        
        alert = {
            "alertType": "tamper_detection",
            "severity": "critical",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": {
                "failedChecks": failed_checks,
                "overallStatus": results["overallStatus"]
            },
            "actions": [
                "IMMEDIATE_INVESTIGATION_REQUIRED",
                "PRESERVE_EVIDENCE",
                "NOTIFY_SECURITY_TEAM"
            ]
        }
        
        await self.send_alert(alert)
```

### 9.3 Tamper Evidence

```python
class TamperEvidence:
    def __init__(self):
        self.evidence_store = []
    
    def collect_evidence(self, tamper_result: dict) -> dict:
        """Collect evidence of tampering."""
        evidence = {
            "evidenceId": str(uuid.uuid4()),
            "collectedAt": datetime.now(timezone.utc).isoformat(),
            "tamperResult": tamper_result,
            "systemState": self.capture_system_state(),
            "hashSnapshots": self.capture_hash_snapshots(),
            "storageMetadata": self.capture_storage_metadata()
        }
        
        self.evidence_store.append(evidence)
        return evidence
    
    def capture_system_state(self) -> dict:
        """Capture current system state."""
        return {
            "hostname": socket.gethostname(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "processId": os.getpid(),
            "environment": os.environ.get("DEPLOYMENT_ENV", "unknown")
        }
    
    def capture_hash_snapshots(self) -> dict:
        """Capture hash snapshots for comparison."""
        return {
            "auditStoreHash": self.get_audit_store_hash(),
            "databaseHash": self.get_database_hash(),
            "backupHash": self.get_backup_hash()
        }
```

---

## 10. AUDIT REPORTING

### 10.1 Compliance Reports

| Report | Frequency | Purpose | Retention |
|--------|-----------|---------|-----------|
| Access Summary | Daily | User access patterns | 1 year |
| Modification Summary | Daily | Data change tracking | 1 year |
| Security Events | Real-time | Security incident tracking | 3 years |
| Compliance Dashboard | Weekly | Regulatory compliance | 7 years |
| Annual Audit Report | Annual | Comprehensive audit summary | Permanent |

### 10.2 Audit Dashboard Metrics

```python
class AuditDashboard:
    def get_metrics(self, time_range: dict) -> dict:
        """Get audit dashboard metrics."""
        return {
            "totalEvents": self.count_events(time_range),
            "eventsByType": self.count_by_type(time_range),
            "eventsByEntity": self.count_by_entity(time_range),
            "eventsByActor": self.count_by_actor(time_range),
            "highRiskEvents": self.count_high_risk(time_range),
            "failedOperations": self.count_failures(time_range),
            "averageResponseTime": self.get_avg_response_time(time_range),
            "complianceScore": self.calculate_compliance_score(time_range),
            "tamperDetections": self.count_tamper_detections(time_range)
        }
    
    def generate_compliance_report(self, period: str) -> dict:
        """Generate compliance report."""
        metrics = self.get_metrics(self.get_period_range(period))
        
        return {
            "reportType": "compliance",
            "period": period,
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "totalAuditEvents": metrics["totalEvents"],
                "securityEvents": metrics["highRiskEvents"],
                "complianceScore": metrics["complianceScore"],
                "tamperDetections": metrics["tamperDetections"]
            },
            "details": {
                "accessPatterns": metrics["eventsByType"],
                "entityActivity": metrics["eventsByEntity"],
                "userActivity": metrics["eventsByActor"]
            },
            "recommendations": self.generate_recommendations(metrics)
        }
```

---

## 11. AUDIT API ENDPOINTS

### 11.1 Audit Event Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/audit-events` | GET | List audit events |
| `/api/v1/audit-events/{id}` | GET | Get audit event |
| `/api/v1/audit-events/search` | POST | Search audit events |
| `/api/v1/audit-events/export` | POST | Export audit events |
| `/api/v1/audit-events/verify` | POST | Verify audit chain |

### 11.2 Compliance Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/compliance/dashboard` | GET | Get compliance dashboard |
| `/api/v1/compliance/report` | POST | Generate compliance report |
| `/api/v1/compliance/verify` | POST | Verify compliance status |

### 11.3 Tamper Detection Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/audit/tamper-scan` | POST | Run tamper detection scan |
| `/api/v1/audit/tamper-status` | GET | Get tamper detection status |
| `/api/v1/audit/evidence` | GET | Get tamper evidence |

---

*Document generated as part of NHDOS Canonical Domain Model*
*Audit model defined for all entities*
*Constitution Reference: Articles V, VI, XII, XV*
*Last Updated: 2026-06-25*
