# SCHEMA REGISTRY

**NHDOS Platform-Core — Schema Registry**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS Schema Registry manages data schemas across all platform services, ensuring compatibility, versioning, and governance of data structures. It provides schema validation, evolution tracking, and compatibility checks for all data exchanges.

---

## 2. Architecture Overview

### 2.1 Schema Registry Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Schema Registry                           │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Schema    │  │ Compatibility│  │  Schema     │     │
│  │   Store     │──▶│   Checker   │──▶│  Evolution  │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │              │
│         └────────┬───────┴────────┬───────┘              │
│                  │                │                       │
│         ┌────────▼────────┐ ┌────▼────────────┐         │
│         │  Schema Store   │ │  Version Store  │         │
│         │  (PostgreSQL)   │ │  (PostgreSQL)   │         │
│         └─────────────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Schema Model

### 3.1 Schema Definition

```json
{
  "schema_id": "patient-record-v1",
  "name": "Patient Record",
  "domain": "healthcare",
  "version": "1.0.0",
  "format": "avro",
  "compatibility": "backward",
  "schema": {
    "type": "record",
    "name": "PatientRecord",
    "fields": [
      {"name": "id", "type": "string"},
      {"name": "national_id", "type": "string"},
      {"name": "given_name", "type": "string"},
      {"name": "family_name", "type": "string"},
      {"name": "date_of_birth", "type": "string", "logicalType": "date"},
      {"name": "status", "type": {"type": "enum", "name": "Status", "symbols": ["ACTIVE", "INACTIVE"]}}
    ]
  },
  "metadata": {
    "owner": "healthcare-core-team",
    "classification": "sensitive",
    "created_at": "2026-01-15T10:00:00Z",
    "updated_at": "2026-06-25T14:30:00Z"
  }
}
```

### 3.2 Schema Formats

| Format | Usage | Compatibility |
|--------|-------|---------------|
| Avro | Kafka messages | Full support |
| JSON Schema | REST APIs | Full support |
| Protobuf | gRPC services | Full support |
| OpenAPI | API contracts | Partial support |

---

## 4. Schema Compatibility

### 4.1 Compatibility Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `backward` | New schema reads old data | Consumer upgrade first |
| `forward` | Old schema reads new data | Producer upgrade first |
| `full` | Both backward and forward | Strict compatibility |
| `none` | No compatibility check | Development only |

### 4.2 Compatibility Rules

| Change | Backward | Forward | Full |
|--------|----------|---------|------|
| Add optional field | ✓ | ✓ | ✓ |
| Remove optional field | ✓ | ✓ | ✓ |
| Add required field | ✗ | ✓ | ✗ |
| Remove required field | ✓ | ✗ | ✗ |
| Change field type | ✗ | ✗ | ✗ |
| Rename field | ✗ | ✗ | ✗ |
| Add enum value | ✗ | ✓ | ✗ |
| Remove enum value | ✓ | ✗ | ✗ |

---

## 5. Schema Evolution

### 5.1 Evolution Process

```
1. Developer proposes schema change
2. System validates compatibility
3. Automated tests verify impact
4. Schema version incremented
5. New version registered
6. Producers/consumers updated
7. Old version deprecated
8. Old version retired
```

### 5.2 Version Management

```python
class SchemaVersionManager:
    def create_version(self, schema_id: str, new_schema: Schema) -> SchemaVersion:
        # 1. Get current version
        current = self.get_current_version(schema_id)
        
        # 2. Check compatibility
        if not self.check_compatibility(current, new_schema):
            raise IncompatibleSchema("Schema change not compatible")
        
        # 3. Increment version
        new_version = self.increment_version(current.version)
        
        # 4. Register new version
        self.register_version(
            schema_id=schema_id,
            version=new_version,
            schema=new_schema
        )
        
        return new_version
```

---

## 6. APIs

### 6.1 Schema Registry API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/schemas` | GET | List schemas |
| `/api/v1/schemas` | POST | Register schema |
| `/api/v1/schemas/{id}` | GET | Get schema |
| `/api/v1/schemas/{id}/versions` | GET | List versions |
| `/api/v1/schemas/{id}/versions/{version}` | GET | Get version |
| `/api/v1/schemas/{id}/compatibility` | POST | Check compatibility |
| `/api/v1/schemas/{id}/evolve` | POST | Create new version |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
