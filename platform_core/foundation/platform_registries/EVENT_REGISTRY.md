# EVENT REGISTRY

**NHDOS Platform-Core — Event Registry**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS Event Registry manages event schemas, versions, and documentation across all platform event-driven architectures. It ensures consistent event formats, enables event discovery, and supports event evolution with backward compatibility.

---

## 2. Architecture Overview

### 2.1 Event Registry Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Event Registry                            │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Event     │  │  Schema     │  │  Event      │     │
│  │   Store     │──▶│  Validator  │──▶│  Catalog    │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │              │
│         └────────┬───────┴────────┬───────┘              │
│                  │                │                       │
│         ┌────────▼────────┐ ┌────▼────────────┐         │
│         │  Event Store    │ │  Schema Store   │         │
│         │  (PostgreSQL)   │ │  (Schema Registry│        │
│         └─────────────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Event Model

### 3.1 Event Definition

```json
{
  "event_id": "patient-created-v1",
  "name": "Patient Created",
  "domain": "healthcare",
  "version": "1.0.0",
  "schema": {
    "type": "object",
    "properties": {
      "event_id": {"type": "string", "format": "uuid"},
      "event_type": {"type": "string", "const": "patient.created"},
      "timestamp": {"type": "string", "format": "date-time"},
      "source": {"type": "string"},
      "data": {
        "type": "object",
        "properties": {
          "patient_id": {"type": "string", "format": "uuid"},
          "national_id": {"type": "string"},
          "status": {"type": "string", "enum": ["ACTIVE", "INACTIVE"]}
        }
      }
    }
  },
  "metadata": {
    "owner": "healthcare-core-team",
    "category": "domain-event",
    "sensitive": true
  }
}
```

### 3.2 Event Categories

| Category | Description | Example |
|----------|-------------|---------|
| `domain-event` | Business events | Patient Created |
| `command` | Command events | Create Patient |
| `query` | Query events | Get Patient |
| `integration` | Integration events | External System Sync |
| `system` | System events | Service Started |

---

## 4. Event Schema

### 4.1 Event Schema Structure

```json
{
  "type": "object",
  "required": ["event_id", "event_type", "timestamp", "source", "data"],
  "properties": {
    "event_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique event identifier"
    },
    "event_type": {
      "type": "string",
      "description": "Event type identifier"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Event timestamp (ISO 8601)"
    },
    "source": {
      "type": "string",
      "description": "Event source service"
    },
    "data": {
      "type": "object",
      "description": "Event payload"
    },
    "metadata": {
      "type": "object",
      "description": "Event metadata"
    }
  }
}
```

### 4.2 Event Versioning

| Version Strategy | Description | Use Case |
|------------------|-------------|----------|
| Event type suffix | `patient.created.v1` | Simple versioning |
| Schema version | Schema-based versioning | Complex schemas |
| Content negotiation | Header-based versioning | Multiple versions |

---

## 5. Event Discovery

### 5.1 Discovery Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| API | REST API queries | Programmatic access |
| Catalog | Web portal | Human discovery |
| SDK | SDK integration | Code integration |
| Watch | Real-time updates | Live monitoring |

### 5.2 Event Catalog

```yaml
events:
  - name: "patient.created"
    domain: "healthcare"
    description: "Emitted when a new patient is registered"
    schema: "patient-created-v1"
    producers: ["patient-service"]
    consumers: ["notification-service", "analytics-service"]
    
  - name: "patient.updated"
    domain: "healthcare"
    description: "Emitted when patient data is updated"
    schema: "patient-updated-v1"
    producers: ["patient-service"]
    consumers: ["notification-service", "audit-service"]
    
  - name: "appointment.scheduled"
    domain: "healthcare"
    description: "Emitted when an appointment is scheduled"
    schema: "appointment-scheduled-v1"
    producers: ["appointment-service"]
    consumers: ["notification-service", "reminder-service"]
```

---

## 6. APIs

### 6.1 Event Registry API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/events` | GET | List events |
| `/api/v1/events` | POST | Register event |
| `/api/v1/events/{id}` | GET | Get event details |
| `/api/v1/events/{id}/schema` | GET | Get event schema |
| `/api/v1/events/{id}/versions` | GET | List event versions |
| `/api/v1/events/{id}/producers` | GET | List producers |
| `/api/v1/events/{id}/consumers` | GET | List consumers |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
