# OFFLINE DOMAIN MODEL — NATIONAL HEALTHCARE DIGITAL OPERATING SYSTEM

**Document**: Canonical Offline Behavior Model
**Version**: 1.0.0
**Date**: 2026-06-25
**Status**: ACTIVE
**Constitution Reference**: Articles I, V, VIII, XIV

---

## 1. OVERVIEW

The NHDOS operates in environments with unreliable or no internet connectivity. This document defines the canonical offline behavior model that ensures data integrity, consistency, and operational continuity when the system is disconnected from the central server.

**Core Principles**:
- The system must be fully functional offline
- Data created offline must sync reliably when connectivity returns
- Conflict resolution must be deterministic and auditable
- No data loss is acceptable during offline/online transitions
- Offline operations are first-class citizens, not degraded mode

---

## 2. OFFLINE ARCHITECTURE

### 2.1 Node Types

| Node Type | Description | Storage | Sync Role |
|-----------|-------------|---------|-----------|
| **Primary Server** | Central NHDOS server | PostgreSQL + Redis | Source of truth |
| **Facility Node** | Lab/hospital local server | PostgreSQL (embedded) | Regional cache |
| **Desktop Node** | Workstation application | SQLite | Local cache |
| **Mobile Node** | PWA/Capacitor application | IndexedDB + SQLite | Local cache |
| **Edge Node** | IoT/device gateway | SQLite | Device cache |

### 2.2 Data Partitioning

Each node is responsible for a subset of data based on its role:

| Node Type | Data Scope | Sync Direction |
|-----------|-----------|----------------|
| Primary Server | All data | Bidirectional |
| Facility Node | Facility-specific data | Bidirectional |
| Desktop Node | User's assigned data | Bidirectional |
| Mobile Node | User's assigned data | Bidirectional |
| Edge Node | Device-specific data | Upload only |

### 2.3 Offline Storage Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    OFFLINE NODE                          │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │                 APPLICATION LAYER                  │  │
│  │  ┌─────────────┐  ┌─────────────┐                │  │
│  │  │  Business   │  │   Offline   │                │  │
│  │  │   Logic     │  │   Manager   │                │  │
│  │  └──────┬──────┘  └──────┬──────┘                │  │
│  │         │                 │                        │  │
│  └─────────┼─────────────────┼────────────────────────┘  │
│            │                 │                            │
│  ┌─────────▼─────────────────▼────────────────────────┐  │
│  │                 DATA ACCESS LAYER                   │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │  │
│  │  │  Local DB   │  │    Sync     │  │  Conflict │  │  │
│  │  │  (SQLite)   │  │   Queue     │  │  Resolver │  │  │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │                 SYNC LAYER                         │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │  │
│  │  │  Transport  │  │  Protocol   │  │  Queue    │  │  │
│  │  │  (HTTP/WS)  │  │  Handler    │  │  Manager  │  │  │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. OFFLINE CREATION PATTERNS

### 3.1 Entity Creation in Offline Mode

When creating entities offline, the system follows these patterns:

#### 3.1.1 UUID Generation

Offline nodes generate UUIDv4 identifiers locally. No central coordination is required.

```python
import uuid

def generate_offline_id() -> str:
    """Generate a UUIDv4 for offline entity creation."""
    return str(uuid.uuid4())

def generate_deterministic_id(entity_type: str, timestamp: str, node_id: str, sequence: int) -> str:
    """Generate a deterministic ID for ordered offline creation."""
    import hashlib
    seed = f"{entity_type}:{timestamp}:{node_id}:{sequence}"
    return str(uuid.UUID(hashlib.md5(seed.encode()).hexdigest()))
```

#### 3.1.2 Offline Entity States

| State | Description | Sync Behavior |
|-------|-------------|---------------|
| `offline_created` | Created while offline | Synced on reconnection |
| `offline_modified` | Modified while offline | Synced with conflict check |
| `offline_deleted` | Deleted while offline | Soft-deleted, synced on reconnection |
| `syncing` | Currently being synced | Read-only during sync |
| `synced` | Successfully synced | Normal operation |
| `conflict` | Sync conflict detected | Requires resolution |

#### 3.1.3 Offline Timestamp Management

```python
from datetime import datetime, timezone

class OfflineTimestamp:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.logical_clock = 0
        self.last_sync_time = None
    
    def create_timestamp(self) -> dict:
        """Create a timestamp for offline operations."""
        self.logical_clock += 1
        return {
            "physical": datetime.now(timezone.utc).isoformat(),
            "logical": self.logical_clock,
            "node_id": self.node_id,
            "synced": False
        }
    
    def sync_timestamp(self, server_time: datetime) -> dict:
        """Update timestamp after successful sync."""
        self.last_sync_time = server_time
        return {
            "physical": server_time.isoformat(),
            "logical": self.logical_clock,
            "node_id": self.node_id,
            "synced": True
        }
```

