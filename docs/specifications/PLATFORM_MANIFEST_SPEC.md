# PLATFORM MANIFEST SPECIFICATION

**Document**: Platform Manifest Specification
**Version**: 1.0.0
**Date**: 2026-06-25
**Status**: DESIGN
**Constitution Reference**: Article IV — Manifest Standard

---

## 1. OVERVIEW

The Platform Manifest is a machine-readable declaration that every repository must contain. It serves as the primary interface between repositories and Platform-Core, enabling governance, discovery, certification, and interoperability.

**File Location**: `platform-manifest.yaml` (or `platform-manifest.json`) at repository root.

**Purpose**:
- Declare repository identity and purpose
- Document services, APIs, events, and devices
- Declare dependencies and compatibility
- Track certification and maturity status
- Enable automated governance and validation

---

## 2. MANIFEST STRUCTURE

The manifest consists of 12 top-level sections:

```
platform-manifest.yaml
├── manifest          # Manifest metadata
├── identity          # Repository identity
├── purpose           # Repository purpose
├── ownership         # Team/organization ownership
├── runtime           # Runtime requirements
├── maturity          # Maturity and certification
├── services          # Services provided
├── apis              # APIs exposed
├── events            # Events published
├── devices           # Devices supported
├── dependencies      # Dependencies
├── standards         # Healthcare standards
└── compatibility     # Version compatibility
```

---

## 3. SECTION DEFINITIONS

### 3.1 manifest (Required)

Metadata about the manifest itself.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | SemVer | Yes | Manifest schema version (`1.0.0`) |
| `version` | SemVer | Yes | This manifest's version |
| `created_at` | ISO 8601 | Yes | Creation timestamp |
| `updated_at` | ISO 8601 | Yes | Last update timestamp |
| `signed_by` | String | No | Signer identity |
| `signature` | String | No | Cryptographic signature |

### 3.2 identity (Required)

Unique identification of the repository.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Repository name (kebab-case) |
| `slug` | String | Yes | URL-safe identifier |
| `description` | String | Yes | Human-readable purpose |
| `type` | Enum | Yes | `platform-core`, `module`, `adapter`, `sdk`, `tool` |
| `tags` | List[String] | No | Classification tags |

### 3.3 purpose (Required)

Detailed purpose and scope.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `summary` | String | Yes | One-line purpose |
| `scope` | Enum | Yes | `shared`, `module-specific`, `infrastructure` |
| `domains` | List[String] | No | Healthcare domains served |

### 3.4 ownership (Required)

Team and organizational ownership.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `team` | String | Yes | Owning team name |
| `organization` | String | Yes | Owning organization |
| `contact` | String | Yes | Contact email or channel |
| `repository_url` | URL | Yes | Source code URL |
| `documentation_url` | URL | No | Documentation URL |

### 3.5 runtime (Required)

Runtime requirements and environment.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `language` | Enum | Yes | Primary language |
| `version` | String | Yes | Language version requirement |
| `framework` | String | No | Framework name and version |
| `runtime` | String | No | Runtime (e.g., Node.js, Python) |
| `os` | List[String] | No | Supported operating systems |
| `container` | Object | No | Container configuration |
| `environment_variables` | List[Object] | No | Required environment variables |

### 3.6 maturity (Required)

Maturity and certification tracking.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `level` | Enum | Yes | `experimental`, `alpha`, `beta`, `stable`, `mature`, `legacy` |
| `since` | ISO 8601 | Yes | When current maturity was reached |
| `certification` | Object | No | Current certification status |

### 3.7 services (Required if services exist)

List of services provided by this repository.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Service name |
| `type` | Enum | Yes | `core`, `module`, `adapter`, `gateway`, `worker`, `scheduler` |
| `description` | String | Yes | Service purpose |
| `version` | SemVer | Yes | Service version |
| `port` | Integer | No | Default port |
| `health_endpoint` | String | No | Health check path |
| `metrics_endpoint` | String | No | Metrics path |

### 3.8 apis (Required if APIs exist)

