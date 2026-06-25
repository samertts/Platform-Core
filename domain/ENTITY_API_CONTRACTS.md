# ENTITY API CONTRACTS — NATIONAL HEALTHCARE DIGITAL OPERATING SYSTEM

**Document**: Canonical Entity API Contracts
**Version**: 1.0.0
**Date**: 2026-06-25
**Status**: ACTIVE
**Constitution Reference**: Articles IV, VII, XII

---

## 1. OVERVIEW

This document defines the complete API contracts for every entity in the National Healthcare Digital Operating System (NHDOS). Each entity follows standardized REST patterns with consistent request/response schemas, pagination, filtering, sorting, and error handling.

**Base URL**: `https://{host}/api/v1`
**Content-Type**: `application/json`
**Authentication**: Bearer JWT token in `Authorization` header
**API Versioning**: URL path versioning (`/api/v1/`, `/api/v2/`)

---

## 2. GLOBAL CONVENTIONS

### 2.1 Standard HTTP Methods

| Method | Purpose | Idempotent | Response |
|--------|---------|------------|----------|
| `GET` | Read resource(s) | Yes | 200 OK |
| `POST` | Create resource | No | 201 Created |
| `PUT` | Full replacement | Yes | 200 OK |
| `PATCH` | Partial update | No | 200 OK |
| `DELETE` | Remove resource | Yes | 204 No Content |

### 2.2 Standard Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 20 | Max items per page (1-100) |
| `cursor` | string | null | Pagination cursor |
| `sort` | string | `created_at:desc` | Sort field and direction |
| `fields` | string | null | Comma-separated field list |
| `q` | string | null | Full-text search query |
| `created_after` | datetime | null | Filter by creation date |
| `created_before` | datetime | null | Filter by creation date |
| `updated_after` | datetime | null | Filter by update date |
| `updated_before` | datetime | null | Filter by update date |

### 2.3 Standard Response Envelope

```json
{
  "data": {},
  "meta": {
    "requestId": "req-uuid",
    "timestamp": "2026-06-25T10:00:00Z",
    "duration": "45ms",
    "apiVersion": "v1"
  }
}
```

### 2.4 Standard Error Response (RFC 7807)

```json
{
  "type": "https://api.nhdos.gov/errors/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "Entity name already exists",
  "instance": "/api/v1/entities",
  "errors": [
    {
      "field": "name",
      "message": "Name 'x' already exists",
      "code": "DUPLICATE",
      "rejectedValue": "x"
    }
  ],
  "meta": {
    "requestId": "req-uuid",
    "timestamp": "2026-06-25T10:00:01Z"
  }
}
```

### 2.5 Standard Pagination Response

```json
{
  "data": [],
  "pagination": {
    "limit": 20,
    "cursor": "eyJpZCI6MTAwfQ==",
    "hasMore": true,
    "total": 150,
    "page": 8
  },
  "meta": {}
}
```

---

## 3. ENTITY API CONTRACTS

### 3.1 Repository Entity

**Resource**: `/api/v1/repositories`

#### 3.1.1 List Repositories

```
GET /api/v1/repositories
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | enum | Filter by status: `created`, `active`, `deprecated`, `suspended`, `archived`, `deleted` |
| `maturity` | enum | Filter by maturity: `experimental`, `alpha`, `beta`, `stable`, `mature`, `legacy` |
| `visibility` | enum | Filter by visibility: `public`, `internal`, `private` |
| `owner` | uuid | Filter by owner team ID |
| `language` | string | Filter by primary language |

**Response 200**:
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "platform-core",
      "slug": "platform-core",
      "description": "Authoritative governance and runtime platform",
      "owner": {
        "id": "team-uuid",
        "name": "Platform Team"
      },
      "language": "python",
      "framework": "FastAPI",
      "status": "active",
      "maturity": "stable",
      "visibility": "internal",
      "modules": [
        {"id": "mod-uuid", "name": "runtime"}
      ],
      "dependencies": [
        {"id": "dep-uuid", "name": "postgresql", "type": "external_package"}
      ],
      "tags": ["foundation", "governance"],
      "manifest": {
        "version": "2.0.0",
        "signed": true,
        "valid": true
      },
      "metadata": {},
      "createdAt": "2026-01-15T08:00:00Z",
      "updatedAt": "2026-06-25T10:00:00Z"
    }
  ],
  "pagination": {
    "limit": 20,
    "cursor": null,
    "hasMore": false,
    "total": 8
  },
  "meta": {
    "requestId": "req-uuid",
    "timestamp": "2026-06-25T10:00:00Z"
  }
}
```

#### 3.1.2 Get Repository by ID

```
GET /api/v1/repositories/{id}
```

**Response 200**: Single Repository object
**Response 404**: `{"type": "...", "title": "Not Found", "status": 404, "detail": "Repository not found"}`

#### 3.1.3 Create Repository

```
POST /api/v1/repositories
```

**Request Body**:
```json
{
  "name": "new-module",
  "description": "Module purpose description",
  "language": "python",
  "framework": "FastAPI",
  "visibility": "internal",
  "tags": ["laboratory", "clinical"],
  "metadata": {}
}
```

**Response 201**: Created Repository object
**Response 409**: Duplicate name error
**Response 422**: Validation error

#### 3.1.4 Update Repository

```
PUT /api/v1/repositories/{id}
```

**Request Body**: Full Repository object
**Response 200**: Updated Repository object

#### 3.1.5 Partial Update Repository

```
PATCH /api/v1/repositories/{id}
```

**Request Body**:
```json
{
  "status": "deprecated",
  "description": "Updated description"
}
```

**Response 200**: Updated Repository object

#### 3.1.6 Delete Repository

```
DELETE /api/v1/repositories/{id}
```

**Response 204**: No Content
**Response 409**: Cannot delete repository with active modules

#### 3.1.7 Search Repositories

```
POST /api/v1/repositories/search
```

**Request Body**:
```json
{
  "query": "platform governance",
  "filters": {
    "status": ["active"],
    "maturity": ["stable", "mature"],
    "language": ["python"]
  },
  "sort": "name:asc",
  "limit": 20,
  "cursor": null
}
```

**Response 200**: Paginated Repository list

#### 3.1.8 Bulk Operations

```
POST /api/v1/repositories/bulk
```

**Request Body**:
```json
{
  "operations": [
    {"action": "create", "data": {"name": "repo-1", "language": "python"}},
    {"action": "update", "id": "repo-uuid", "data": {"status": "active"}},
    {"action": "delete", "id": "repo-uuid-2"}
  ]
}
```

**Response 200**:
```json
{
  "data": {
    "results": [
      {"action": "create", "status": "success", "id": "new-uuid"},
      {"action": "update", "status": "success", "id": "repo-uuid"},
      {"action": "delete", "status": "success", "id": "repo-uuid-2"}
    ],
    "summary": {"total": 3, "success": 3, "failed": 0}
  }
}
```

#### 3.1.9 Sync Repository

```
POST /api/v1/repositories/{id}/sync
```

**Request Body**:
```json
{
  "force": false,
  "validateManifest": true
}
```

**Response 200**: Sync status object

#### 3.1.10 Verify Repository

```
POST /api/v1/repositories/{id}/verify
```

**Response 200**:
```json
{
  "data": {
    "repositoryId": "uuid",
    "checks": {
      "manifestValid": true,
      "dependenciesResolved": true,
      "testsPassing": true,
      "securityScanClean": true,
      "governanceCompliant": true
    },
    "overallStatus": "passed",
    "verifiedAt": "2026-06-25T10:00:00Z"
  }
}
```

---

### 3.2 Module Entity

**Resource**: `/api/v1/modules`

#### 3.2.1 List Modules

```
GET /api/v1/modules
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `repository` | uuid | Filter by parent repository |
| `status` | enum | Filter by status |
| `maturity` | enum | Filter by maturity |

**Response 200**: Paginated Module list

#### 3.2.2 Get Module

```
GET /api/v1/modules/{id}
```

**Response 200**: Single Module object with nested services, APIs, events

#### 3.2.3 Create Module

```
POST /api/v1/modules
```

**Request Body**:
```json
{
  "name": "authentication",
  "description": "User authentication and authorization",
  "repository": "repo-uuid",
  "services": [],
  "apis": [],
  "events": [],
  "metadata": {}
}
```

**Response 201**: Created Module object

#### 3.2.4 Update Module

```
PUT /api/v1/modules/{id}
```

#### 3.2.5 Partial Update Module

```
PATCH /api/v1/modules/{id}
```

#### 3.2.6 Delete Module

```
DELETE /api/v1/modules/{id}
```

#### 3.2.7 Search Modules

```
POST /api/v1/modules/search
```

#### 3.2.8 Bulk Operations

```
POST /api/v1/modules/bulk
```

#### 3.2.9 Sync Module

```
POST /api/v1/modules/{id}/sync
```

#### 3.2.10 Verify Module

```
POST /api/v1/modules/{id}/verify
```

---

### 3.3 Service Entity

**Resource**: `/api/v1/services`

#### 3.3.1 List Services

```
GET /api/v1/services
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `module` | uuid | Filter by parent module |
| `type` | enum | Filter by type: `core`, `module`, `adapter`, `gateway`, `worker`, `scheduler` |
| `status` | enum | Filter by status |

#### 3.3.2 Get Service

```
GET /api/v1/services/{id}
```

#### 3.3.3 Create Service

```
POST /api/v1/services
```

**Request Body**:
```json
{
  "name": "auth-service",
  "description": "JWT authentication service",
  "module": "module-uuid",
  "type": "core",
  "healthEndpoint": "/health",
  "metricsEndpoint": "/metrics",
  "apis": [],
  "eventsConsuming": [],
  "eventsPublishing": [],
  "dependencies": [],
  "metadata": {}
}
```

#### 3.3.4 Update Service

```
PUT /api/v1/services/{id}
```

#### 3.3.5 Partial Update Service

```
PATCH /api/v1/services/{id}
```

#### 3.3.6 Delete Service

```
DELETE /api/v1/services/{id}
```

#### 3.3.7 Search Services

```
POST /api/v1/services/search
```

#### 3.3.8 Bulk Operations

```
POST /api/v1/services/bulk
```

#### 3.3.9 Sync Service

```
POST /api/v1/services/{id}/sync
```

#### 3.3.10 Verify Service

```
POST /api/v1/services/{id}/verify
```

---

### 3.4 API Entity

**Resource**: `/api/v1/apis`

#### 3.4.1 List APIs

```
GET /api/v1/apis
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `service` | uuid | Filter by parent service |
| `type` | enum | Filter by type: `rest`, `graphql`, `grpc`, `websocket`, `webhook` |
| `status` | enum | Filter by status |
| `authentication` | enum | Filter by auth method |

#### 3.4.2 Get API

```
GET /api/v1/apis/{id}
```

#### 3.4.3 Create API

```
POST /api/v1/apis
```

**Request Body**:
```json
{
  "name": "User Management API",
  "description": "CRUD operations for users",
  "service": "service-uuid",
  "type": "rest",
  "basePath": "/api/v1/users",
  "schema": "schema-ref",
  "authentication": "jwt",
  "rateLimit": {
    "requestsPerMinute": 100,
    "burstSize": 20
  },
  "backwardCompatible": true,
  "metadata": {}
}
```

#### 3.4.4 Update API

```
PUT /api/v1/apis/{id}
```

#### 3.4.5 Partial Update API

```
PATCH /api/v1/apis/{id}
```

#### 3.4.6 Delete API

```
DELETE /api/v1/apis/{id}
```

#### 3.4.7 Search APIs

```
POST /api/v1/apis/search
```

#### 3.4.8 Bulk Operations

```
POST /api/v1/apis/bulk
```

#### 3.4.9 Sync API

```
POST /api/v1/apis/{id}/sync
```

#### 3.4.10 Verify API

```
POST /api/v1/apis/{id}/verify
```

---

### 3.5 Event Entity

**Resource**: `/api/v1/events`

#### 3.5.1 List Events

```
GET /api/v1/events
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `publisher` | uuid | Filter by publishing service |
| `category` | enum | Filter by category: `domain`, `integration`, `system`, `audit`, `notification` |
| `status` | enum | Filter by status |
| `type` | string | Filter by event type pattern |