### 3.2 Entity-Specific Offline Creation

#### 3.2.1 Patient Entity (Offline)

```json
{
  "id": "offline-uuid-1234",
  "status": "offline_created",
  "medicalRecordNumber": "MRN-OFFLINE-001",
  "firstName": "Ahmed",
  "lastName": "Al-Rashid",
  "offlineMetadata": {
    "createdOffline": true,
    "nodeId": "node-uuid",
    "offlineTimestamp": "2026-06-25T08:00:00Z",
    "syncedAt": null,
    "version": 1
  },
  "syncPriority": "high",
  "localOnly": false
}
```

#### 3.2.2 Sample Entity (Offline)

```json
{
  "id": "offline-uuid-5678",
  "status": "offline_created",
  "sampleId": "SMP-OFFLINE-001",
  "patient": "patient-uuid",
  "type": "blood",
  "offlineMetadata": {
    "createdOffline": true,
    "nodeId": "node-uuid",
    "offlineTimestamp": "2026-06-25T08:30:00Z",
    "syncedAt": null,
    "version": 1
  },
  "syncPriority": "critical",
  "localOnly": false
}
```

#### 3.2.3 Test Result Entity (Offline)

```json
{
  "id": "offline-uuid-9012",
  "status": "offline_created",
  "testOrder": "test-order-uuid",
  "results": [
    {
      "analyte": "WBC",
      "value": "7.5",
      "unit": "10^3/uL",
      "flag": "normal"
    }
  ],
  "offlineMetadata": {
    "createdOffline": true,
    "nodeId": "node-uuid",
    "offlineTimestamp": "2026-06-25T10:00:00Z",
    "syncedAt": null,
    "version": 1
  },
  "syncPriority": "critical",
  "localOnly": false
}
```

---

## 4. OFFLINE UPDATE PATTERNS

### 4.1 Optimistic Concurrency Control

All offline updates use version numbers to detect conflicts:

```python
class OfflineUpdate:
    def __init__(self, entity_id: str, entity_type: str):
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.local_version = 0
        self.server_version = 0
        self.changes = {}
        self.timestamp = None
    
    def apply_change(self, field: str, old_value: any, new_value: any):
        """Apply a change to the entity."""
        self.changes[field] = {
            "from": old_value,
            "to": new_value
        }
    
    def get_update_payload(self) -> dict:
        """Get the payload for sync."""
        return {
            "entityType": self.entity_type,
            "entityId": self.entity_id,
            "localVersion": self.local_version,
            "serverVersion": self.server_version,
            "changes": self.changes,
            "timestamp": self.timestamp
        }
```

### 4.2 Version Tracking

Every entity maintains version information:

```json
{
  "id": "entity-uuid",
  "version": 3,
  "versionHistory": [
    {"version": 1, "nodeId": "node-1", "timestamp": "2026-06-25T08:00:00Z"},
    {"version": 2, "nodeId": "node-1", "timestamp": "2026-06-25T09:00:00Z"},
    {"version": 3, "nodeId": "node-2", "timestamp": "2026-06-25T10:00:00Z"}
  ],
  "lastModifiedBy": "node-2",
  "lastModifiedAt": "2026-06-25T10:00:00Z"
}
```

### 4.3 Batch Offline Updates

```python
class OfflineBatchUpdate:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.updates = []
        self.batch_id = str(uuid.uuid4())
    
    def add_update(self, entity_type: str, entity_id: str, changes: dict):
        """Add an update to the batch."""
        self.updates.append({
            "entityType": entity_type,
            "entityId": entity_id,
            "changes": changes,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    
    def get_batch_payload(self) -> dict:
        """Get the batch payload for sync."""
        return {
            "batchId": self.batch_id,
            "nodeId": self.node_id,
            "updates": self.updates,
            "totalCount": len(self.updates),
            "createdAt": datetime.now(timezone.utc).isoformat()
        }
```

---

## 5. CONFLICT DETECTION STRATEGIES

### 5.1 Version-Based Detection

The primary conflict detection strategy uses version numbers:

```python
class VersionConflictDetector:
    def detect(self, local_version: int, server_version: int) -> bool:
        """Detect if a conflict exists."""
        return local_version != server_version
    
    def get_conflict_type(self, local_version: int, server_version: int) -> str:
        """Determine the type of conflict."""
        if local_version < server_version:
            return "stale_local"  # Local is behind server
        elif local_version > server_version:
            return "forward_local"  # Local is ahead (shouldn't happen normally)
        else:
            return "no_conflict"  # Versions match
```