List of APIs exposed by this repository.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | API name |
| `type` | Enum | Yes | `rest`, `graphql`, `grpc`, `websocket`, `webhook` |
| `description` | String | Yes | API purpose |
| `version` | SemVer | Yes | API version |
| `base_path` | String | Yes | Base URL path |
| `authentication` | Enum | Yes | `none`, `api_key`, `jwt`, `oauth2`, `mtls` |
| `rate_limit` | Object | No | Rate limiting config |
| `deprecated` | Boolean | No | Is this API deprecated |
| `sunset_date` | ISO 8601 | No | Deprecation sunset date |

### 3.9 events (Required if events exist)

List of events published by this repository.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Event name (dot notation) |
| `type` | Enum | Yes | `domain`, `integration`, `system`, `audit`, `notification` |
| `description` | String | Yes | Event purpose |
| `version` | SemVer | Yes | Event schema version |
| `schema` | String | No | Schema reference |
| `retention_days` | Integer | No | Retention period |

### 3.10 devices (Required if devices exist)

List of devices supported by this repository.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Device name |
| `type` | Enum | Yes | Device category |
| `manufacturer` | String | Yes | Manufacturer |
| `model` | String | Yes | Device model |
| `protocol` | String | Yes | Communication protocol |
| `driver` | String | Yes | Driver reference |

### 3.11 dependencies (Required)

All dependencies (internal and external).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Dependency name |
| `type` | Enum | Yes | `platform`, `external_package`, `external_service`, `shared_sdk`, `protocol`, `standard` |
| `version` | String | Yes | Version constraint |
| `repository` | String | No | Platform repository reference |
| `optional` | Boolean | No | Is this optional |
| `critical` | Boolean | No | Is this critical |

### 3.12 standards (Optional)

Healthcare standards supported.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Standard name (e.g., `HL7`, `FHIR`) |
| `version` | String | Yes | Standard version |
| `level` | Enum | Yes | `full`, `partial`, `planned` |
| `adapter` | String | No | Adapter reference |

### 3.13 compatibility (Required)

Version compatibility matrix.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `platform_core` | String | Yes | Compatible Platform-Core versions |
| `min_platform_core` | String | Yes | Minimum Platform-Core version |
| `breaking_changes` | List[String] | No | Known breaking changes |
| `migration_guide` | URL | No | Migration documentation URL |

---

## 4. YAML EXAMPLES

### 4.1 Platform-Core Repository Manifest

```yaml
manifest:
  schema_version: "1.0.0"
  version: "1.0.0"
  created_at: "2026-06-25T00:00:00Z"
  updated_at: "2026-06-25T00:00:00Z"

identity:
  name: platform-core
  slug: platform-core
  description: "Authoritative governance, runtime, intelligence and integration platform"
  type: platform-core
  tags:
    - governance
    - intelligence
    - runtime
    - core

purpose:
  summary: "Central platform for governance, shared services, and ecosystem intelligence"
  scope: shared
  domains:
    - governance
    - intelligence
    - operations
    - certification

ownership:
  team: platform-engineering
  organization: unified-healthcare-platform
  contact: platform@healthcare.org
  repository_url: "https://github.com/samertts/Platform-Core"
  documentation_url: "https://docs.healthcare-platform.org/platform-core"

runtime:
  language: python
  version: ">=3.11"
  framework: fastapi
  runtime: "python:3.11-slim"
  os:
    - linux
  container:
    base_image: "python:3.11-slim"
    ports:
      - 8080:8080
  environment_variables:
    - name: DATABASE_URL
      required: true
      description: "PostgreSQL connection URL"
    - name: REDIS_URL
      required: true
      description: "Redis connection URL"

maturity:
  level: alpha
  since: "2026-06-25"
  certification:
    level: basic
    status: pending

services:
  - name: governance-service
    type: core
    description: "Platform governance and policy enforcement"
    version: "0.1.0"
    port: 8081
    health_endpoint: "/health"
    metrics_endpoint: "/metrics"
  - name: registry-service
    type: core
    description: "Central registry management"
    version: "0.1.0"
    port: 8082
    health_endpoint: "/health"
    metrics_endpoint: "/metrics"
  - name: certification-service
    type: core
    description: "Module certification and compliance"
    version: "0.1.0"
    port: 8083
    health_endpoint: "/health"
    metrics_endpoint: "/metrics"

apis:
  - name: platform-api
    type: rest
    description: "Platform-Core REST API"
    version: "1.0.0"
    base_path: "/api/v1"
    authentication: jwt
    rate_limit:
      requests_per_minute: 1000
      burst: 100

events:
  - name: platform.manifest.validated
    type: system
    description: "Published when a manifest is validated"
    version: "1.0.0"
    retention_days: 90
  - name: platform.module.certified
    type: audit
    description: "Published when a module passes certification"
    version: "1.0.0"
    retention_days: 365

dependencies:
  - name: fastapi
    type: external_package
    version: ">=0.100.0"
  - name: uvicorn
    type: external_package
    version: ">=0.23.0"
  - name: sqlalchemy
    type: external_package
    version: ">=2.0.0"
  - name: redis
    type: external_package
    version: ">=5.0.0"
  - name: pydantic
    type: external_package
    version: ">=2.0.0"

standards: []

compatibility:
  platform_core: ">=1.0.0"
  min_platform_core: "1.0.0"
  breaking_changes: []
  migration_guide: "https://docs.healthcare-platform.org/platform-core/migration"
```