#### 3.5.2 Get Event

```
GET /api/v1/events/{id}
```

#### 3.5.3 Create Event

```
POST /api/v1/events
```

**Request Body**:
```json
{
  "name": "patient.admitted",
  "description": "Published when a patient is admitted",
  "category": "domain",
  "publisher": "service-uuid",
  "schema": {
    "type": "object",
    "properties": {
      "patientId": {"type": "string"},
      "admittedAt": {"type": "string", "format": "date-time"},
      "ward": {"type": "string"}
    }
  },
  "retentionDays": 365,
  "orderingKey": "patientId",
  "metadata": {}
}
```

#### 3.5.4 Update Event

```
PUT /api/v1/events/{id}
```

#### 3.5.5 Partial Update Event

```
PATCH /api/v1/events/{id}
```

#### 3.5.6 Delete Event

```
DELETE /api/v1/events/{id}
```

#### 3.5.7 Search Events

```
POST /api/v1/events/search
```

#### 3.5.8 Bulk Operations

```
POST /api/v1/events/bulk
```

#### 3.5.9 Sync Event

```
POST /api/v1/events/{id}/sync
```

#### 3.5.10 Verify Event

```
POST /api/v1/events/{id}/verify
```

---

### 3.6 Device Entity

**Resource**: `/api/v1/devices`

#### 3.6.1 List Devices

```
GET /api/v1/devices
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | enum | Filter by type: `analyzer`, `reader`, `printer`, `sensor`, `imaging`, `point_of_care`, `infusion`, `monitor` |
| `status` | enum | Filter by status |
| `protocol` | uuid | Filter by communication protocol |
| `location` | string | Filter by physical location |

#### 3.6.2 Get Device

```
GET /api/v1/devices/{id}
```

#### 3.6.3 Create Device

```
POST /api/v1/devices
```

**Request Body**:
```json
{
  "name": "Cobas 8800 Analyzer",
  "description": "Molecular diagnostics analyzer",
  "type": "analyzer",
  "manufacturer": "Roche",
  "model": "Cobas 8800",
  "protocol": "protocol-uuid",
  "driver": "driver-uuid",
  "capabilities": ["rna_detection", "pcr"],
  "location": "Building A, Room 101",
  "metadata": {
    "serialNumber": "SN-12345",
    "purchaseDate": "2025-01-15"
  }
}
```

#### 3.6.4 Update Device

```
PUT /api/v1/devices/{id}
```

#### 3.6.5 Partial Update Device

```
PATCH /api/v1/devices/{id}
```

#### 3.6.6 Delete Device

```
DELETE /api/v1/devices/{id}
```

#### 3.6.7 Search Devices

```
POST /api/v1/devices/search
```

#### 3.6.8 Bulk Operations

```
POST /api/v1/devices/bulk
```

#### 3.6.9 Sync Device

```
POST /api/v1/devices/{id}/sync
```

#### 3.6.10 Verify Device

```
POST /api/v1/devices/{id}/verify
```

---

### 3.7 Workflow Entity

**Resource**: `/api/v1/workflows`

#### 3.7.1 List Workflows

```
GET /api/v1/workflows
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | enum | Filter by status: `draft`, `active`, `suspended`, `retired` |
| `triggerEvent` | string | Filter by trigger event type |

#### 3.7.2 Get Workflow

```
GET /api/v1/workflows/{id}
```

#### 3.7.3 Create Workflow

```
POST /api/v1/workflows
```

**Request Body**:
```json
{
  "name": "Sample Intake Workflow",
  "description": "Automated sample intake and registration",
  "steps": [
    {
      "name": "Receive Sample",
      "type": "service_call",
      "service": "sample-service-uuid",
      "action": "receive",
      "timeoutSeconds": 30,
      "retryPolicy": {"maxRetries": 3, "backoffMs": 1000}
    },
    {
      "name": "Validate Sample",
      "type": "condition",
      "conditions": [{"field": "sampleType", "operator": "in", "value": ["blood", "urine", "saliva"]}]
    },
    {
      "name": "Register Sample",
      "type": "service_call",
      "service": "sample-service-uuid",
      "action": "register"
    }
  ],
  "triggerEvents": ["sample.received"],
  "emittedEvents": ["sample.registered", "sample.rejected"],
  "metadata": {}
}
```

#### 3.7.4 Update Workflow

```
PUT /api/v1/workflows/{id}
```

#### 3.7.5 Partial Update Workflow

```
PATCH /api/v1/workflows/{id}
```

#### 3.7.6 Delete Workflow

```
DELETE /api/v1/workflows/{id}
```

#### 3.7.7 Search Workflows

```
POST /api/v1/workflows/search
```

#### 3.7.8 Bulk Operations

```
POST /api/v1/workflows/bulk
```

#### 3.7.9 Sync Workflow

```
POST /api/v1/workflows/{id}/sync
```

#### 3.7.10 Verify Workflow

```
POST /api/v1/workflows/{id}/verify
```

---

### 3.8 Policy Entity

**Resource**: `/api/v1/policies`

#### 3.8.1 List Policies

```
GET /api/v1/policies
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | enum | Filter by type: `access_control`, `data_governance`, `security`, `compliance`, `quality`, `deployment` |
| `enforcement` | enum | Filter by enforcement: `enforcing`, `advisory`, `audit_only` |
| `scope` | enum | Filter by scope |
| `status` | enum | Filter by status |

#### 3.8.2 Get Policy

```
GET /api/v1/policies/{id}
```

#### 3.8.3 Create Policy

```
POST /api/v1/policies
```

**Request Body**:
```json
{
  "name": "access.lab.result.read",
  "description": "Controls who can read laboratory results",
  "type": "access_control",
  "enforcement": "enforcing",
  "scope": "module",
  "rules": [
    {
      "effect": "allow",
      "subjects": ["role:lab_tech", "role:physician"],
      "resources": ["lab.result.*"],
      "conditions": [
        {"type": "time_based", "operator": "between", "value": ["08:00", "18:00"]}
      ]
    },
    {
      "effect": "deny",
      "subjects": ["role:admin"],
      "resources": ["lab.result.*"],
      "conditions": [
        {"type": "attribute_based", "operator": "not_in", "value": {"field": "department", "values": ["laboratory"]}}
      ]
    }
  ],
  "metadata": {}
}
```

#### 3.8.4 Update Policy

```
PUT /api/v1/policies/{id}
```

#### 3.8.5 Partial Update Policy

```
PATCH /api/v1/policies/{id}
```

#### 3.8.6 Delete Policy

```
DELETE /api/v1/policies/{id}
```

#### 3.8.7 Search Policies

```
POST /api/v1/policies/search
```

#### 3.8.8 Bulk Operations

```
POST /api/v1/policies/bulk
```

#### 3.8.9 Sync Policy

```
POST /api/v1/policies/{id}/sync
```

#### 3.8.10 Verify Policy

```
POST /api/v1/policies/{id}/verify
```

---

### 3.9 Manifest Entity

**Resource**: `/api/v1/manifests`

#### 3.9.1 List Manifests

```
GET /api/v1/manifests
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `repository` | uuid | Filter by owning repository |
| `status` | enum | Filter by status: `draft`, `valid`, `invalid`, `expired` |
| `schemaVersion` | string | Filter by schema version |

#### 3.9.2 Get Manifest

```
GET /api/v1/manifests/{id}
```

#### 3.9.3 Create Manifest

```
POST /api/v1/manifests
```

**Request Body**:
```json
{
  "repository": "repo-uuid",
  "schemaVersion": "2.0.0",
  "version": "1.0.0",
  "identity": {
    "name": "my-module",
    "slug": "my-module",
    "description": "Module purpose"
  },
  "purpose": "Laboratory information management",
  "ownership": {
    "team": "team-uuid",
    "organization": "health-ministry"
  },
  "services": [],
  "apis": [],
  "events": [],
  "dependencies": [],
  "runtime": {
    "python": ">=3.11",
    "memory": "512MB",
    "disk": "1GB"
  },
  "maturity": "beta",
  "compatibility": {
    "platformCore": ">=2.0.0",
    "backwardCompatible": true
  },
  "metadata": {}
}
```

#### 3.9.4 Update Manifest

```
PUT /api/v1/manifests/{id}
```

#### 3.9.5 Partial Update Manifest

```
PATCH /api/v1/manifests/{id}
```

#### 3.9.6 Delete Manifest

```
DELETE /api/v1/manifests/{id}
```

#### 3.9.7 Search Manifests

```
POST /api/v1/manifests/search
```

#### 3.9.8 Bulk Operations

```
POST /api/v1/manifests/bulk
```

#### 3.9.9 Sync Manifest

```
POST /api/v1/manifests/{id}/sync
```

#### 3.9.10 Verify Manifest

```
POST /api/v1/manifests/{id}/verify
```

---

### 3.10 Certification Entity

**Resource**: `/api/v1/certifications`

#### 3.10.1 List Certifications

```
GET /api/v1/certifications
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `module` | uuid | Filter by certified module |
| `level` | enum | Filter by level: `basic`, `standard`, `clinical`, `national` |
| `status` | enum | Filter by status: `pending`, `passed`, `conditional`, `failed`, `expired`, `revoked` |
| `scope` | enum | Filter by scope |

#### 3.10.2 Get Certification

```
GET /api/v1/certifications/{id}
```

#### 3.10.3 Create Certification

```
POST /api/v1/certifications
```

**Request Body**:
```json
{
  "module": "module-uuid",
  "level": "standard",
  "scope": "full",
  "criteria": [
    {"name": "Security Scan", "required": true, "weight": 0.25},
    {"name": "Test Coverage", "required": true, "weight": 0.25},
    {"name": "Architecture Review", "required": true, "weight": 0.25},
    {"name": "Performance Benchmark", "required": true, "weight": 0.25}
  ],
  "assessor": "certification-engine",
  "metadata": {}
}
```

#### 3.10.4 Update Certification

```
PUT /api/v1/certifications/{id}
```

#### 3.10.5 Partial Update Certification

```
PATCH /api/v1/certifications/{id}
```

#### 3.10.6 Delete Certification

```
DELETE /api/v1/certifications/{id}
```

#### 3.10.7 Search Certifications

```
POST /api/v1/certifications/search
```

#### 3.10.8 Bulk Operations

```
POST /api/v1/certifications/bulk
```

#### 3.10.9 Sync Certification

```
POST /api/v1/certifications/{id}/sync
```

#### 3.10.10 Verify Certification

```
POST /api/v1/certifications/{id}/verify
```

---

### 3.11 Dependency Entity

**Resource**: `/api/v1/dependencies`

#### 3.11.1 List Dependencies

```
GET /api/v1/dependencies
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `repository` | uuid | Filter by owning repository |
| `type` | enum | Filter by type: `platform`, `external_package`, `external_service`, `shared_sdk`, `protocol`, `standard` |
| `critical` | boolean | Filter by critical flag |

#### 3.11.2 Get Dependency

```
GET /api/v1/dependencies/{id}
```

#### 3.11.3 Create Dependency

```
POST /api/v1/dependencies
```

**Request Body**:
```json
{
  "name": "postgresql",
  "type": "external_package",
  "versionConstraint": ">=16.0.0,<17.0.0",
  "source": "docker",
  "repository": "repo-uuid",
  "optional": false,
  "critical": true,
  "metadata": {}
}
```