### 5.2 Timestamp-Based Detection

For entities without version numbers, timestamps are used:

```python
class TimestampConflictDetector:
    def detect(self, local_timestamp: str, server_timestamp: str) -> bool:
        """Detect conflict using timestamps."""
        local_dt = datetime.fromisoformat(local_timestamp)
        server_dt = datetime.fromisoformat(server_timestamp)
        
        # If server timestamp is newer, potential conflict
        if server_dt > local_dt:
            return True
        
        return False
    
    def get_conflict_severity(self, local_ts: str, server_ts: str) -> str:
        """Determine conflict severity based on time difference."""
        local_dt = datetime.fromisoformat(local_ts)
        server_dt = datetime.fromisoformat(server_ts)
        diff = abs((server_dt - local_dt).total_seconds())
        
        if diff < 60:  # Less than 1 minute
            return "low"
        elif diff < 3600:  # Less than 1 hour
            return "medium"
        else:
            return "high"
```

### 5.3 Field-Level Conflict Detection

Detect conflicts at the field level rather than entity level:

```python
class FieldLevelConflictDetector:
    def detect_field_conflicts(
        self,
        local_fields: dict,
        server_fields: dict,
        base_fields: dict
    ) -> list:
        """Detect conflicts at the field level."""
        conflicts = []
        
        for field in set(local_fields.keys()) | set(server_fields.keys()):
            local_val = local_fields.get(field)
            server_val = server_fields.get(field)
            base_val = base_fields.get(field)
            
            # Both changed from base = conflict
            if local_val != base_val and server_val != base_val:
                if local_val != server_val:
                    conflicts.append({
                        "field": field,
                        "localValue": local_val,
                        "serverValue": server_val,
                        "baseValue": base_val,
                        "conflictType": "both_modified"
                    })
            
            # One changed, one deleted
            elif (local_val != base_val and server_val is None) or \
                 (server_val != base_val and local_val is None):
                conflicts.append({
                    "field": field,
                    "localValue": local_val,
                    "serverValue": server_val,
                    "baseValue": base_val,
                    "conflictType": "modify_delete"
                })
        
        return conflicts
```

### 5.4 Hash-Based Conflict Detection

For large entities, hash comparison is efficient:

```python
import hashlib
import json

class HashConflictDetector:
    def compute_hash(self, entity: dict) -> str:
        """Compute a hash of the entity state."""
        serialized = json.dumps(entity, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()
    
    def detect(self, local_hash: str, server_hash: str) -> bool:
        """Detect conflict using hash comparison."""
        return local_hash != server_hash
```

---

## 6. CONFLICT RESOLUTION POLICIES

### 6.1 Policy Overview

| Policy | Description | Use Case | Deterministic |
|--------|-------------|----------|---------------|
| `last_write_wins` | Latest timestamp wins | Non-critical data | Yes |
| `server_wins` | Server always wins | Reference data | Yes |
| `local_wins` | Local always wins | Offline-created data | Yes |
| `merge` | Automatic field merge | Complementary changes | Yes |
| `manual` | Human resolves | Critical data | No |
| `highest_priority` | Priority node wins | Multi-site operations | Yes |

### 6.2 Last-Write-Wins (LWW)

```python
class LastWriteWinsResolver:
    def resolve(self, local_entity: dict, server_entity: dict) -> dict:
        """Resolve conflict using last-write-wins."""
        local_ts = datetime.fromisoformat(local_entity["updatedAt"])
        server_ts = datetime.fromisoformat(server_entity["updatedAt"])
        
        if local_ts >= server_ts:
            return local_entity
        else:
            return server_entity
    
    def get_resolution_log(self, local_entity: dict, server_entity: dict) -> dict:
        """Log the resolution for audit purposes."""
        local_ts = datetime.fromisoformat(local_entity["updatedAt"])
        server_ts = datetime.fromisoformat(server_entity["updatedAt"])
        
        winner = "local" if local_ts >= server_ts else "server"
        
        return {
            "policy": "last_write_wins",
            "winner": winner,
            "localTimestamp": local_entity["updatedAt"],
            "serverTimestamp": server_entity["updatedAt"],
            "resolvedAt": datetime.now(timezone.utc).isoformat()
        }
```

### 6.3 Server-Wins

