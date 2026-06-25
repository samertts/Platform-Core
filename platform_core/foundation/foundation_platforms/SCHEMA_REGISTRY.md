# SCHEMA REGISTRY

**NHDOS Platform-Core — Foundation Platform 14: Schema Registry**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The Schema Registry manages JSON Schema, OpenAPI, Avro, ProtoBuf, FHIR profiles, and event schemas for NHDOS, enforcing compatibility rules and migration rules across 18 governorates and 4,800 healthcare facilities.

---

## 2. Architecture

### 2.1 Core Principles

| Principle | Description |
|-----------|-------------|
| Centralized | Single schema repository |
| Versioned | Full schema version history |
| Compatible | Compatibility rules enforced |
| Validated | Schema validation on registration |
| Migrated | Migration rules for schema evolution |

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SCHEMA REGISTRY                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Schema      │  │   Version    │  │   Compatibility│         │
│  │  Store       │──▶│   Manager    │──▶│   Checker    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │  Validation  │  │   Migration  │  │   Discovery  │          │
│  │  Engine      │  │   Engine     │  │   Service    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Schema Types

### 3.1 Supported Formats

| Format | Usage | Validation |
|--------|-------|------------|
| JSON Schema | API request/response | JSON Schema Draft 7 |
| OpenAPI 3.0 | REST API specifications | OpenAPI 3.0.3 |
| Avro | Event schemas | Avro 1.11 |
| ProtoBuf | gRPC definitions | Proto3 |
| FHIR Profiles | Healthcare resources | FHIR R4 |
| Event Schemas | Event payloads | JSON Schema |

### 3.2 Schema Registry Entries

| Schema | Type | Version | Compatibility |
|--------|------|---------|---------------|
| Patient | JSON Schema | 1.0.0 | Backward |
| Encounter | JSON Schema | 1.0.0 | Backward |
| Observation | JSON Schema | 1.0.0 | Backward |
| MedicationRequest | JSON Schema | 1.0.0 | Backward |
| DiagnosticReport | JSON Schema | 1.0.0 | Backward |
| NHDOS-Patient | FHIR Profile | 1.0.0 | Backward |
| NHDOS-Encounter | FHIR Profile | 1.0.0 | Backward |
| PatientCreated | Avro | 1.0.0 | Full |
| EncounterCreated | Avro | 1.0.0 | Full |
| ObservationCreated | Avro | 1.0.0 | Full |

---

## 4. Compatibility Rules

### 4.1 Compatibility Modes

| Mode | Description | Rules |
|------|-------------|-------|
| Backward | New schema readable by old consumers | No removal, no type change |
| Forward | Old schema readable by new consumers | No addition, no type change |
| Full | Both backward and forward compatible | No changes except additions |
| None | No compatibility checks | Any change allowed |

### 4.2 Allowed Changes by Mode

| Change | Backward | Forward | Full |
|--------|----------|---------|------|
| Add optional field | ✓ | ✗ | ✗ |
| Remove optional field | ✗ | ✓ | ✗ |
| Add required field | ✗ | ✗ | ✗ |
| Remove required field | ✗ | ✗ | ✗ |
| Change field type | ✗ | ✗ | ✗ |
| Add enum value | ✓ | ✗ | ✗ |

---

## 5. Migration Rules

### 5.1 Migration Types

| Type | Description | Example |
|------|-------------|---------|
| Field Rename | Rename a field | `name` → `full_name` |
| Type Change | Change field type | `string` → `integer` |
| Restructure | Restructure schema | Nested to flat |
| Deprecation | Mark field deprecated | With migration path |

### 5.2 Migration Example

```yaml
migration:
  version: "1.0.0 -> 1.1.0"
  rules:
    - type: field_rename
      from: "name"
      to: "full_name"
      transform: "identity"
    - type: field_deprecate
      field: "old_field"
      replacement: "new_field"
```

---

## 6. APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/schemas | GET | List all schemas |
| /api/v1/schemas/{schema} | GET | Get schema |
| /api/v1/schemas/{schema}/versions | GET | List versions |
| /api/v1/schemas/{schema}/versions/{version} | GET | Get version |
| /api/v1/schemas/{schema}/validate | POST | Validate data |
| /api/v1/schemas/{schema}/compatibility | POST | Check compatibility |
| /api/v1/schemas/{schema}/migrate | POST | Migrate data |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