#### 3.11.4 Update Dependency

```
PUT /api/v1/dependencies/{id}
```

#### 3.11.5 Partial Update Dependency

```
PATCH /api/v1/dependencies/{id}
```

#### 3.11.6 Delete Dependency

```
DELETE /api/v1/dependencies/{id}
```

#### 3.11.7 Search Dependencies

```
POST /api/v1/dependencies/search
```

#### 3.11.8 Bulk Operations

```
POST /api/v1/dependencies/bulk
```

#### 3.11.9 Sync Dependency

```
POST /api/v1/dependencies/{id}/sync
```

#### 3.11.10 Verify Dependency

```
POST /api/v1/dependencies/{id}/verify
```

---

### 3.12 Relationship Entity

**Resource**: `/api/v1/relationships`

#### 3.12.1 List Relationships

```
GET /api/v1/relationships
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `source` | uuid | Filter by source entity |
| `target` | uuid | Filter by target entity |
| `type` | enum | Filter by type: `owns`, `depends-on`, `implements`, `publishes`, `consumes`, `exposes`, `uses`, `extends`, `triggers`, `certifies` |

#### 3.12.2 Get Relationship

```
GET /api/v1/relationships/{id}
```

#### 3.12.3 Create Relationship

```
POST /api/v1/relationships
```

**Request Body**:
```json
{
  "source": "entity-uuid-1",
  "target": "entity-uuid-2",
  "type": "owns",
  "weight": 1.0,
  "metadata": {}
}
```

#### 3.12.4 Update Relationship

```
PUT /api/v1/relationships/{id}
```

#### 3.12.5 Partial Update Relationship

```
PATCH /api/v1/relationships/{id}
```

#### 3.12.6 Delete Relationship

```
DELETE /api/v1/relationships/{id}
```

#### 3.12.7 Search Relationships

```
POST /api/v1/relationships/search
```

#### 3.12.8 Bulk Operations

```
POST /api/v1/relationships/bulk
```

#### 3.12.9 Sync Relationship

```
POST /api/v1/relationships/{id}/sync
```

#### 3.12.10 Verify Relationship

```
POST /api/v1/relationships/{id}/verify
```

---

### 3.13 Patient Entity

**Resource**: `/api/v1/patients`

#### 3.13.1 List Patients

```
GET /api/v1/patients
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | enum | Filter by status: `active`, `inactive`, `deceased`, `transferred` |
| `gender` | enum | Filter by gender |
| `facility` | uuid | Filter by facility |
| `dateOfBirth` | date | Filter by DOB range |

#### 3.13.2 Get Patient

```
GET /api/v1/patients/{id}
```

#### 3.13.3 Create Patient

```
POST /api/v1/patients
```

**Request Body**:
```json
{
  "medicalRecordNumber": "MRN-2026-0001",
  "firstName": "Ahmed",
  "lastName": "Al-Rashid",
  "dateOfBirth": "1990-05-15",
  "gender": "male",
  "nationalId": "IQ-1234567890",
  "contactInfo": {
    "phone": "+964-770-123-4567",
    "email": "ahmed@example.com",
    "address": {
      "street": "123 Main St",
      "city": "Baghdad",
      "province": "Baghdad",
      "country": "IQ"
    }
  },
  "emergencyContact": {
    "name": "Fatima Al-Rashid",
    "relationship": "spouse",
    "phone": "+964-770-987-6543"
  },
  "insurance": {
    "provider": "Health Ministry Insurance",
    "policyNumber": "HMI-2026-001",
    "expiryDate": "2027-12-31"
  },
  "allergies": ["penicillin", "sulfa"],
  "bloodType": "O+",
  "facility": "facility-uuid",
  "metadata": {}
}
```

#### 3.13.4 Update Patient

```
PUT /api/v1/patients/{id}
```

#### 3.13.5 Partial Update Patient

```
PATCH /api/v1/patients/{id}
```

#### 3.13.6 Delete Patient

```
DELETE /api/v1/patients/{id}
```

**Note**: Soft delete only. Patient records are never physically deleted.

#### 3.13.7 Search Patients

```
POST /api/v1/patients/search
```

**Request Body**:
```json
{
  "query": "Ahmed Al-Rashid",
  "filters": {
    "status": ["active"],
    "facility": ["facility-uuid"]
  },
  "sort": "lastName:asc",
  "limit": 20
}
```

#### 3.13.8 Bulk Operations

```
POST /api/v1/patients/bulk
```

#### 3.13.9 Sync Patient

```
POST /api/v1/patients/{id}/sync
```

#### 3.13.10 Verify Patient

```
POST /api/v1/patients/{id}/verify
```

---

### 3.14 Sample Entity

**Resource**: `/api/v1/samples`

#### 3.14.1 List Samples

```
GET /api/v1/samples
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | enum | Filter by status: `collected`, `received`, `processing`, `analyzed`, `reported`, `archived`, `rejected` |
| `type` | enum | Filter by sample type: `blood`, `urine`, `saliva`, `tissue`, `stool`, `csf`, `other` |
| `patient` | uuid | Filter by patient |
| `facility` | uuid | Filter by facility |

#### 3.14.2 Get Sample

```
GET /api/v1/samples/{id}
```

#### 3.14.3 Create Sample

```
POST /api/v1/samples
```

**Request Body**:
```json
{
  "sampleId": "SMP-2026-0001",
  "patient": "patient-uuid",
  "type": "blood",
  "collectedAt": "2026-06-25T08:30:00Z",
  "collectedBy": "user-uuid",
  "facility": "facility-uuid",
  "collectionSite": "Left antecubital vein",
  "volume": "10ml",
  "containerType": "EDTA tube",
  "fastingRequired": false,
  "priority": "routine",
  "requestedTests": ["CBC", "BMP"],
  "chainOfCustody": [
    {
      "action": "collected",
      "by": "user-uuid",
      "at": "2026-06-25T08:30:00Z",
      "location": "Ward 3"
    }
  ],
  "metadata": {}
}
```

#### 3.14.4 Update Sample

```
PUT /api/v1/samples/{id}
```

#### 3.14.5 Partial Update Sample

```
PATCH /api/v1/samples/{id}
```

#### 3.14.6 Delete Sample

```
DELETE /api/v1/samples/{id}
```

**Note**: Samples are never deleted once in the system.

#### 3.14.7 Search Samples

```
POST /api/v1/samples/search
```

#### 3.14.8 Bulk Operations

```
POST /api/v1/samples/bulk
```

#### 3.14.9 Sync Sample

```
POST /api/v1/samples/{id}/sync
```

#### 3.14.10 Verify Sample

```
POST /api/v1/samples/{id}/verify
```

---

### 3.15 Test Order Entity

**Resource**: `/api/v1/test-orders`

#### 3.15.1 List Test Orders

```
GET /api/v1/test-orders
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | enum | Filter by status: `pending`, `in_progress`, `completed`, `cancelled` |
| `patient` | uuid | Filter by patient |
| `sample` | uuid | Filter by sample |
| `priority` | enum | Filter by priority: `stat`, `urgent`, `routine` |

#### 3.15.2 Get Test Order

```
GET /api/v1/test-orders/{id}
```

#### 3.15.3 Create Test Order

```
POST /api/v1/test-orders
```

**Request Body**:
```json
{
  "patient": "patient-uuid",
  "sample": "sample-uuid",
  "orderedBy": "user-uuid",
  "priority": "routine",
  "tests": [
    {
      "testCode": "CBC",
      "testName": "Complete Blood Count",
      "loincCode": "58410-2"
    },
    {
      "testCode": "BMP",
      "testName": "Basic Metabolic Panel",
      "loincCode": "51901-6"
    }
  ],
  "clinicalInfo": "Routine checkup",
  "diagnosis": "Z00.00",
  "metadata": {}
}
```

#### 3.15.4 Update Test Order

```
PUT /api/v1/test-orders/{id}
```

#### 3.15.5 Partial Update Test Order

```
PATCH /api/v1/test-orders/{id}
```

#### 3.15.6 Delete Test Order

```
DELETE /api/v1/test-orders/{id}
```

#### 3.15.7 Search Test Orders

```
POST /api/v1/test-orders/search
```

#### 3.15.8 Bulk Operations

```
POST /api/v1/test-orders/bulk
```

#### 3.15.9 Sync Test Order

```
POST /api/v1/test-orders/{id}/sync
```

#### 3.15.10 Verify Test Order

```
POST /api/v1/test-orders/{id}/verify
```

---

### 3.16 Test Result Entity

**Resource**: `/api/v1/test-results`

#### 3.16.1 List Test Results

```
GET /api/v1/test-results
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | enum | Filter by status: `preliminary`, `final`, `corrected`, `cancelled` |
| `patient` | uuid | Filter by patient |
| `sample` | uuid | Filter by sample |
| `testOrder` | uuid | Filter by test order |
| `abnormal` | boolean | Filter by abnormal results |

#### 3.16.2 Get Test Result

```
GET /api/v1/test-results/{id}
```

#### 3.16.3 Create Test Result

```
POST /api/v1/test-results
```

**Request Body**:
```json
{
  "testOrder": "test-order-uuid",
  "sample": "sample-uuid",
  "patient": "patient-uuid",
  "testCode": "CBC",
  "testName": "Complete Blood Count",
  "status": "final",
  "results": [
    {
      "analyte": "WBC",
      "value": "7.5",
      "unit": "10^3/uL",
      "referenceRange": "4.5-11.0",
      "flag": "normal",
      "method": "flow cytometry",
      "instrument": "Cobas 8800"
    },
    {
      "analyte": "RBC",
      "value": "5.2",
      "unit": "10^6/uL",
      "referenceRange": "4.5-5.5",
      "flag": "normal",
      "method": "impedance",
      "instrument": "Cobas 8800"
    }
  ],
  "performedBy": "user-uuid",
  "verifiedBy": "user-uuid",
  "performedAt": "2026-06-25T10:00:00Z",
  "verifiedAt": "2026-06-25T10:30:00Z",
  "comments": "",
  "metadata": {}
}
```

#### 3.16.4 Update Test Result

```
PUT /api/v1/test-results/{id}
```

#### 3.16.5 Partial Update Test Result

```
PATCH /api/v1/test-results/{id}
```

#### 3.16.6 Delete Test Result

```
DELETE /api/v1/test-results/{id}
```

#### 3.16.7 Search Test Results

```
POST /api/v1/test-results/search
```

#### 3.16.8 Bulk Operations

```
POST /api/v1/test-results/bulk
```

#### 3.16.9 Sync Test Result

```
POST /api/v1/test-results/{id}/sync
```

#### 3.16.10 Verify Test Result

```
POST /api/v1/test-results/{id}/verify
```

---

### 3.17 User Entity

**Resource**: `/api/v1/users`

#### 3.17.1 List Users

```
GET /api/v1/users
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | enum | Filter by status: `active`, `inactive`, `locked`, `pending` |
| `role` | uuid | Filter by role |
| `facility` | uuid | Filter by facility |
| `department` | string | Filter by department |

#### 3.17.2 Get User

```
GET /api/v1/users/{id}
```

#### 3.17.3 Create User

```
POST /api/v1/users
```

**Request Body**:
```json
{
  "username": "ahmed.rashid",
  "email": "ahmed@health.gov.iq",
  "firstName": "Ahmed",
  "lastName": "Al-Rashid",
  "phone": "+964-770-123-4567",
  "roles": ["role-uuid-1", "role-uuid-2"],
  "facility": "facility-uuid",
  "department": "laboratory",
  "title": "Senior Lab Technician",
  "licenseNumber": "LAB-2026-001",
  "licenseExpiry": "2027-12-31",
  "metadata": {}
}
```