```python
class ServerWinsResolver:
    def resolve(self, local_entity: dict, server_entity: dict) -> dict:
        """Server always wins."""
        return server_entity
    
    def get_resolution_log(self, local_entity: dict, server_entity: dict) -> dict:
        """Log the resolution."""
        return {
            "policy": "server_wins",
            "winner": "server",
            "reason": "Policy mandates server as source of truth",
            "resolvedAt": datetime.now(timezone.utc).isoformat()
        }
```

### 6.4 Local-Wins

```python
class LocalWinsResolver:
    def resolve(self, local_entity: dict, server_entity: dict) -> dict:
        """Local always wins (for offline-created data)."""
        return local_entity
    
    def get_resolution_log(self, local_entity: dict, server_entity: dict) -> dict:
        """Log the resolution."""
        return {
            "policy": "local_wins",
            "winner": "local",
            "reason": "Entity created offline, local is authoritative",
            "resolvedAt": datetime.now(timezone.utc).isoformat()
        }
```

### 6.5 Automatic Merge

```python
class AutoMergeResolver:
    def resolve(self, local_entity: dict, server_entity: dict, base_entity: dict) -> dict:
        """Automatically merge non-conflicting changes."""
        merged = base_entity.copy()
        conflicts = []
        
        all_fields = set(local_entity.keys()) | set(server_entity.keys()) | set(base_entity.keys())
        
        for field in all_fields:
            if field in ("id", "createdAt", "version", "offlineMetadata"):
                continue  # Skip immutable fields
            
            local_val = local_entity.get(field)
            server_val = server_entity.get(field)
            base_val = base_entity.get(field)
            
            if local_val == server_val:
                # Same change or no change
                merged[field] = local_val
            elif local_val == base_val:
                # Only server changed
                merged[field] = server_val
            elif server_val == base_val:
                # Only local changed
                merged[field] = local_val
            else:
                # Both changed - conflict
                conflicts.append({
                    "field": field,
                    "localValue": local_val,
                    "serverValue": server_val
                })
                # Default to server for conflicts
                merged[field] = server_val
        
        if conflicts:
            merged["_mergeConflicts"] = conflicts
        
        return merged
    
    def get_resolution_log(self, conflicts: list) -> dict:
        """Log the merge resolution."""
        return {
            "policy": "auto_merge",
            "mergedFields": [c["field"] for c in conflicts],
            "conflicts": conflicts,
            "resolvedAt": datetime.now(timezone.utc).isoformat()
        }
```

### 6.6 Manual Resolution

```python
class ManualResolver:
    def detect_escalation(self, conflicts: list) -> dict:
        """Detect when manual resolution is needed."""
        critical_fields = {"status", "result", "diagnosis", "treatment"}
        
        critical_conflicts = [
            c for c in conflicts
            if c["field"] in critical_fields
        ]
        
        return {
            "requiresManualResolution": len(critical_conflicts) > 0,
            "criticalConflicts": critical_conflicts,
            "escalationLevel": "supervisor" if critical_conflicts else "operator"
        }
```

### 6.7 Entity-Specific Resolution Policies

| Entity | Default Policy | Fallback | Manual Trigger |
|--------|---------------|----------|----------------|
| Patient | merge | manual | Any demographic conflict |
| Sample | last_write_wins | manual | Status conflict |
| Test Result | server_wins | manual | Result value conflict |
| Test Order | merge | manual | Priority conflict |
| User | server_wins | manual | Role conflict |
| Device | server_wins | manual | Status conflict |
| Credential | server_wins | manual | Status conflict |
| Inventory | merge | manual | Quantity conflict |
| Attendance | merge | manual | Time conflict |
| Correspondence | last_write_wins | manual | Status conflict |
| Finding | server_wins | manual | Severity conflict |
| Policy | server_wins | manual | Rule conflict |

---

## 7. SYNCHRONIZATION PRIORITIES

### 7.1 Priority Levels

| Priority | Value | Entities | Max Delay |
|----------|-------|----------|-----------|
| **Critical** | 1 | Test Results, Patient Safety | Immediate |
| **High** | 2 | Samples, Test Orders, Devices | 5 minutes |
| **Normal** | 3 | Patients, Users, Inventory | 15 minutes |
| **Low** | 4 | Reports, Configurations | 1 hour |
| **Background** | 5 | Audit Events, Telemetry | 24 hours |

### 7.2 Priority Assignment