### 4.2 Module Repository Manifest (Example: Inventory Module)

```yaml
manifest:
  schema_version: "1.0.0"
  version: "1.0.0"
  created_at: "2026-06-25T00:00:00Z"
  updated_at: "2026-06-25T00:00:00Z"

identity:
  name: module-inventory
  slug: module-inventory
  description: "Laboratory inventory management module"
  type: module
  tags:
    - inventory
    - laboratory
    - supplies

purpose:
  summary: "Manage laboratory inventory, stock levels, and reordering"
  scope: module-specific
  domains:
    - laboratory
    - inventory

ownership:
  team: laboratory-features
  organization: unified-healthcare-platform
  contact: lab-features@healthcare.org
  repository_url: "https://github.com/samertts/Module-Inventory"

runtime:
  language: python
  version: ">=3.11"
  framework: fastapi
  runtime: "python:3.11-slim"
  os:
    - linux

maturity:
  level: alpha
  since: "2026-06-25"

services:
  - name: inventory-service
    type: module
    description: "Core inventory management service"
    version: "0.1.0"
    port: 9001
    health_endpoint: "/health"

apis:
  - name: inventory-api
    type: rest
    description: "Inventory CRUD and query API"
    version: "1.0.0"
    base_path: "/api/v1/inventory"
    authentication: jwt
    rate_limit:
      requests_per_minute: 500

events:
  - name: inventory.stock.low
    type: domain
    description: "Published when stock falls below threshold"
    version: "1.0.0"
  - name: inventory.item.received
    type: domain
    description: "Published when inventory item is received"
    version: "1.0.0"

dependencies:
  - name: platform-core
    type: platform
    version: ">=1.0.0"
    critical: true
  - name: module-auth
    type: platform
    version: ">=1.0.0"
    critical: true

standards: []

compatibility:
  platform_core: ">=1.0.0"
  min_platform_core: "1.0.0"
```

### 4.3 Device Adapter Manifest (Example: ASTM Adapter)