#### 3.17.4 Update User

```
PUT /api/v1/users/{id}
```

#### 3.17.5 Partial Update User

```
PATCH /api/v1/users/{id}
```

#### 3.17.6 Delete User

```
DELETE /api/v1/users/{id}
```

#### 3.17.7 Search Users

```
POST /api/v1/users/search
```

#### 3.17.8 Bulk Operations

```
POST /api/v1/users/bulk
```

#### 3.17.9 Sync User

```
POST /api/v1/users/{id}/sync
```

#### 3.17.10 Verify User

```
POST /api/v1/users/{id}/verify
```

---

### 3.18 Role Entity

**Resource**: `/api/v1/roles`

#### 3.18.1 List Roles

```
GET /api/v1/roles
```

#### 3.18.2 Get Role

```
GET /api/v1/roles/{id}
```

#### 3.18.3 Create Role

```
POST /api/v1/roles
```

**Request Body**:
```json
{
  "name": "lab_techician",
  "description": "Laboratory Technician with result entry access",
  "permissions": [
    "sample.create",
    "sample.read",
    "sample.update",
    "test_order.read",
    "test_result.create",
    "test_result.read"
  ],
  "hierarchy": 2,
  "metadata": {}
}
```

#### 3.18.4 Update Role

```
PUT /api/v1/roles/{id}
```

#### 3.18.5 Partial Update Role

```
PATCH /api/v1/roles/{id}
```

#### 3.18.6 Delete Role

```
DELETE /api/v1/roles/{id}
```

#### 3.18.7 Search Roles

```
POST /api/v1/roles/search
```

#### 3.18.8 Bulk Operations

```
POST /api/v1/roles/bulk
```

#### 3.18.9 Sync Role

```
POST /api/v1/roles/{id}/sync
```

#### 3.18.10 Verify Role

```
POST /api/v1/roles/{id}/verify
```

---

### 3.19 Facility Entity

**Resource**: `/api/v1/facilities`

#### 3.19.1 List Facilities

```
GET /api/v1/facilities
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | enum | Filter by type: `hospital`, `laboratory`, `clinic`, `pharmacy`, `warehouse`, `office` |
| `status` | enum | Filter by status |
| `province` | string | Filter by province |

#### 3.19.2 Get Facility

```
GET /api/v1/facilities/{id}
```

#### 3.19.3 Create Facility

```
POST /api/v1/facilities
```

**Request Body**:
```json
{
  "name": "Central Laboratory - Baghdad",
  "code": "LAB-BAG-001",
  "type": "laboratory",
  "status": "active",
  "address": {
    "street": "456 Health Ave",
    "city": "Baghdad",
    "province": "Baghdad",
    "country": "IQ",
    "postalCode": "10001"
  },
  "contactInfo": {
    "phone": "+964-1-234-5678",
    "email": "central.lab@health.gov.iq",
    "fax": "+964-1-234-5679"
  },
  "capacity": {
    "beds": 0,
    "dailySamples": 500,
    "staff": 25
  },
  "accreditation": {
    "body": "CAP",
    "number": "CAP-2026-001",
    "expiryDate": "2027-12-31"
  },
  "operatingHours": {
    "weekday": "07:00-17:00",
    "weekend": "08:00-14:00"
  },
  "metadata": {}
}
```

#### 3.19.4 Update Facility

```
PUT /api/v1/facilities/{id}
```

#### 3.19.5 Partial Update Facility

```
PATCH /api/v1/facilities/{id}
```

#### 3.19.6 Delete Facility

```
DELETE /api/v1/facilities/{id}
```

#### 3.19.7 Search Facilities

```
POST /api/v1/facilities/search
```

#### 3.19.8 Bulk Operations

```
POST /api/v1/facilities/bulk
```

#### 3.19.9 Sync Facility

```
POST /api/v1/facilities/{id}/sync
```

#### 3.19.10 Verify Facility

```
POST /api/v1/facilities/{id}/verify
```

---

### 3.20 Credential Entity

**Resource**: `/api/v1/credentials`

#### 3.20.1 List Credentials

```
GET /api/v1/credentials
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | enum | Filter by type: `license`, `certificate`, `diploma`, `certification` |
| `status` | enum | Filter by status: `active`, `expired`, `revoked`, `pending` |
| `holder` | uuid | Filter by credential holder |

#### 3.20.2 Get Credential

```
GET /api/v1/credentials/{id}
```

#### 3.20.3 Create Credential

```
POST /api/v1/credentials
```

**Request Body**:
```json
{
  "holder": "user-uuid",
  "type": "license",
  "name": "Laboratory Technician License",
  "issuer": "Ministry of Health",
  "licenseNumber": "LAB-2026-001",
  "issuedDate": "2026-01-01",
  "expiryDate": "2027-12-31",
  "scope": ["hematology", "chemistry"],
  "documentUrl": "credentials/license-001.pdf",
  "verificationCode": "VER-2026-001",
  "metadata": {}
}
```

#### 3.20.4 Update Credential

```
PUT /api/v1/credentials/{id}
```

#### 3.20.5 Partial Update Credential

```
PATCH /api/v1/credentials/{id}
```

#### 3.20.6 Delete Credential

```
DELETE /api/v1/credentials/{id}
```

#### 3.20.7 Search Credentials

```
POST /api/v1/credentials/search
```

#### 3.20.8 Bulk Operations

```
POST /api/v1/credentials/bulk
```

#### 3.20.9 Sync Credential

```
POST /api/v1/credentials/{id}/sync
```

#### 3.20.10 Verify Credential

```
POST /api/v1/credentials/{id}/verify
```

---

### 3.21 Correspondence Entity

**Resource**: `/api/v1/correspondences`

#### 3.21.1 List Correspondences

```
GET /api/v1/correspondences
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | enum | Filter by type: `incoming`, `outgoing`, `internal` |
| `status` | enum | Filter by status: `draft`, `sent`, `received`, `archived` |
| `classification` | enum | Filter by classification: `public`, `internal`, `confidential`, `restricted` |
| `facility` | uuid | Filter by facility |

#### 3.21.2 Get Correspondence

```
GET /api/v1/correspondences/{id}
```

#### 3.21.3 Create Correspondence

```
POST /api/v1/correspondences
```

**Request Body**:
```json
{
  "referenceNumber": "COR-2026-0001",
  "type": "outgoing",
  "classification": "internal",
  "subject": "Monthly Laboratory Performance Report",
  "body": "Please find attached the monthly performance report...",
  "from": {
    "user": "user-uuid",
    "facility": "facility-uuid"
  },
  "to": [
    {
      "name": "Dr. Hassan Ali",
      "title": "Director of Laboratories",
      "facility": "facility-uuid"
    }
  ],
  "attachments": [
    {
      "name": "performance-report-june.pdf",
      "url": "attachments/report-001.pdf",
      "size": 1024000
    }
  ],
  "responseRequired": true,
  "responseDeadline": "2026-07-10T00:00:00Z",
  "metadata": {}
}
```

#### 3.21.4 Update Correspondence

```
PUT /api/v1/correspondences/{id}
```

#### 3.21.5 Partial Update Correspondence

```
PATCH /api/v1/correspondences/{id}
```

#### 3.21.6 Delete Correspondence

```
DELETE /api/v1/correspondences/{id}
```

#### 3.21.7 Search Correspondences

```
POST /api/v1/correspondences/search
```

#### 3.21.8 Bulk Operations

```
POST /api/v1/correspondences/bulk
```

#### 3.21.9 Sync Correspondence

```
POST /api/v1/correspondences/{id}/sync
```

#### 3.21.10 Verify Correspondence

```
POST /api/v1/correspondences/{id}/verify
```

---

### 3.22 Inventory Item Entity

**Resource**: `/api/v1/inventory-items`

#### 3.22.1 List Inventory Items

```
GET /api/v1/inventory-items
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | enum | Filter by category: `reagent`, `consumable`, `equipment`, `supplies` |
| `status` | enum | Filter by status: `available`, `low_stock`, `out_of_stock`, `expired`, `reserved` |
| `facility` | uuid | Filter by facility |

#### 3.22.2 Get Inventory Item

```
GET /api/v1/inventory-items/{id}
```

#### 3.22.3 Create Inventory Item

```
POST /api/v1/inventory-items
```

**Request Body**:
```json
{
  "itemCode": "REAGENT-001",
  "name": "CBC Reagent Pack",
  "category": "reagent",
  "description": "Reagent pack for Complete Blood Count analysis",
  "manufacturer": "Roche",
  "catalogNumber": "RBC-1234",
  "lotNumber": "LOT-2026-001",
  "quantity": 100,
  "unit": "tests",
  "minimumStock": 20,
  "maximumStock": 200,
  "unitCost": 2.50,
  "currency": "IQD",
  "storageConditions": "2-8°C",
  "expiryDate": "2027-06-30",
  "facility": "facility-uuid",
  "location": "Cold Storage Room A",
  "compatibleInstruments": ["Cobas 8800"],
  "metadata": {}
}
```

#### 3.22.4 Update Inventory Item

```
PUT /api/v1/inventory-items/{id}
```

#### 3.22.5 Partial Update Inventory Item

```
PATCH /api/v1/inventory-items/{id}
```

#### 3.22.6 Delete Inventory Item

```
DELETE /api/v1/inventory-items/{id}
```

#### 3.22.7 Search Inventory Items

```
POST /api/v1/inventory-items/search
```

#### 3.22.8 Bulk Operations

```
POST /api/v1/inventory-items/bulk
```

#### 3.22.9 Sync Inventory Item

```
POST /api/v1/inventory-items/{id}/sync
```

#### 3.22.10 Verify Inventory Item

```
POST /api/v1/inventory-items/{id}/verify
```

---

### 3.23 Attendance Record Entity

**Resource**: `/api/v1/attendance-records`

#### 3.23.1 List Attendance Records

```
GET /api/v1/attendance-records
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `user` | uuid | Filter by user |
| `status` | enum | Filter by status: `present`, `absent`, `late`, `half_day`, `leave` |
| `date` | date | Filter by date |
| `facility` | uuid | Filter by facility |

#### 3.23.2 Get Attendance Record

```
GET /api/v1/attendance-records/{id}
```

#### 3.23.3 Create Attendance Record

```
POST /api/v1/attendance-records
```

**Request Body**:
```json
{
  "user": "user-uuid",
  "date": "2026-06-25",
  "checkIn": "2026-06-25T07:55:00Z",
  "checkOut": "2026-06-25T16:05:00Z",
  "status": "present",
  "overtime": 0,
  "facility": "facility-uuid",
  "notes": "",
  "metadata": {}
}
```

#### 3.23.4 Update Attendance Record

```
PUT /api/v1/attendance-records/{id}
```

#### 3.23.5 Partial Update Attendance Record

```
PATCH /api/v1/attendance-records/{id}
```

#### 3.23.6 Delete Attendance Record

```
DELETE /api/v1/attendance-records/{id}
```

#### 3.23.7 Search Attendance Records

```
POST /api/v1/attendance-records/search
```

#### 3.23.8 Bulk Operations

```
POST /api/v1/attendance-records/bulk
```

#### 3.23.9 Sync Attendance Record

```
POST /api/v1/attendance-records/{id}/sync
```

#### 3.23.10 Verify Attendance Record

```
POST /api/v1/attendance-records/{id}/verify
```

---

### 3.24 Leave Request Entity

**Resource**: `/api/v1/leave-requests`

#### 3.24.1 List Leave Requests

```
GET /api/v1/leave-requests
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `user` | uuid | Filter by user |
| `type` | enum | Filter by type: `annual`, `sick`, `maternity`, `paternity`, `unpaid`, `other` |
| `status` | enum | Filter by status: `pending`, `approved`, `rejected`, `cancelled` |