```python
class SyncPriorityManager:
    ENTITY_PRIORITIES = {
        "test_result": 1,      # Critical
        "sample": 2,           # High
        "test_order": 2,       # High
        "device": 2,           # High
        "patient": 3,          # Normal
        "user": 3,             # Normal
        "inventory_item": 3,   # Normal
        "credential": 3,       # Normal
        "report": 4,           # Low
        "configuration": 4,    # Low
        "audit_event": 5,      # Background
        "telemetry_event": 5,  # Background
    }
    
    def get_priority(self, entity_type: str) -> int:
        """Get sync priority for entity type."""
        return self.ENTITY_PRIORITIES.get(entity_type, 3)  # Default to Normal
    
    def get_priority_label(self, priority: int) -> str:
        """Get human-readable priority label."""
        labels = {1: "Critical", 2: "High", 3: "Normal", 4: "Low", 5: "Background"}
        return labels.get(priority, "Normal")
```

### 7.3 Priority-Based Queue Management

```python
import heapq
from dataclasses import dataclass, field

@dataclass(order=True)
class SyncItem:
    priority: int
    entity_type: str = field(compare=False)
    entity_id: str = field(compare=False)
    operation: str = field(compare=False)
    payload: dict = field(compare=False)
    created_at: str = field(compare=False)

class PrioritySyncQueue:
    def __init__(self):
        self.queue = []
        self.item_set = set()  # Prevent duplicates
    
    def enqueue(self, entity_type: str, entity_id: str, operation: str, payload: dict):
        """Add item to priority queue."""
        priority_manager = SyncPriorityManager()
        priority = priority_manager.get_priority(entity_type)
        
        item_key = f"{entity_type}:{entity_id}:{operation}"
        if item_key not in self.item_set:
            item = SyncItem(
                priority=priority,
                entity_type=entity_type,
                entity_id=entity_id,
                operation=operation,
                payload=payload,
                created_at=datetime.now(timezone.utc).isoformat()
            )
            heapq.heappush(self.queue, item)
            self.item_set.add(item_key)
    
    def dequeue(self) -> SyncItem:
        """Get highest priority item."""
        if self.queue:
            item = heapq.heappop(self.queue)
            item_key = f"{item.entity_type}:{item.entity_id}:{item.operation}"
            self.item_set.discard(item_key)
            return item
        return None
    
    def get_queue_stats(self) -> dict:
        """Get queue statistics."""
        stats = {"total": len(self.queue), "by_priority": {}, "by_type": {}}
        for item in self.queue:
            priority_label = SyncPriorityManager().get_priority_label(item.priority)
            stats["by_priority"][priority_label] = stats["by_priority"].get(priority_label, 0) + 1
            stats["by_type"][item.entity_type] = stats["by_type"].get(item.entity_type, 0) + 1
        return stats
```

---

## 8. QUEUE MANAGEMENT

### 8.1 Queue States

```
pending → processing → completed
    ↓           ↓
    ↓       failed → retrying → completed
    ↓           ↓
    └─────→ cancelled
```

| State | Description | Retry |
|-------|-------------|-------|
| `pending` | Waiting to be synced | N/A |
| `processing` | Currently syncing | N/A |
| `completed` | Successfully synced | N/A |
| `failed` | Sync failed | Yes (with backoff) |
| `retrying` | Retrying failed sync | Yes (limited) |
| `cancelled` | Manually cancelled | No |

### 8.2 Queue Item Structure

```json
{
  "id": "queue-uuid",
  "entityType": "patient",
  "entityId": "patient-uuid",
  "operation": "create",
  "payload": {
    "firstName": "Ahmed",
    "lastName": "Al-Rashid"
  },
  "status": "pending",
  "priority": 3,
  "nodeId": "node-uuid",
  "createdAt": "2026-06-25T08:00:00Z",
  "attemptCount": 0,
  "maxAttempts": 5,
  "nextRetryAt": null,
  "lastError": null,
  "syncedAt": null
}
```

### 8.3 Retry Logic

```python
class RetryManager:
    RETRY_DELAYS = [0, 1, 5, 15, 60]  # seconds
    MAX_ATTEMPTS = 5
    
    def calculate_next_retry(self, attempt_count: int) -> dict:
        """Calculate next retry time with exponential backoff."""
        if attempt_count >= self.MAX_ATTEMPTS:
            return {"shouldRetry": False, "reason": "Max attempts reached"}
        
        delay = self.RETRY_DELAYS[min(attempt_count, len(self.RETRY_DELAYS) - 1)]
        # Add jitter (±20%)
        jitter = delay * 0.2 * (2 * (hash(str(attempt_count)) % 100) / 100 - 1)
        delay = max(0, delay + jitter)
        
        next_retry = datetime.now(timezone.utc) + timedelta(seconds=delay)
        
        return {
            "shouldRetry": True,
            "attemptCount": attempt_count + 1,
            "nextRetryAt": next_retry.isoformat(),
            "delaySeconds": delay
        }
```

### 8.4 Queue Monitoring