```yaml
manifest:
  schema_version: "1.0.0"
  version: "1.0.0"
  created_at: "2026-06-25T00:00:00Z"
  updated_at: "2026-06-25T00:00:00Z"

identity:
  name: adapter-astm
  slug: adapter-astm
  description: "ASTM protocol adapter for laboratory device communication"
  type: adapter
  tags:
    - astm
    - device
    - laboratory
    - protocol

purpose:
  summary: "Enable ASTM protocol communication with laboratory devices"
  scope: module-specific
  domains:
    - laboratory
    - devices

ownership:
  team: device-integration
  organization: unified-healthcare-platform
  contact: devices@healthcare.org
  repository_url: "https://github.com/samertts/Adapter-ASTM"

runtime:
  language: python
  version: ">=3.11"
  os:
    - linux

maturity:
  level: experimental
  since: "2026-06-25"

services:
  - name: astm-adapter
    type: adapter
    description: "ASTM protocol handler"
    version: "0.1.0"
    port: 9100

devices:
  - name: Generic ASTM Analyzer
    type: analyzer
    manufacturer: Generic
    model: ASTM-compatible
    protocol: ASTM
    driver: astm-driver

dependencies:
  - name: platform-core
    type: platform
    version: ">=1.0.0"
    critical: true
  - name: lablink-core
    type: platform
    version: ">=1.0.0"
    critical: true

standards:
  - name: ASTM
    version: "E1394-97"
    level: full

compatibility:
  platform_core: ">=1.0.0"
  min_platform_core: "1.0.0"
```

---

## 5. JSON SCHEMA

See: `schemas/platform-manifest.schema.json`

The JSON Schema defines the complete validation structure for manifests.

---

## 6. VALIDATION RULES

### 6.1 Required Field Validation

Every manifest MUST contain all required fields. Missing required fields result in `invalid` status.

### 6.2 Naming Convention Validation

| Field | Pattern | Example |
|-------|---------|---------|
| `identity.name` | `^[a-z][a-z0-9-]*[a-z0-9]$` | `platform-core` |
| `identity.slug` | `^[a-z][a-z0-9-]*[a-z0-9]$` | `platform-core` |
| `services[].name` | `^[a-z][a-z0-9-]*[a-z0-9]$` | `auth-service` |
| `apis[].base_path` | `^/` | `/api/v1/users` |
| `events[].name` | `^[a-z][a-z0-9.]*[a-z0-9]$` | `user.created` |

### 6.3 Version Validation

All version fields MUST follow SemVer 2.0.0 format: `MAJOR.MINOR.PATCH`

### 6.4 Consistency Validation

- `services` and `apis` references must be internally consistent
- `events` publisher must match a service in the same repository
- `dependencies` must reference valid version constraints
- `compatibility.min_platform_core` must be <= `compatibility.platform_core`

### 6.5 Lifecycle Validation

- Manifests in `draft` status are not governance-enforced
- Manifests must be `valid` to be registered in the Repository Registry
- Manifests expire after 90 days without `updated_at` refresh

### 6.6 Security Validation

- No hardcoded secrets or credentials in manifest
- `environment_variables` must not contain default secret values
- `signed_by` and `signature` fields recommended for production manifests

---

## 7. VALIDATION SEVERITY LEVELS

| Level | Description | Action |
|-------|-------------|--------|
| `error` | Critical validation failure | Block registration |
| `warning` | Non-critical issue | Allow with advisory |
| `info` | Suggestion for improvement | Log only |

---

## 8. MANIFEST LIFECYCLE

```
draft → valid → registered → active → expired
                ↓              ↓
                └── invalid    └── deprecated
```

| State | Description |
|-------|-------------|
| `draft` | Manifest is being prepared |
| `valid` | Manifest passes all validation rules |
| `invalid` | Manifest fails validation |
| `registered` | Manifest is registered in Repository Registry |
| `active` | Manifest is actively maintained |
| `expired` | Manifest has not been refreshed within 90 days |
| `deprecated` | Manifest is no longer maintained |

---

## 9. GOVERNANCE INTEGRATION

When a manifest is submitted:

1. **Validation Engine** validates the manifest against the schema and rules
2. **Repository Registry** registers or updates the repository entry
3. **Knowledge Graph** updates entity relationships
4. **Governance Engine** evaluates compliance with Constitution
5. **Certification Engine** checks certification requirements
6. **Notification Service** alerts relevant teams

---

*Document generated as part of Platform-Core V2.0 Bootstrap Program — Phase 3*
*Constitution Reference: Article IV — Manifest Standard*