#### 3.24.2 Get Leave Request

```
GET /api/v1/leave-requests/{id}
```

#### 3.24.3 Create Leave Request

```
POST /api/v1/leave-requests
```

**Request Body**:
```json
{
  "user": "user-uuid",
  "type": "annual",
  "startDate": "2026-07-01",
  "endDate": "2026-07-05",
  "reason": "Family vacation",
  "replacement": "user-uuid-2",
  "metadata": {}
}
```

#### 3.24.4 Update Leave Request

```
PUT /api/v1/leave-requests/{id}
```

#### 3.24.5 Partial Update Leave Request

```
PATCH /api/v1/leave-requests/{id}
```

#### 3.24.6 Delete Leave Request

```
DELETE /api/v1/leave-requests/{id}
```

#### 3.24.7 Search Leave Requests

```
POST /api/v1/leave-requests/search
```

#### 3.24.8 Bulk Operations

```
POST /api/v1/leave-requests/bulk
```

#### 3.24.9 Sync Leave Request

```
POST /api/v1/leave-requests/{id}/sync
```

#### 3.24.10 Verify Leave Request

```
POST /api/v1/leave-requests/{id}/verify
```

---

### 3.25 Training Record Entity

**Resource**: `/api/v1/training-records`

#### 3.25.1 List Training Records

```
GET /api/v1/training-records
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `user` | uuid | Filter by user |
| `status` | enum | Filter by status: `enrolled`, `in_progress`, `completed`, `failed`, `expired` |
| `course` | string | Filter by course name |

#### 3.25.2 Get Training Record

```
GET /api/v1/training-records/{id}
```

#### 3.25.3 Create Training Record

```
POST /api/v1/training-records
```

**Request Body**:
```json
{
  "user": "user-uuid",
  "course": "Biosafety Level 3 Training",
  "courseCode": "BSL-3-001",
  "provider": "WHO",
  "enrolledAt": "2026-06-01T00:00:00Z",
  "completedAt": "2026-06-15T00:00:00Z",
  "expiryDate": "2027-06-15",
  "status": "completed",
  "score": 92,
  "certificateUrl": "certs/bsl3-001.pdf",
  "metadata": {}
}
```

#### 3.25.4 Update Training Record

```
PUT /api/v1/training-records/{id}
```

#### 3.25.5 Partial Update Training Record

```
PATCH /api/v1/training-records/{id}
```

#### 3.25.6 Delete Training Record

```
DELETE /api/v1/training-records/{id}
```

#### 3.25.7 Search Training Records

```
POST /api/v1/training-records/search
```

#### 3.25.8 Bulk Operations

```
POST /api/v1/training-records/bulk
```

#### 3.25.9 Sync Training Record

```
POST /api/v1/training-records/{id}/sync
```

#### 3.25.10 Verify Training Record

```
POST /api/v1/training-records/{id}/verify
```

---

### 3.26 Audit Event Entity

**Resource**: `/api/v1/audit-events`

#### 3.26.1 List Audit Events

```
GET /api/v1/audit-events
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `entityType` | string | Filter by entity type |
| `entityId` | uuid | Filter by entity ID |
| `action` | enum | Filter by action: `create`, `read`, `update`, `delete`, `login`, `logout`, `export`, `print` |
| `actor` | uuid | Filter by actor |
| `result` | enum | Filter by result: `success`, `failure`, `denied` |
| `from` | datetime | Filter by time range start |
| `to` | datetime | Filter by time range end |

#### 3.26.2 Get Audit Event

```
GET /api/v1/audit-events/{id}
```

#### 3.26.3 Search Audit Events

```
POST /api/v1/audit-events/search
```

#### 3.26.4 Export Audit Events

```
POST /api/v1/audit-events/export
```

**Request Body**:
```json
{
  "format": "csv",
  "filters": {
    "from": "2026-01-01T00:00:00Z",
    "to": "2026-06-30T23:59:59Z",
    "entityType": "patient"
  }
}
```

**Response 200**:
```json
{
  "data": {
    "downloadUrl": "/exports/audit-2026.csv",
    "expiresAt": "2026-06-26T10:00:00Z",
    "recordCount": 15420
  }
}
```

---

### 3.27 Notification Entity

**Resource**: `/api/v1/notifications`

#### 3.27.1 List Notifications

```
GET /api/v1/notifications
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `user` | uuid | Filter by recipient |
| `type` | enum | Filter by type: `info`, `warning`, `error`, `success` |
| `read` | boolean | Filter by read status |

#### 3.27.2 Get Notification

```
GET /api/v1/notifications/{id}
```

#### 3.27.3 Create Notification

```
POST /api/v1/notifications
```

**Request Body**:
```json
{
  "recipient": "user-uuid",
  "type": "warning",
  "title": "Low Stock Alert",
  "message": "CBC Reagent Pack stock is below minimum threshold",
  "entityType": "inventory_item",
  "entityId": "item-uuid",
  "actionUrl": "/inventory/item-uuid",
  "channels": ["in_app", "email"],
  "metadata": {}
}
```

#### 3.27.4 Update Notification

```
PUT /api/v1/notifications/{id}
```

#### 3.27.5 Partial Update Notification

```
PATCH /api/v1/notifications/{id}
```

#### 3.27.6 Delete Notification

```
DELETE /api/v1/notifications/{id}
```

#### 3.27.7 Search Notifications

```
POST /api/v1/notifications/search
```

#### 3.27.8 Bulk Operations

```
POST /api/v1/notifications/bulk
```

#### 3.27.9 Sync Notification

```
POST /api/v1/notifications/{id}/sync
```

#### 3.27.10 Verify Notification

```
POST /api/v1/notifications/{id}/verify
```

---

### 3.28 Report Entity

**Resource**: `/api/v1/reports`

#### 3.28.1 List Reports

```
GET /api/v1/reports
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | enum | Filter by type: `daily`, `weekly`, `monthly`, `quarterly`, `annual`, `adhoc` |
| `status` | enum | Filter by status: `generating`, `completed`, `failed` |
| `facility` | uuid | Filter by facility |

#### 3.28.2 Get Report

```
GET /api/v1/reports/{id}
```

#### 3.28.3 Create Report

```
POST /api/v1/reports
```

**Request Body**:
```json
{
  "title": "Monthly Laboratory Performance Report",
  "type": "monthly",
  "template": "monthly_performance",
  "parameters": {
    "month": 6,
    "year": 2026,
    "facility": "facility-uuid"
  },
  "requestedBy": "user-uuid",
  "format": "pdf",
  "metadata": {}
}
```

#### 3.28.4 Update Report

```
PUT /api/v1/reports/{id}
```

#### 3.28.5 Partial Update Report

```
PATCH /api/v1/reports/{id}
```

#### 3.28.6 Delete Report

```
DELETE /api/v1/reports/{id}
```

#### 3.28.7 Search Reports

```
POST /api/v1/reports/search
```

#### 3.28.8 Bulk Operations

```
POST /api/v1/reports/bulk
```

#### 3.28.9 Sync Report

```
POST /api/v1/reports/{id}/sync
```

#### 3.28.10 Verify Report

```
POST /api/v1/reports/{id}/verify
```

---

### 3.29 Protocol Entity

**Resource**: `/api/v1/protocols`

#### 3.29.1 List Protocols

```
GET /api/v1/protocols
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | enum | Filter by category: `astm`, `hl7`, `fhir`, `dicom`, `usb`, `serial`, `tcp_ip`, `bluetooth` |
| `status` | enum | Filter by status |

#### 3.29.2 Get Protocol

```
GET /api/v1/protocols/{id}
```

#### 3.29.3 Create Protocol

```
POST /api/v1/protocols
```

**Request Body**:
```json
{
  "name": "ASTM E1394-97",
  "category": "astm",
  "version": "E1394-97",
  "description": "ASTM standard for bidirectional serial communication",
  "specification": {
    "baudRate": 9600,
    "dataBits": 8,
    "stopBits": 1,
    "parity": "none",
    "flowControl": "hardware"
  },
  "supportedTransports": ["serial", "tcp_ip"],
  "documentationUrl": "https://www.astm.org/E1394-97",
  "metadata": {}
}
```

#### 3.29.4 Update Protocol

```
PUT /api/v1/protocols/{id}
```

#### 3.29.5 Partial Update Protocol

```
PATCH /api/v1/protocols/{id}
```

#### 3.29.6 Delete Protocol

```
DELETE /api/v1/protocols/{id}
```

#### 3.29.7 Search Protocols

```
POST /api/v1/protocols/search
```

#### 3.29.8 Bulk Operations

```
POST /api/v1/protocols/bulk
```

#### 3.29.9 Sync Protocol

```
POST /api/v1/protocols/{id}/sync
```

#### 3.29.10 Verify Protocol

```
POST /api/v1/protocols/{id}/verify
```

---

### 3.30 Driver Entity

**Resource**: `/api/v1/drivers`

#### 3.30.1 List Drivers

```
GET /api/v1/drivers
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `protocol` | uuid | Filter by protocol |
| `status` | enum | Filter by status |
| `deviceType` | enum | Filter by compatible device type |

#### 3.30.2 Get Driver

```
GET /api/v1/drivers/{id}
```

#### 3.30.3 Create Driver

```
POST /api/v1/drivers
```

**Request Body**:
```json
{
  "name": "Cobas 8800 ASTM Driver",
  "description": "ASTM driver for Roche Cobas 8800 analyzer",
  "protocol": "protocol-uuid",
  "deviceType": "analyzer",
  "version": "1.0.0",
  "capabilities": ["result_parsing", "order_sending", "status_monitoring"],
  "configurationSchema": {
    "type": "object",
    "properties": {
      "port": {"type": "string"},
      "baudRate": {"type": "integer", "default": 9600}
    }
  },
  "metadata": {}
}
```

#### 3.30.4 Update Driver

```
PUT /api/v1/drivers/{id}
```

#### 3.30.5 Partial Update Driver

```
PATCH /api/v1/drivers/{id}
```

#### 3.30.6 Delete Driver

```
DELETE /api/v1/drivers/{id}
```

#### 3.30.7 Search Drivers

```
POST /api/v1/drivers/search
```

#### 3.30.8 Bulk Operations

```
POST /api/v1/drivers/bulk
```

#### 3.30.9 Sync Driver

```
POST /api/v1/drivers/{id}/sync
```

#### 3.30.10 Verify Driver

```
POST /api/v1/drivers/{id}/verify
```

---

### 3.31 Capability Entity

**Resource**: `/api/v1/capabilities`

#### 3.31.1 List Capabilities

```
GET /api/v1/capabilities
```

#### 3.31.2 Get Capability

```
GET /api/v1/capabilities/{id}
```

#### 3.31.3 Create Capability

```
POST /api/v1/capabilities
```

**Request Body**:
```json
{
  "name": "pcr_amplification",
  "description": "Polymerase Chain Reaction amplification",
  "category": "molecular_diagnostics",
  "parameters": {
    "temperatureRange": {"min": 55, "max": 95, "unit": "celsius"},
    "cycleCount": {"min": 25, "max": 45}
  },
  "metadata": {}
}
```

#### 3.31.4 Update Capability

```
PUT /api/v1/capabilities/{id}
```

#### 3.31.5 Partial Update Capability

```
PATCH /api/v1/capabilities/{id}
```

#### 3.31.6 Delete Capability

```
DELETE /api/v1/capabilities/{id}
```

#### 3.31.7 Search Capabilities

```
POST /api/v1/capabilities/search
```

#### 3.31.8 Bulk Operations

```
POST /api/v1/capabilities/bulk
```

#### 3.31.9 Sync Capability