```python
class QueueMonitor:
    def get_queue_health(self) -> dict:
        """Monitor queue health metrics."""
        return {
            "totalPending": self.get_pending_count(),
            "byPriority": self.get_pending_by_priority(),
            "byEntity": self.get_pending_by_entity(),
            "oldestItem": self.get_oldest_pending(),
            "averageWaitTime": self.get_average_wait_time(),
            "failureRate": self.get_failure_rate(),
            "throughput": self.get_throughput_per_minute()
        }
    
    def get_alerts(self) -> list:
        """Generate alerts for queue issues."""
        alerts = []
        
        pending_count = self.get_pending_count()
        if pending_count > 1000:
            alerts.append({
                "level": "critical",
                "message": f"Sync queue backlog: {pending_count} items",
                "action": "Increase sync capacity or investigate connectivity"
            })
        
        failure_rate = self.get_failure_rate()
        if failure_rate > 0.1:  # 10% failure rate
            alerts.append({
                "level": "warning",
                "message": f"High sync failure rate: {failure_rate:.1%}",
                "action": "Check network connectivity and server health"
            })
        
        return alerts
```

---

## 9. DATA INTEGRITY IN OFFLINE MODE

### 9.1 Local Data Validation

All data created or modified offline must be validated:

```python
class OfflineDataValidator:
    def validate_entity(self, entity: dict, entity_type: str) -> dict:
        """Validate entity before local storage."""
        errors = []
        warnings = []
        
        # Required fields check
        required_fields = self.get_required_fields(entity_type)
        for field in required_fields:
            if field not in entity or entity[field] is None:
                errors.append(f"Missing required field: {field}")
        
        # Format validation
        if "email" in entity and entity["email"]:
            if not self.validate_email(entity["email"]):
                warnings.append("Invalid email format")
        
        # Business rules
        if entity_type == "sample":
            if "collectedAt" in entity:
                if not self.validate_future_date(entity["collectedAt"]):
                    errors.append("Collection date cannot be in the future")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
```

### 9.2 Local Transaction Safety

```python
class OfflineTransaction:
    def __init__(self, db_connection):
        self.db = db_connection
        self.operations = []
        self.savepoints = []
    
    def begin(self):
        """Begin transaction."""
        self.db.execute("BEGIN TRANSACTION")
    
    def add_operation(self, operation: str, entity_type: str, data: dict):
        """Add operation to transaction."""
        self.operations.append({
            "operation": operation,
            "entityType": entity_type,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    
    def commit(self):
        """Commit transaction."""
        try:
            self.db.execute("COMMIT")
            return {"success": True, "operations": len(self.operations)}
        except Exception as e:
            self.rollback()
            return {"success": False, "error": str(e)}
    
    def rollback(self):
        """Rollback transaction."""
        self.db.execute("ROLLBACK")
        self.operations = []
```

### 9.3 Checksum Verification

```python
class ChecksumVerifier:
    def compute_entity_checksum(self, entity: dict) -> str:
        """Compute checksum for entity integrity."""
        # Remove metadata fields that don't affect integrity
        checksum_entity = {
            k: v for k, v in entity.items()
            if k not in ("_checksum", "_lastSynced", "_syncStatus")
        }
        serialized = json.dumps(checksum_entity, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()
    
    def verify_integrity(self, entity: dict) -> bool:
        """Verify entity integrity using checksum."""
        stored_checksum = entity.get("_checksum")
        if not stored_checksum:
            return True  # No checksum to verify
        
        computed_checksum = self.compute_entity_checksum(entity)
        return stored_checksum == computed_checksum
```

### 9.4 Offline Data Encryption

```python
from cryptography.fernet import Fernet

class OfflineEncryption:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def encrypt_sensitive_fields(self, entity: dict, sensitive_fields: list) -> dict:
        """Encrypt sensitive fields before local storage."""
        encrypted_entity = entity.copy()
        
        for field in sensitive_fields:
            if field in encrypted_entity and encrypted_entity[field]:
                value = str(encrypted_entity[field]).encode()
                encrypted_entity[field] = self.cipher.encrypt(value).decode()
                encrypted_entity[f"{field}_encrypted"] = True
        
        return encrypted_entity
    
    def decrypt_sensitive_fields(self, entity: dict, sensitive_fields: list) -> dict:
        """Decrypt sensitive fields after local retrieval."""
        decrypted_entity = entity.copy()
        
        for field in sensitive_fields:
            if f"{field}_encrypted" in decrypted_entity and decrypted_entity.get(f"{field}_encrypted"):
                value = decrypted_entity[field].encode()
                decrypted_entity[field] = self.cipher.decrypt(value).decode()
                del decrypted_entity[f"{field}_encrypted"]
        
        return decrypted_entity
```

