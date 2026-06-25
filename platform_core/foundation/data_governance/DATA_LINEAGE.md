# DATA LINEAGE

**NHDOS Platform-Core — Data Lineage**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS Data Lineage system tracks data flow from source to consumption across all platform services. It provides visibility into data origins, transformations, and destinations, enabling compliance, debugging, and data quality monitoring.

---

## 2. Architecture Overview

### 2.1 Data Lineage Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Data Lineage System                       │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Source    │  │  Transform  │  │   Target    │     │
│  │   Tracker   │  │   Logger    │  │   Registry  │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │              │
│         └────────┬───────┴────────┬───────┘              │
│                  │                │                       │
│         ┌────────▼────────┐ ┌────▼────────────┐         │
│         │  Lineage Graph  │ │  Metadata Store │         │
│         │  (Neo4j)        │ │  (PostgreSQL)   │         │
│         └─────────────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Lineage Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| Source Tracker | Custom Agent | Track data origins |
| Transform Logger | ETL Middleware | Log transformations |
| Lineage Graph | Neo4j | Store relationships |
| Metadata Store | PostgreSQL | Store metadata |
| API Gateway | REST API | Query lineage |

---

## 3. Lineage Model

### 3.1 Data Asset

```json
{
  "asset_id": "patient-record-001",
  "asset_type": "table",
  "name": "patient_master",
  "description": "Patient master data table",
  "owner": "healthcare-core-team",
  "classification": "sensitive",
  "source_system": "hospital-emr",
  "created_at": "2026-01-15T10:00:00Z",
  "updated_at": "2026-06-25T14:30:00Z"
}
```

### 3.2 Data Flow

```json
{
  "flow_id": "flow-001",
  "source": {
    "asset_id": "hospital-emr-patients",
    "system": "hospital-emr"
  },
  "target": {
    "asset_id": "patient-master",
    "system": "nhdos-core"
  },
  "transformations": [
    {
      "type": "map",
      "description": "Map EMR fields to NHDOS schema"
    },
    {
      "type": "validate",
      "description": "Validate patient demographics"
    },
    {
      "type": "encrypt",
      "description": "Encrypt PII fields"
    }
  ],
  "frequency": "real-time",
  "last_run": "2026-06-25T14:30:00Z"
}
```

### 3.3 Transformation Types

| Type | Description | Example |
|------|-------------|---------|
| `map` | Field mapping | EMR field → NHDOS field |
| `filter` | Data filtering | Remove inactive records |
| `aggregate` | Data aggregation | Daily summary calculation |
| `encrypt` | Encryption | PII field encryption |
| `anonymize` | Anonymization | Patient ID masking |
| `validate` | Validation | Data quality checks |
| `enrich` | Enrichment | Add reference data |

---

## 4. Lineage Tracking

### 4.1 Tracking Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| Automatic | System-instrumented | Database operations |
| Manual | Developer-declared | Custom transformations |
| Derived | Computed from metadata | Derived datasets |

### 4.2 Tracking Implementation

```python
from platform_lineage import LineageTracker

tracker = LineageTracker()

# Track data flow
with tracker.track(
    source="hospital-emr-patients",
    target="patient-master",
    operation="etl"
) as ctx:
    # Your data transformation code
    patients = extract_from_emr()
    transformed = transform(patients)
    load_to_core(transformed)
    
    # Lineage automatically tracked
    ctx.add_metadata("record_count", len(patients))
```

---

## 5. Lineage Querying

### 5.1 Query API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/lineage/assets` | GET | List data assets |
| `/api/v1/lineage/assets/{id}` | GET | Get asset details |
| `/api/v1/lineage/assets/{id}/upstream` | GET | Get upstream sources |
| `/api/v1/lineage/assets/{id}/downstream` | GET | Get downstream targets |
| `/api/v1/lineage/flows` | GET | List data flows |
| `/api/v1/lineage/flows/{id}` | GET | Get flow details |

### 5.2 Lineage Graph Query

```cypher
// Find all upstream sources for a target
MATCH (target:Asset {id: 'patient-master'})
MATCH path = (source:Asset)-[:FLOWS_TO*]->(target)
RETURN path

// Find all downstream consumers
MATCH (source:Asset {id: 'patient-master'})
MATCH path = (source)-[:FLOWS_TO*]->(target:Asset)
RETURN path

// Find impact of source change
MATCH (source:Asset {id: 'hospital-emr-patients'})
MATCH path = (source)-[:FLOWS_TO*]->(target:Asset)
WHERE target.classification = 'sensitive'
RETURN target, length(path) as depth
ORDER BY depth
```

---

## 6. Compliance

### 6.1 Compliance Requirements

| Requirement | Description | Lineage Support |
|-------------|-------------|-----------------|
| GDPR Art. 30 | Records of processing | Full lineage tracking |
| HIPAA §164.530 | Data access logging | Complete audit trail |
| Local Regulations | Data residency | Source/target tracking |

### 6.2 Audit Trail

| Event | Data Captured | Retention |
|-------|---------------|-----------|
| Data created | Source, timestamp, user | 7 years |
| Data transformed | Input, output, logic | 7 years |
| Data accessed | User, purpose, time | 7 years |
| Data deleted | Reason, timestamp | 7 years |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