```
POST /api/v1/capabilities/{id}/sync
```

#### 3.31.10 Verify Capability

```
POST /api/v1/capabilities/{id}/verify
```

---

### 3.32 Schema Entity

**Resource**: `/api/v1/schemas`

#### 3.32.1 List Schemas

```
GET /api/v1/schemas
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | enum | Filter by category: `api_request`, `api_response`, `event_payload`, `database`, `export` |
| `format` | enum | Filter by format: `json_schema`, `avro`, `protobuf`, `openapi` |

#### 3.32.2 Get Schema

```
GET /api/v1/schemas/{id}
```

#### 3.32.3 Create Schema

```
POST /api/v1/schemas
```

**Request Body**:
```json
{
  "name": "patient-created-v1",
  "description": "Schema for patient.created event payload",
  "category": "event_payload",
  "format": "json_schema",
  "version": "1.0.0",
  "schema": {
    "type": "object",
    "required": ["patientId", "createdAt"],
    "properties": {
      "patientId": {"type": "string", "format": "uuid"},
      "medicalRecordNumber": {"type": "string"},
      "createdAt": {"type": "string", "format": "date-time"}
    }
  },
  "metadata": {}
}
```

#### 3.32.4 Update Schema

```
PUT /api/v1/schemas/{id}
```

#### 3.32.5 Partial Update Schema

```
PATCH /api/v1/schemas/{id}
```

#### 3.32.6 Delete Schema

```
DELETE /api/v1/schemas/{id}
```

#### 3.32.7 Search Schemas

```
POST /api/v1/schemas/search
```

#### 3.32.8 Bulk Operations

```
POST /api/v1/schemas/bulk
```

#### 3.32.9 Sync Schema

```
POST /api/v1/schemas/{id}/sync
```

#### 3.32.10 Verify Schema

```
POST /api/v1/schemas/{id}/verify
```

---

### 3.33 Standard Entity

**Resource**: `/api/v1/standards`

#### 3.33.1 List Standards

```
GET /api/v1/standards
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | enum | Filter by category: `hl7`, `fhir`, `loinc`, `snomed_ct`, `astm`, `dicom`, `ihe`, `icd` |
| `status` | enum | Filter by status |

#### 3.33.2 Get Standard

```
GET /api/v1/standards/{id}
```

#### 3.33.3 Create Standard

```
POST /api/v1/standards
```

**Request Body**:
```json
{
  "name": "LOINC",
  "version": "2.76",
  "category": "loinc",
  "description": "Logical Observation Identifiers Names and Codes",
  "organization": "Regenstrief Institute",
  "url": "https://loinc.org",
  "supportedVersions": ["2.74", "2.75", "2.76"],
  "metadata": {}
}
```

#### 3.33.4 Update Standard

```
PUT /api/v1/standards/{id}
```

#### 3.33.5 Partial Update Standard

```
PATCH /api/v1/standards/{id}
```

#### 3.33.6 Delete Standard

```
DELETE /api/v1/standards/{id}
```

#### 3.33.7 Search Standards

```
POST /api/v1/standards/search
```

#### 3.33.8 Bulk Operations

```
POST /api/v1/standards/bulk
```

#### 3.33.9 Sync Standard

```
POST /api/v1/standards/{id}/sync
```

#### 3.33.10 Verify Standard

```
POST /api/v1/standards/{id}/verify
```

---

### 3.34 Configuration Entity

**Resource**: `/api/v1/configurations`

#### 3.34.1 List Configurations

```
GET /api/v1/configurations
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `scope` | enum | Filter by scope: `global`, `facility`, `department`, `user` |
| `module` | string | Filter by module name |

#### 3.34.2 Get Configuration

```
GET /api/v1/configurations/{id}
```

#### 3.34.3 Create Configuration

```
POST /api/v1/configurations
```

**Request Body**:
```json
{
  "key": "lab.result.auto_verify_threshold",
  "value": 0.95,
  "scope": "facility",
  "scopeId": "facility-uuid",
  "module": "lab-results",
  "description": "Confidence threshold for automatic result verification",
  "dataType": "float",
  "minValue": 0.0,
  "maxValue": 1.0,
  "metadata": {}
}
```

#### 3.34.4 Update Configuration

```
PUT /api/v1/configurations/{id}
```

#### 3.34.5 Partial Update Configuration

```
PATCH /api/v1/configurations/{id}
```

#### 3.34.6 Delete Configuration

```
DELETE /api/v1/configurations/{id}
```

#### 3.34.7 Search Configurations

```
POST /api/v1/configurations/search
```

#### 3.34.8 Bulk Operations

```
POST /api/v1/configurations/bulk
```

#### 3.34.9 Sync Configuration

```
POST /api/v1/configurations/{id}/sync
```

#### 3.34.10 Verify Configuration

```
POST /api/v1/configurations/{id}/verify
```

---

### 3.35 Finding Entity

**Resource**: `/api/v1/findings`

#### 3.35.1 List Findings

```
GET /api/v1/findings
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `severity` | enum | Filter by severity: `critical`, `high`, `medium`, `low`, `info` |
| `status` | enum | Filter by status: `open`, `acknowledged`, `in_progress`, `resolved`, `dismissed` |
| `type` | string | Filter by finding type |
| `repository` | uuid | Filter by repository |

#### 3.35.2 Get Finding

```
GET /api/v1/findings/{id}
```

#### 3.35.3 Create Finding

```
POST /api/v1/findings
```

**Request Body**:
```json
{
  "repository": "repo-uuid",
  "type": "security.vulnerability",
  "severity": "high",
  "title": "SQL Injection vulnerability in user search",
  "description": "User search endpoint does not sanitize input",
  "recommendation": "Use parameterized queries",
  "evidence": "GET /api/v1/users?q=' OR 1=1--",
  "source": "automated_scan",
  "metadata": {}
}
```

#### 3.35.4 Update Finding

```
PUT /api/v1/findings/{id}
```

#### 3.35.5 Partial Update Finding

```
PATCH /api/v1/findings/{id}
```

#### 3.35.6 Delete Finding

```
DELETE /api/v1/findings/{id}
```

#### 3.35.7 Search Findings

```
POST /api/v1/findings/search
```

#### 3.35.8 Bulk Operations

```
POST /api/v1/findings/bulk
```

#### 3.35.9 Sync Finding

```
POST /api/v1/findings/{id}/sync
```

#### 3.35.10 Verify Finding

```
POST /api/v1/findings/{id}/verify
```

---

### 3.36 Review Entity

**Resource**: `/api/v1/reviews`

#### 3.36.1 List Reviews

```
GET /api/v1/reviews
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | enum | Filter by type: `architecture`, `security`, `performance`, `quality`, `compliance`, `documentation`, `dependency`, `test_coverage` |
| `status` | enum | Filter by status: `pending`, `in_progress`, `completed`, `cancelled` |
| `repository` | uuid | Filter by repository |

#### 3.36.2 Get Review

```
GET /api/v1/reviews/{id}
```

#### 3.36.3 Create Review

```
POST /api/v1/reviews
```

**Request Body**:
```json
{
  "repository": "repo-uuid",
  "type": "architecture",
  "reviewer": "user-uuid",
  "scope": "full",
  "metadata": {}
}
```

#### 3.36.4 Update Review

```
PUT /api/v1/reviews/{id}
```

#### 3.36.5 Partial Update Review

```
PATCH /api/v1/reviews/{id}
```

#### 3.36.6 Delete Review

```
DELETE /api/v1/reviews/{id}
```

#### 3.36.7 Search Reviews

```
POST /api/v1/reviews/search
```

#### 3.36.8 Bulk Operations

```
POST /api/v1/reviews/bulk
```

#### 3.36.9 Sync Review

```
POST /api/v1/reviews/{id}/sync
```

#### 3.36.10 Verify Review

```
POST /api/v1/reviews/{id}/verify
```

---

### 3.37 Decision Entity

**Resource**: `/api/v1/decisions`

#### 3.37.1 List Decisions

```
GET /api/v1/decisions
```

#### 3.37.2 Get Decision

```
GET /api/v1/decisions/{id}
```

#### 3.37.3 Create Decision

```
POST /api/v1/decisions
```

**Request Body**:
```json
{
  "repository": "repo-uuid",
  "type": "auto",
  "trigger": "certification_failure",
  "decision": "reject_deployment",
  "reason": "Critical security findings unresolved",
  "evidence": ["finding-uuid-1", "finding-uuid-2"],
  "decidedBy": "governance-engine",
  "metadata": {}
}
```

#### 3.37.4 Update Decision

```
PUT /api/v1/decisions/{id}
```

#### 3.37.5 Partial Update Decision

```
PATCH /api/v1/decisions/{id}
```

#### 3.37.6 Delete Decision

```
DELETE /api/v1/decisions/{id}
```

#### 3.37.7 Search Decisions

```
POST /api/v1/decisions/search
```

#### 3.37.8 Bulk Operations

```
POST /api/v1/decisions/bulk
```

#### 3.37.9 Sync Decision

```
POST /api/v1/decisions/{id}/sync
```

#### 3.37.10 Verify Decision

```
POST /api/v1/decisions/{id}/verify
```

---

### 3.38 Recommendation Entity

**Resource**: `/api/v1/recommendations`

#### 3.38.1 List Recommendations

```
GET /api/v1/recommendations
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `priority` | enum | Filter by priority: `critical`, `high`, `medium`, `low` |
| `status` | enum | Filter by status: `pending`, `accepted`, `rejected`, `implemented` |
| `repository` | uuid | Filter by repository |

#### 3.38.2 Get Recommendation

```
GET /api/v1/recommendations/{id}
```

#### 3.38.3 Create Recommendation

```
POST /api/v1/recommendations
```

**Request Body**:
```json
{
  "repository": "repo-uuid",
  "priority": "high",
  "category": "security",
  "title": "Upgrade cryptography library",
  "description": "Current version has known vulnerabilities",
  "recommendation": "Upgrade to cryptography >= 42.0.0",
  "impact": "Eliminates 2 known CVEs",
  "effort": "low",
  "source": "dependency_scan",
  "metadata": {}
}
```

#### 3.38.4 Update Recommendation

```
PUT /api/v1/recommendations/{id}
```

#### 3.38.5 Partial Update Recommendation

```
PATCH /api/v1/recommendations/{id}
```

#### 3.38.6 Delete Recommendation

```
DELETE /api/v1/recommendations/{id}
```

#### 3.38.7 Search Recommendations

```
POST /api/v1/recommendations/search
```

#### 3.38.8 Bulk Operations

```
POST /api/v1/recommendations/bulk
```

#### 3.38.9 Sync Recommendation

```
POST /api/v1/recommendations/{id}/sync
```

#### 3.38.10 Verify Recommendation

```
POST /api/v1/recommendations/{id}/verify
```

---

### 3.39 Exception Entity

**Resource**: `/api/v1/exceptions`

#### 3.39.1 List Exceptions