### 9.5 Sensitive Fields by Entity

| Entity | Sensitive Fields | Encryption Required |
|--------|-----------------|---------------------|
| Patient | nationalId, insurance.policyNumber, medicalRecordNumber | Yes |
| User | email, phone, passwordHash | Yes |
| Credential | licenseNumber, verificationCode | Yes |
| Test Result | All clinical data | Yes (at rest) |
| Sample | Patient linkage | Yes |
| Correspondence | Subject, Body (if classified) | Yes (if classified) |

---

## 10. SYNC PROTOCOL

### 10.1 Sync Handshake

```
┌──────────────┐                    ┌──────────────┐
│  Offline     │                    │   Server     │
│    Node      │                    │              │
└──────┬───────┘                    └──────┬───────┘
       │                                   │
       │  1. SYNC_REQUEST                  │
       │  (nodeId, lastSyncTime,           │
       │   capabilities)                   │
       │──────────────────────────────────>│
       │                                   │
       │  2. SYNC_RESPONSE                 │
       │  (serverTime, syncId,             │
       │   conflictPolicy)                 │
       │<──────────────────────────────────│
       │                                   │
       │  3. PUSH_DATA                     │
       │  (entities, priority order)       │
       │──────────────────────────────────>│
       │                                   │
       │  4. PUSH_ACK                      │
       │  (accepted, conflicts[])          │
       │<──────────────────────────────────│
       │                                   │
       │  5. PULL_DATA                     │
       │  (since: lastSyncTime)            │
       │──────────────────────────────────>│
       │                                   │
       │  6. PULL_RESPONSE                 │
       │  (entities, metadata)             │
       │<──────────────────────────────────│
       │                                   │
       │  7. SYNC_COMPLETE                 │
       │  (syncId, stats)                  │
       │──────────────────────────────────>│
       │                                   │
```

### 10.2 Sync Request

```json
{
  "nodeId": "node-uuid",
  "nodeType": "desktop",
  "lastSyncTime": "2026-06-25T08:00:00Z",
  "capabilities": {
    "supportsBatchSync": true,
    "supportsConflictResolution": true,
    "maxBatchSize": 100
  },
  "pendingOperations": [
    {"entityType": "patient", "count": 5},
    {"entityType": "sample", "count": 12},
    {"entityType": "test_result", "count": 25}
  ]
}
```

### 10.3 Sync Response

```json
{
  "syncId": "sync-uuid",
  "serverTime": "2026-06-25T10:00:00Z",
  "conflictPolicy": "last_write_wins",
  "accepted": true,
  "syncWindow": {
    "from": "2026-06-25T08:00:00Z",
    "to": "2026-06-25T10:00:00Z"
  }
}
```

### 10.4 Push Data

```json
{
  "syncId": "sync-uuid",
  "entities": [
    {
      "entityType": "patient",
      "operation": "create",
      "data": {
        "id": "offline-uuid-1234",
        "firstName": "Ahmed",
        "lastName": "Al-Rashid"
      },
      "offlineMetadata": {
        "createdOffline": true,
        "nodeId": "node-uuid",
        "offlineTimestamp": "2026-06-25T08:00:00Z"
      }
    }
  ],
  "batchNumber": 1,
  "totalBatches": 3
}
```

### 10.5 Push Acknowledgment

```json
{
  "syncId": "sync-uuid",
  "batchNumber": 1,
  "accepted": [
    {
      "entityType": "patient",
      "entityId": "offline-uuid-1234",
      "serverId": "server-uuid-5678",
      "status": "created"
    }
  ],
  "conflicts": [
    {
      "entityType": "sample",
      "entityId": "sample-uuid",
      "conflictType": "version_mismatch",
      "localVersion": 2,
      "serverVersion": 3,
      "resolution": "server_wins"
    }
  ]
}
```

### 10.6 Pull Response

```json
{
  "syncId": "sync-uuid",
  "entities": [
    {
      "entityType": "test_result",
      "operation": "update",
      "data": {
        "id": "result-uuid",
        "status": "verified",
        "verifiedBy": "supervisor-uuid"
      },
      "serverTimestamp": "2026-06-25T09:30:00Z"
    }
  ],
  "hasMore": true,
  "nextCursor": "cursor-uuid"
}
```

### 10.7 Sync Complete