```
GET /api/v1/exceptions
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | enum | Filter by status: `active`, `expired`, `revoked`, `pending` |
| `repository` | uuid | Filter by repository |
| `findingType` | string | Filter by finding type |

#### 3.39.2 Get Exception

```
GET /api/v1/exceptions/{id}
```

#### 3.39.3 Create Exception

```
POST /api/v1/exceptions
```

**Request Body**:
```json
{
  "repository": "repo-uuid",
  "findingType": "security.vulnerability",
  "reason": "Legacy dependency required for compatibility",
  "approvedBy": "supervisor-uuid",
  "expiryDate": "2026-12-31",
  "conditions": [
    "Must not be exposed to public network",
    "Must be monitored for exploitation attempts"
  ],
  "metadata": {}
}
```

#### 3.39.4 Update Exception

```
PUT /api/v1/exceptions/{id}
```

#### 3.39.5 Partial Update Exception

```
PATCH /api/v1/exceptions/{id}
```

#### 3.39.6 Delete Exception

```
DELETE /api/v1/exceptions/{id}
```

#### 3.39.7 Search Exceptions

```
POST /api/v1/exceptions/search
```

#### 3.39.8 Bulk Operations

```
POST /api/v1/exceptions/bulk
```

#### 3.39.9 Sync Exception

```
POST /api/v1/exceptions/{id}/sync
```

#### 3.39.10 Verify Exception

```
POST /api/v1/exceptions/{id}/verify
```

---

### 3.40 Risk Assessment Entity

**Resource**: `/api/v1/risk-assessments`

#### 3.40.1 List Risk Assessments

```
GET /api/v1/risk-assessments
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | enum | Filter by category: `security`, `operational`, `compliance`, `financial`, `reputational`, `technical`, `strategic` |
| `level` | enum | Filter by level: `critical`, `high`, `medium`, `low`, `negligible` |
| `repository` | uuid | Filter by repository |

#### 3.40.2 Get Risk Assessment

```
GET /api/v1/risk-assessments/{id}
```

#### 3.40.3 Create Risk Assessment

```
POST /api/v1/risk-assessments
```

**Request Body**:
```json
{
  "repository": "repo-uuid",
  "category": "security",
  "title": "Unencrypted data at rest",
  "description": "Database not encrypted at rest",
  "likelihood": "medium",
  "impact": "high",
  "level": "high",
  "mitigation": "Enable PostgreSQL TDE",
  "residualRisk": "low",
  "owner": "user-uuid",
  "metadata": {}
}
```

#### 3.40.4 Update Risk Assessment

```
PUT /api/v1/risk-assessments/{id}
```

#### 3.40.5 Partial Update Risk Assessment

```
PATCH /api/v1/risk-assessments/{id}
```

#### 3.40.6 Delete Risk Assessment

```
DELETE /api/v1/risk-assessments/{id}
```

#### 3.40.7 Search Risk Assessments

```
POST /api/v1/risk-assessments/search
```

#### 3.40.8 Bulk Operations

```
POST /api/v1/risk-assessments/bulk
```

#### 3.40.9 Sync Risk Assessment

```
POST /api/v1/risk-assessments/{id}/sync
```

#### 3.40.10 Verify Risk Assessment

```
POST /api/v1/risk-assessments/{id}/verify
```

---

### 3.41 Compliance Standard Entity

**Resource**: `/api/v1/compliance-standards`

#### 3.41.1 List Compliance Standards

```
GET /api/v1/compliance-standards
```

#### 3.41.2 Get Compliance Standard

```
GET /api/v1/compliance-standards/{id}
```

#### 3.41.3 Create Compliance Standard

```
POST /api/v1/compliance-standards
```

**Request Body**:
```json
{
  "name": "HIPAA",
  "version": "2024",
  "description": "Health Insurance Portability and Accountability Act",
  "category": "data_privacy",
  "jurisdiction": "US",
  "requirements": [
    {
      "id": "HIPAA-164.312",
      "title": "Technical Safeguards",
      "description": "Access control, audit controls, integrity, transmission security",
      "mandatory": true
    }
  ],
  "metadata": {}
}
```

#### 3.41.4 Update Compliance Standard

```
PUT /api/v1/compliance-standards/{id}
```

#### 3.41.5 Partial Update Compliance Standard

```
PATCH /api/v1/compliance-standards/{id}
```

#### 3.41.6 Delete Compliance Standard

```
DELETE /api/v1/compliance-standards/{id}
```

#### 3.41.7 Search Compliance Standards

```
POST /api/v1/compliance-standards/search
```

#### 3.41.8 Bulk Operations

```
POST /api/v1/compliance-standards/bulk
```

#### 3.41.9 Sync Compliance Standard

```
POST /api/v1/compliance-standards/{id}/sync
```

#### 3.41.10 Verify Compliance Standard

```
POST /api/v1/compliance-standards/{id}/verify
```

---

### 3.42 Quality Gate Entity

**Resource**: `/api/v1/quality-gates`

#### 3.42.1 List Quality Gates

```
GET /api/v1/quality-gates
```

#### 3.42.2 Get Quality Gate

```
GET /api/v1/quality-gates/{id}
```

#### 3.42.3 Create Quality Gate

```
POST /api/v1/quality-gates
```

**Request Body**:
```json
{
  "name": "Production Deployment Gate",
  "description": "Quality gate for production deployments",
  "repository": "repo-uuid",
  "criteria": [
    {"name": "Test Coverage", "threshold": 90, "unit": "percent", "mandatory": true},
    {"name": "Critical Findings", "threshold": 0, "unit": "count", "mandatory": true},
    {"name": "High Findings", "threshold": 0, "unit": "count", "mandatory": true},
    {"name": "Build Success", "threshold": 100, "unit": "percent", "mandatory": true},
    {"name": "Security Scan", "threshold": 100, "unit": "percent", "mandatory": true}
  ],
  "metadata": {}
}
```

#### 3.42.4 Update Quality Gate

```
PUT /api/v1/quality-gates/{id}
```

#### 3.42.5 Partial Update Quality Gate

```
PATCH /api/v1/quality-gates/{id}
```

#### 3.42.6 Delete Quality Gate

```
DELETE /api/v1/quality-gates/{id}
```

#### 3.42.7 Search Quality Gates

```
POST /api/v1/quality-gates/search
```

#### 3.42.8 Bulk Operations

```
POST /api/v1/quality-gates/bulk
```

#### 3.42.9 Sync Quality Gate

```
POST /api/v1/quality-gates/{id}/sync
```

#### 3.42.10 Verify Quality Gate

```
POST /api/v1/quality-gates/{id}/verify
```

---

### 3.43 Knowledge Graph Node Entity

**Resource**: `/api/v1/knowledge/nodes`

#### 3.43.1 List Nodes

```
GET /api/v1/knowledge/nodes
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | enum | Filter by node type |
| `status` | enum | Filter by status |

#### 3.43.2 Get Node

```
GET /api/v1/knowledge/nodes/{id}
```

#### 3.43.3 Create Node

```
POST /api/v1/knowledge/nodes
```

**Request Body**:
```json
{
  "type": "repository",
  "name": "platform-core",
  "properties": {
    "language": "python",
    "status": "active"
  },
  "metadata": {}
}
```

#### 3.43.4 Update Node

```
PUT /api/v1/knowledge/nodes/{id}
```

#### 3.43.5 Partial Update Node

```
PATCH /api/v1/knowledge/nodes/{id}
```

#### 3.43.6 Delete Node

```
DELETE /api/v1/knowledge/nodes/{id}
```

#### 3.43.7 Search Nodes

```
POST /api/v1/knowledge/nodes/search
```

#### 3.43.8 Bulk Operations

```
POST /api/v1/knowledge/nodes/bulk
```

#### 3.43.9 Sync Node

```
POST /api/v1/knowledge/nodes/{id}/sync
```

#### 3.43.10 Verify Node

```
POST /api/v1/knowledge/nodes/{id}/verify
```

---

### 3.44 Knowledge Graph Edge Entity

**Resource**: `/api/v1/knowledge/edges`

#### 3.44.1 List Edges

```
GET /api/v1/knowledge/edges
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `source` | uuid | Filter by source node |
| `target` | uuid | Filter by target node |
| `type` | enum | Filter by edge type |

#### 3.44.2 Get Edge

```
GET /api/v1/knowledge/edges/{id}
```

#### 3.44.3 Create Edge

```
POST /api/v1/knowledge/edges
```

**Request Body**:
```json
{
  "source": "node-uuid-1",
  "target": "node-uuid-2",
  "type": "owns",
  "weight": 1.0,
  "metadata": {}
}
```

#### 3.44.4 Update Edge

```
PUT /api/v1/knowledge/edges/{id}
```

#### 3.44.5 Partial Update Edge

```
PATCH /api/v1/knowledge/edges/{id}
```

#### 3.44.6 Delete Edge

```
DELETE /api/v1/knowledge/edges/{id}
```

#### 3.44.7 Search Edges

```
POST /api/v1/knowledge/edges/search
```

#### 3.44.8 Bulk Operations

```
POST /api/v1/knowledge/edges/bulk
```

#### 3.44.9 Sync Edge

```
POST /api/v1/knowledge/edges/{id}/sync
```

#### 3.44.10 Verify Edge

```
POST /api/v1/knowledge/edges/{id}/verify
```

---

### 3.45 Package Entity

**Resource**: `/api/v1/packages`

#### 3.45.1 List Packages

```
GET /api/v1/packages
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | enum | Filter by type: `module`, `library`, `sdk`, `plugin`, `driver` |
| `status` | enum | Filter by status: `available`, `deprecated`, `yanked` |
| `repository` | uuid | Filter by source repository |

#### 3.45.2 Get Package

```
GET /api/v1/packages/{id}
```

#### 3.45.3 Create Package

```
POST /api/v1/packages
```

**Request Body**:
```json
{
  "name": "lab-results-module",
  "version": "1.0.0",
  "type": "module",
  "repository": "repo-uuid",
  "description": "Laboratory results management module",
  "license": "MIT",
  "authors": ["Platform Team"],
  "dependencies": [
    {"name": "platform-core", "version": ">=2.0.0"}
  ],
  "files": [
    {"path": "dist/lab_results-1.0.0.tar.gz", "hash": "sha256:abc123", "size": 1024000}
  ],
  "metadata": {}
}
```

#### 3.45.4 Update Package

```
PUT /api/v1/packages/{id}
```

#### 3.45.5 Partial Update Package

```
PATCH /api/v1/packages/{id}
```

#### 3.45.6 Delete Package

```
DELETE /api/v1/packages/{id}
```

#### 3.45.7 Search Packages

```
POST /api/v1/packages/search
```

#### 3.45.8 Bulk Operations

```
POST /api/v1/packages/bulk
```

#### 3.45.9 Sync Package

```
POST /api/v1/packages/{id}/sync
```

#### 3.45.10 Verify Package

```
POST /api/v1/packages/{id}/verify
```

---

### 3.46 Release Entity

**Resource**: `/api/v1/releases`

#### 3.46.1 List Releases

```
GET /api/v1/releases
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `repository` | uuid | Filter by repository |
| `status` | enum | Filter by status: `draft`, `staging`, `released`, `yanked` |

#### 3.46.2 Get Release

```
GET /api/v1/releases/{id}
```

#### 3.46.3 Create Release

```
POST /api/v1/releases
```

**Request Body**:
```json
{
  "repository": "repo-uuid",
  "version": "2.1.0",
  "name": "Release 2.1.0",
  "description": "Performance improvements and bug fixes",
  "changelog": [
    {"type": "added", "description": "New audit logging feature"},
    {"type": "fixed", "description": "Memory leak in event bus"},
    {"type": "changed", "description": "Improved query performance by 40%"}
  ],
  "packages": ["package-uuid-1", "package-uuid-2"],
  "certification": "cert-uuid",
  "metadata": {}
}
```

#### 3.46.4 Update Release

```
PUT /api/v1/releases/{id}
```

#### 3.46.5 Partial Update Release

```
PATCH /api/v1/releases/{id}
```

#### 3.46.6 Delete Release

```
DELETE /api/v1/releases/{id}
```

#### 3.46.7 Search Releases

```
POST /api/v1/releases/search
```

#### 3.46.8 Bulk Operations

```
POST /api/v1/releases/bulk
```

#### 3.46.9 Sync Release

```
POST /api/v1/releases/{id}/sync
```

#### 3.46.10 Verify Release

```
POST /api/v1/releases/{id}/verify
```

---