```json
{
  "syncId": "sync-uuid",
  "stats": {
    "pushed": {
      "total": 42,
      "created": 20,
      "updated": 15,
      "deleted": 2,
      "conflicts": 5
    },
    "pulled": {
      "total": 150,
      "created": 80,
      "updated": 65,
      "deleted": 5
    },
    "duration": "12.5s",
    "bytesTransferred": 1048576
  },
  "nextSyncAvailable": "2026-06-25T10:05:00Z"
}
```

---

## 11. CONNECTIVITY DETECTION

### 11.1 Connectivity States

| State | Description | Behavior |
|-------|-------------|----------|
| `online` | Full connectivity | Normal operation |
| `degraded` | Intermittent connectivity | Reduced sync frequency |
| `offline` | No connectivity | Offline mode |
| `syncing` | Currently syncing | Partial online |

### 11.2 Connectivity Monitor

```python
class ConnectivityMonitor:
    def __init__(self):
        self.state = "online"
        self.last_check = None
        self.consecutive_failures = 0
        self.check_interval = 30  # seconds
    
    async def check_connectivity(self) -> dict:
        """Check connectivity to server."""
        try:
            # Try health endpoint
            response = await self.http_client.get(
                f"{self.server_url}/health",
                timeout=5
            )
            
            if response.status_code == 200:
                self.consecutive_failures = 0
                self.state = "online"
                return {"connected": True, "latency": response.elapsed.total_seconds()}
            else:
                self.consecutive_failures += 1
                if self.consecutive_failures >= 3:
                    self.state = "offline"
                return {"connected": False, "statusCode": response.status_code}
        
        except Exception as e:
            self.consecutive_failures += 1
            if self.consecutive_failures >= 3:
                self.state = "offline"
            return {"connected": False, "error": str(e)}
    
    def get_recommended_action(self) -> dict:
        """Get recommended action based on connectivity state."""
        if self.state == "online":
            return {"action": "sync", "frequency": "real_time"}
        elif self.state == "degraded":
            return {"action": "batch_sync", "frequency": "every_5_minutes"}
        else:
            return {"action": "queue_for_sync", "frequency": "when_reconnected"}
```

---

## 12. OFFLINE MODE TRANSITIONS

### 12.1 Going Offline

When connectivity is lost:

1. **Detect**: Connectivity monitor detects failure
2. **Notify**: Notify user of offline mode
3. **Queue**: Queue all write operations locally
4. **Validate**: Validate data before local storage
5. **Encrypt**: Encrypt sensitive fields
6. **Log**: Log transition for audit

### 12.2 Coming Online

When connectivity is restored:

1. **Detect**: Connectivity restored
2. **Sync**: Initiate sync protocol
3. **Resolve**: Resolve any conflicts
4. **Update**: Update local data with server changes
5. **Push**: Push local changes to server
6. **Notify**: Notify user of sync completion
7. **Log**: Log transition for audit

### 12.3 Transition Events

```json
{
  "event": "connectivity_changed",
  "from": "online",
  "to": "offline",
  "timestamp": "2026-06-25T08:00:00Z",
  "reason": "network_timeout",
  "pendingOperations": 0,
  "queuedEntities": []
}
```

---

## 13. OFFLINE REPORTING

### 13.1 Offline Dashboard

When offline, the system provides a local dashboard:

| Metric | Source | Update Frequency |
|--------|--------|-----------------|
| Pending Sync Items | Local queue | Real-time |
| Local Entity Counts | Local database | Real-time |
| Last Sync Time | Sync metadata | On sync completion |
| Sync Health | Queue monitor | Every 5 minutes |
| Conflicts Detected | Conflict log | On sync completion |

### 13.2 Offline Reports

| Report | Available Offline | Data Source |
|--------|-------------------|-------------|
| Daily Summary | Yes | Local database |
| Sample Counts | Yes | Local database |
| Result Statistics | Yes | Local database |
| User Activity | Yes | Local audit log |
| Inventory Status | Yes | Local database |

---

## 14. RECOVERY PROCEDURES

### 14.1 Data Recovery

If local database is corrupted:

1. **Backup Check**: Check for automatic backups
2. **Partial Recovery**: Recover what's possible
3. **Re-sync**: Full re-sync from server
4. **Validate**: Verify data integrity
5. **Report**: Generate recovery report

### 14.2 Queue Recovery

If sync queue is corrupted:

1. **Queue Scan**: Scan for orphaned items
2. **Deduplication**: Remove duplicate entries
3. **Priority Rebuild**: Rebuild priority ordering
4. **Validation**: Validate all queue items
5. **Resume**: Resume normal operation

---

*Document generated as part of NHDOS Canonical Domain Model*
*Offline behavior model defined and documented*
*Constitution Reference: Articles I, V, VIII, XIV*
*Last Updated: 2026-06-25*