### 3.47 Team Entity

**Resource**: `/api/v1/teams`

#### 3.47.1 List Teams

```
GET /api/v1/teams
```

#### 3.47.2 Get Team

```
GET /api/v1/teams/{id}
```

#### 3.47.3 Create Team

```
POST /api/v1/teams
```

**Request Body**:
```json
{
  "name": "Platform Engineering",
  "description": "Core platform development team",
  "members": ["user-uuid-1", "user-uuid-2"],
  "lead": "user-uuid-1",
  "repositories": ["repo-uuid-1"],
  "metadata": {}
}
```

#### 3.47.4 Update Team

```
PUT /api/v1/teams/{id}
```

#### 3.47.5 Partial Update Team

```
PATCH /api/v1/teams/{id}
```

#### 3.47.6 Delete Team

```
DELETE /api/v1/teams/{id}
```

#### 3.47.7 Search Teams

```
POST /api/v1/teams/search
```

#### 3.47.8 Bulk Operations

```
POST /api/v1/teams/bulk
```

#### 3.47.9 Sync Team

```
POST /api/v1/teams/{id}/sync
```

#### 3.47.10 Verify Team

```
POST /api/v1/teams/{id}/verify
```

---

### 3.48 ADR Entity

**Resource**: `/api/v1/adrs`

#### 3.48.1 List ADRs

```
GET /api/v1/adrs
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | enum | Filter by status: `proposed`, `accepted`, `deprecated`, `superseded` |
| `repository` | uuid | Filter by repository |

#### 3.48.2 Get ADR

```
GET /api/v1/adrs/{id}
```

#### 3.48.3 Create ADR

```
POST /api/v1/adrs
```

**Request Body**:
```json
{
  "title": "Use PostgreSQL as primary database",
  "status": "accepted",
  "repository": "repo-uuid",
  "context": "Need a reliable, scalable relational database",
  "decision": "Use PostgreSQL 16 with Apache AGE for graph queries",
  "consequences": [
    "ACID compliance",
    "Graph query capability",
    "Strong community support"
  ],
  "alternatives": [
    {"name": "MySQL", "rejectedReason": "Limited graph support"},
    {"name": "MongoDB", "rejectedReason": "No ACID transactions"}
  ],
  "metadata": {}
}
```

#### 3.48.4 Update ADR

```
PUT /api/v1/adrs/{id}
```

#### 3.48.5 Partial Update ADR

```
PATCH /api/v1/adrs/{id}
```

#### 3.48.6 Delete ADR

```
DELETE /api/v1/adrs/{id}
```

#### 3.48.7 Search ADRs

```
POST /api/v1/adrs/search
```

#### 3.48.8 Bulk Operations

```
POST /api/v1/adrs/bulk
```

#### 3.48.9 Sync ADR

```
POST /api/v1/adrs/{id}/sync
```

#### 3.48.10 Verify ADR

```
POST /api/v1/adrs/{id}/verify
```

---

### 3.49 Event Instance Entity

**Resource**: `/api/v1/event-instances`

#### 3.49.1 List Event Instances

```
GET /api/v1/event-instances
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `eventType` | uuid | Filter by event type |
| `status` | enum | Filter by status: `pending`, `delivered`, `failed`, `expired` |
| `from` | datetime | Filter by time range start |
| `to` | datetime | Filter by time range end |

#### 3.49.2 Get Event Instance

```
GET /api/v1/event-instances/{id}
```

#### 3.49.3 Create Event Instance

```
POST /api/v1/event-instances
```

**Request Body**:
```json
{
  "eventType": "event-type-uuid",
  "source": "platform-core/registry",
  "payload": {
    "repositoryId": "repo-uuid",
    "name": "new-module"
  },
  "correlationId": "corr-uuid",
  "metadata": {}
}
```

#### 3.49.4 Update Event Instance

```
PUT /api/v1/event-instances/{id}
```

#### 3.49.5 Partial Update Event Instance

```
PATCH /api/v1/event-instances/{id}
```

#### 3.49.6 Delete Event Instance

```
DELETE /api/v1/event-instances/{id}
```

#### 3.49.7 Search Event Instances

```
POST /api/v1/event-instances/search
```

#### 3.49.8 Bulk Operations

```
POST /api/v1/event-instances/bulk
```

#### 3.49.9 Sync Event Instance

```
POST /api/v1/event-instances/{id}/sync
```

#### 3.49.10 Verify Event Instance

```
POST /api/v1/event-instances/{id}/verify
```

---

### 3.50 Sync Queue Entity

**Resource**: `/api/v1/sync-queues`

#### 3.50.1 List Sync Queues

```
GET /api/v1/sync-queues
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | enum | Filter by status: `pending`, `processing`, `completed`, `failed` |
| `priority` | enum | Filter by priority: `critical`, `high`, `normal`, `low` |
| `entityType` | string | Filter by entity type |

#### 3.50.2 Get Sync Queue

```
GET /api/v1/sync-queues/{id}
```

#### 3.50.3 Create Sync Queue

```
POST /api/v1/sync-queues
```

**Request Body**:
```json
{
  "entityType": "patient",
  "entityId": "patient-uuid",
  "operation": "update",
  "priority": "high",
  "payload": {
    "firstName": "Updated Name"
  },
  "nodeId": "node-uuid",
  "metadata": {}
}
```

#### 3.50.4 Update Sync Queue

```
PUT /api/v1/sync-queues/{id}
```

#### 3.50.5 Partial Update Sync Queue

```
PATCH /api/v1/sync-queues/{id}
```

#### 3.50.6 Delete Sync Queue

```
DELETE /api/v1/sync-queues/{id}
```

#### 3.50.7 Search Sync Queues

```
POST /api/v1/sync-queues/search
```

#### 3.50.8 Bulk Operations

```
POST /api/v1/sync-queues/bulk
```

#### 3.50.9 Sync Sync Queue

```
POST /api/v1/sync-queues/{id}/sync
```

#### 3.50.10 Verify Sync Queue

```
POST /api/v1/sync-queues/{id}/verify
```

---

### 3.51 Offline Conflict Entity

**Resource**: `/api/v1/offline-conflicts`

#### 3.51.1 List Offline Conflicts

```
GET /api/v1/offline-conflicts
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | enum | Filter by status: `detected`, `resolving`, `resolved`, `escalated` |
| `resolution` | enum | Filter by resolution: `local_wins`, `remote_wins`, `merged`, `manual` |
| `entityType` | string | Filter by entity type |

#### 3.51.2 Get Offline Conflict

```
GET /api/v1/offline-conflicts/{id}
```

#### 3.51.3 Create Offline Conflict

```
POST /api/v1/offline-conflicts
```

**Request Body**:
```json
{
  "entityType": "patient",
  "entityId": "patient-uuid",
  "localVersion": {
    "firstName": "Ahmed",
    "updatedAt": "2026-06-25T08:00:00Z"
  },
  "remoteVersion": {
    "firstName": "Ahmed Ali",
    "updatedAt": "2026-06-25T09:00:00Z"
  },
  "nodeId": "node-uuid",
  "metadata": {}
}
```

#### 3.51.4 Update Offline Conflict

```
PUT /api/v1/offline-conflicts/{id}
```

#### 3.51.5 Partial Update Offline Conflict

```
PATCH /api/v1/offline-conflicts/{id}
```

#### 3.51.6 Delete Offline Conflict

```
DELETE /api/v1/offline-conflicts/{id}
```

#### 3.51.7 Search Offline Conflicts

```
POST /api/v1/offline-conflicts/search
```

#### 3.51.8 Bulk Operations

```
POST /api/v1/offline-conflicts/bulk
```

#### 3.51.9 Sync Offline Conflict

```
POST /api/v1/offline-conflicts/{id}/sync
```

#### 3.51.10 Verify Offline Conflict

```
POST /api/v1/offline-conflicts/{id}/verify
```

---

### 3.52 Telemetry Event Entity

**Resource**: `/api/v1/telemetry-events`

#### 3.52.1 List Telemetry Events

```
GET /api/v1/telemetry-events
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `level` | enum | Filter by level: `info`, `warning`, `error`, `critical` |
| `source` | string | Filter by source module |
| `from` | datetime | Filter by time range start |
| `to` | datetime | Filter by time range end |

#### 3.52.2 Get Telemetry Event

```
GET /api/v1/telemetry-events/{id}
```

#### 3.52.3 Create Telemetry Event

```
POST /api/v1/telemetry-events
```

**Request Body**:
```json
{
  "level": "info",
  "source": "platform-core/registry",
  "message": "Repository registered successfully",
  "traceId": "trace-uuid",
  "spanId": "span-uuid",
  "attributes": {
    "repository.name": "my-module",
    "repository.version": "1.0.0"
  },
  "metadata": {}
}
```

#### 3.52.4 Update Telemetry Event

```
PUT /api/v1/telemetry-events/{id}
```

#### 3.52.5 Partial Update Telemetry Event

```
PATCH /api/v1/telemetry-events/{id}
```

#### 3.52.6 Delete Telemetry Event

```
DELETE /api/v1/telemetry-events/{id}
```

#### 3.52.7 Search Telemetry Events

```
POST /api/v1/telemetry-events/search
```

#### 3.52.8 Bulk Operations

```
POST /api/v1/telemetry-events/bulk
```

#### 3.52.9 Sync Telemetry Event

```
POST /api/v1/telemetry-events/{id}/sync
```

#### 3.52.10 Verify Telemetry Event

```
POST /api/v1/telemetry-events/{id}/verify
```

---

## 4. CROSS-ENTITY OPERATIONS

### 4.1 Entity Relationship Queries

```
GET /api/v1/knowledge/graph/{nodeId}/neighbors
GET /api/v1/knowledge/graph/{nodeId}/path/{targetId}
GET /api/v1/knowledge/graph/{nodeId}/impact
```

### 4.2 Aggregation Endpoints

```
GET /api/v1/analytics/repositories/health
GET /api/v1/analytics/modules/certification-status
GET /api/v1/analytics/governance/compliance-summary
GET /api/v1/analytics/laboratory/turnaround-time
GET /api/v1/analytics/laboratory/sample-volume
GET /api/v1/analytics/laboratory/result-accuracy
```

### 4.3 Bulk Export Endpoints

```
POST /api/v1/export/repositories
POST /api/v1/export/modules
POST /api/v1/export/audit-events
POST /api/v1/export/patients
POST /api/v1/export/samples
POST /api/v1/export/test-results
```

---

## 5. RATE LIMITING

### 5.1 Rate Limit Headers

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Maximum requests per window |
| `X-RateLimit-Remaining` | Remaining requests in window |
| `X-RateLimit-Reset` | Window reset timestamp |
| `Retry-After` | Seconds until retry (when 429) |

### 5.2 Default Rate Limits

| Endpoint Category | Requests/Minute | Burst |
|-------------------|----------------|-------|
| Read Operations | 1000 | 100 |
| Write Operations | 100 | 20 |
| Search Operations | 200 | 30 |
| Bulk Operations | 10 | 5 |
| Export Operations | 5 | 2 |

---

## 6. VERSIONING RULES

### 6.1 API Version Lifecycle

```
v1 (current) → v2 (developing) → v1 (deprecated, 12-month window) → v1 (removed)
```

### 6.2 Breaking Changes

- Removing or renaming fields
- Changing field types
- Changing response structure
- Changing error codes
- Removing endpoints

### 6.3 Non-Breaking Changes

- Adding new optional fields
- Adding new endpoints
- Adding new query parameters
- Adding new enum values
- Increasing rate limits

---

*Document generated as part of NHDOS Canonical Domain Model*
*52 Entity API Contracts defined*
*Constitution Reference: Articles IV, VII, XII*
*Last Updated: 2026-06-25*
