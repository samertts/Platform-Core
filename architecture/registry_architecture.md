# REGISTRY ARCHITECTURE

**Document**: Centralized Registry Architecture
**Version**: 1.0.0
**Date**: 2026-06-25
**Status**: DESIGN
**Constitution Reference**: Articles III, IV, V, VI, VII, VIII

---

## 1. OVERVIEW

Platform-Core maintains nine centralized registries that serve as the authoritative source of truth for every entity type in the ecosystem. Registries are the backbone of governance, discovery, and interoperability.

**Design Principles**:
- Each registry is authoritative for its entity type
- Registries are queryable via standardized APIs
- Registries support event-driven updates
- Registries maintain full history (append-only)
- Registries are self-describing (each has a schema)

---

## 2. REGISTRY INVENTORY

| Registry | Entity Type | Constitution Reference | Purpose |
|----------|-------------|----------------------|---------|
| Repository Registry | Repository | Article III, IV | Track all repositories in the ecosystem |
| Service Registry | Service | Article III, V | Track all services and their status |
| API Registry | API | Article III, VII | Track all APIs and their contracts |
| Event Registry | Event | Article III, VI | Track all events and their schemas |
| Device Registry | Device | Article III, VIII | Track all devices and their capabilities |
| Workflow Registry | Workflow | Article III, V | Track all workflows and their definitions |
| Policy Registry | Policy | Article III, V, IX | Track all policies and their enforcement |
| Plugin Registry | Plugin | Article III, V | Track all plugins and their capabilities |
| Knowledge Registry | Knowledge | Article III | Track all platform knowledge and relationships |

---

## 3. REPOSITORY REGISTRY

**Purpose**: The authoritative source of truth for every repository in the platform ecosystem.

**Constitution Reference**: Articles III, IV

### 3.1 Data Model

```yaml
repository_entry:
  id: UUIDv4                    # Unique identifier
  name: String                  # Repository name (unique)
  slug: String                  # URL-safe identifier (unique)
  description: String           # Repository purpose
  type: Enum                    # platform-core, module, adapter, sdk, tool
  status: Enum                  # active, deprecated, archived, suspended
  visibility: Enum              # public, internal, private
  owner:                        # Ownership information
    team: String
    organization: String
    contact: String
    repository_url: URL
  manifest:                     # Manifest reference
    manifest_id: UUIDv4
    schema_version: SemVer
    manifest_version: SemVer
    last_validated: Timestamp
    validation_status: Enum     # valid, invalid, expired
  modules: List[UUIDv4]         # Modules in this repository
  services: List[UUIDv4]        # Services in this repository
  apis: List[UUIDv4]            # APIs in this repository
  events: List[UUIDv4]          # Events in this repository
  dependencies: List[UUIDv4]    # Dependencies
  maturity: Enum                # experimental, alpha, beta, stable, mature, legacy
  certification:                # Certification status
    level: Enum
    status: Enum
    assessed_at: Timestamp
    expires_at: Timestamp
  health_score: Float           # 0.0 - 1.0
  last_discovered: Timestamp    # When last scanned
  created_at: Timestamp
  updated_at: Timestamp
```

### 3.2 Registry Operations

| Operation | Description | Trigger |
|-----------|-------------|---------|
| `register` | Add new repository | Manifest submission |
| `update` | Update repository entry | Manifest update |
| `deregister` | Soft-delete repository | Repository archival |
| `query` | Search repositories | Any time |
| `validate` | Re-validate manifest | Scheduled/manual |
| `score` | Calculate health score | Scheduled |

### 3.3 Query Capabilities

```
GET /registry/repositories
GET /registry/repositories/{id}
GET /registry/repositories/{name}
GET /registry/repositories?status=active
GET /registry/repositories?owner.team=platform-engineering
GET /registry/repositories?maturity=stable
GET /registry/repositories?certification.status=passed
```

### 3.4 Events

| Event | Description |
|-------|-------------|
| `registry.repository.registered` | New repository registered |
| `registry.repository.updated` | Repository entry updated |
| `registry.repository.deregistered` | Repository deregistered |
| `registry.repository.validated` | Manifest validation completed |
| `registry.repository.scored` | Health score recalculated |

---

## 4. SERVICE REGISTRY

**Purpose**: The authoritative source of truth for all services running in the platform ecosystem.

**Constitution Reference**: Articles III, V

### 4.1 Data Model

```yaml
service_entry:
  id: UUIDv4
  name: String                  # Service name
  slug: String                  # URL-safe identifier
  description: String
  type: Enum                    # core, module, adapter, gateway, worker, scheduler
  status: Enum                  # running, stopped, error, degraded
  version: SemVer
  repository: UUIDv4            # Parent repository
  module: UUIDv4                # Parent module (if applicable)
  endpoints:                    # Network endpoints
    health: URL
    metrics: URL
    api_base: URL
  port: Integer
  dependencies: List[UUIDv4]    # Services this depends on
  consumers: List[UUIDv4]       # Services that depend on this
  events_consuming: List[UUIDv4]
  events_publishing: List[UUIDv4]
  owner:
    team: String
    contact: String
  configuration: Map            # Runtime configuration
  metrics:                      # Current metrics
    request_rate: Float
    error_rate: Float
    latency_p99: Float
    uptime_percent: Float
  last_health_check: Timestamp
  created_at: Timestamp
  updated_at: Timestamp
```

### 4.2 Registry Operations

| Operation | Description | Trigger |
|-----------|-------------|---------|
| `register` | Register new service | Service deployment |
| `update` | Update service metadata | Configuration change |
| `deregister` | Remove service | Service shutdown |
| `heartbeat` | Update health status | Periodic health check |
| `query` | Search services | Any time |
| `discover` | Find services by capability | Runtime discovery |

### 4.3 Query Capabilities

```
GET /registry/services
GET /registry/services/{id}
GET /registry/services?status=running
GET /registry/services?type=core
GET /registry/services?owner.team=platform-engineering
GET /registry/services?health.uptime_percent>99.9
```

### 4.4 Events

| Event | Description |
|-------|-------------|
| `registry.service.registered` | New service registered |
| `registry.service.updated` | Service metadata updated |
| `registry.service.deregistered` | Service deregistered |
| `registry.service.healthy` | Service health restored |
| `registry.service.unhealthy` | Service health degraded |

---

## 5. API REGISTRY

**Purpose**: The authoritative source of truth for all API contracts in the platform ecosystem.

**Constitution Reference**: Articles III, VII

### 5.1 Data Model

```yaml
api_entry:
  id: UUIDv4
  name: String
  slug: String
  description: String
  type: Enum                    # rest, graphql, grpc, websocket, webhook
  version: SemVer
  status: Enum                  # active, deprecated, sunset, removed
  service: UUIDv4               # Owning service
  repository: UUIDv4            # Owning repository
  base_path: String             # e.g., /api/v1/users
  authentication: Enum          # none, api_key, jwt, oauth2, mtls
  rate_limit:                   # Rate limiting configuration
    requests_per_minute: Integer
    burst: Integer
  schema:                       # API schema reference
    openapi_url: URL
    schema_version: SemVer
  backward_compatible: Boolean
  documentation_url: URL
  health_endpoint: URL
  metrics_endpoint: URL
  consumers: List[UUIDv4]       # APIs that depend on this
  deprecation:                  # Deprecation info
    deprecated_at: Timestamp
    sunset_at: Timestamp
    migration_guide: URL
  owner:
    team: String
    contact: String
  metrics:                      # API metrics
    request_rate: Float
    error_rate: Float
    latency_p50: Float
    latency_p99: Float
  created_at: Timestamp
  updated_at: Timestamp
```

### 5.2 Registry Operations

| Operation | Description | Trigger |
|-----------|-------------|---------|
| `register` | Register new API | Manifest update |
| `update` | Update API metadata | API version change |
| `deprecate` | Mark API as deprecated | Deprecation decision |
| `sunset` | Mark API as sunset | Sunset date reached |
| `validate` | Validate API schema | Scheduled/manual |
| `query` | Search APIs | Any time |

### 5.3 Query Capabilities

```
GET /registry/apis
GET /registry/apis/{id}
GET /registry/apis?status=active
GET /registry/apis?type=rest
GET /registry/apis?authentication=jwt
GET /registry/apis?backward_compatible=false
```

### 5.4 Events

| Event | Description |
|-------|-------------|
| `registry.api.registered` | New API registered |
| `registry.api.updated` | API metadata updated |
| `registry.api.deprecated` | API marked deprecated |
| `registry.api.sunset` | API sunset |
| `registry.api.schema_invalid` | API schema validation failed |

---

## 6. EVENT REGISTRY

**Purpose**: The authoritative source of truth for all event types in the platform ecosystem.

**Constitution Reference**: Articles III, VI

### 6.1 Data Model

```yaml
event_entry:
  id: UUIDv4
  name: String                  # e.g., user.created
  slug: String
  description: String
  type: Enum                    # domain, integration, system, audit, notification
  version: SemVer
  status: Enum                  # active, deprecated, archived
  publisher: UUIDv4             # Publishing service
  repository: UUIDv4            # Owning repository
  schema:                       # Event schema
    schema_url: URL
    schema_version: SemVer
    format: Enum                # json, avro, protobuf
  consumers: List[UUIDv4]       # Known consumers
  retention_days: Integer
  ordering_key: String          # Partition key for ordering
  category: Enum                # Event category
  owner:
    team: String
    contact: String
  documentation_url: URL
  created_at: Timestamp
  updated_at: Timestamp
```

### 6.2 Registry Operations

| Operation | Description | Trigger |
|-----------|-------------|---------|
| `register` | Register new event type | Manifest update |
| `update` | Update event metadata | Schema change |
| `deprecate` | Mark event as deprecated | Deprecation decision |
| `validate` | Validate event schema | Scheduled/manual |
| `query` | Search events | Any time |

### 6.3 Query Capabilities

```
GET /registry/events
GET /registry/events/{id}
GET /registry/events?status=active
GET /registry/events?type=domain
GET /registry/events?publisher={service_id}
```

### 6.4 Events

| Event | Description |
|-------|-------------|
| `registry.event.registered` | New event type registered |
| `registry.event.updated` | Event metadata updated |
| `registry.event.deprecated` | Event type deprecated |
| `registry.event.schema_invalid` | Event schema validation failed |

---

## 7. DEVICE REGISTRY

**Purpose**: The authoritative source of truth for all devices in the platform ecosystem.

**Constitution Reference**: Articles III, VIII

### 7.1 Data Model

```yaml
device_entry:
  id: UUIDv4
  name: String
  slug: String
  description: String
  type: Enum                    # analyzer, reader, printer, sensor, imaging, etc.
  manufacturer: String
  model: String
  serial_number: String
  protocol: Enum                # ASTM, HL7, FHIR, USB, Serial, TCP_IP, Bluetooth
  driver: UUIDv4                # Driver reference
  status: Enum                  # registered, configured, active, maintenance, decommissioned, error
  capabilities: List[Capability]
  location:                     # Physical location
    site: String
    building: String
    room: String
    position: String
  connection:                   # Connection info
    type: Enum                  # serial, tcp, bluetooth, usb
    address: String
    port: Integer
  last_communication: Timestamp
  health_status: Enum           # healthy, degraded, offline
  owner:
    team: String
    contact: String
  calibration:                  # Calibration info
    last_calibrated: Timestamp
    next_calibration: Timestamp
    certificate_url: URL
  created_at: Timestamp
  updated_at: Timestamp

Capability:
  name: String
  description: String
  protocol: String
  version: String
  parameters: Map
```

### 7.2 Registry Operations

| Operation | Description | Trigger |
|-----------|-------------|---------|
| `register` | Register new device | Device discovery |
| `configure` | Update device configuration | Configuration change |
| `activate` | Mark device as active | Device ready |
| `deactivate` | Mark device as inactive | Device maintenance |
| `decommission` | Remove device | End of life |
| `query` | Search devices | Any time |

### 7.3 Query Capabilities

```
GET /registry/devices
GET /registry/devices/{id}
GET /registry/devices?status=active
GET /registry/devices?protocol=ASTM
GET /registry/devices?location.site=lab-1
```

### 7.4 Events

| Event | Description |
|-------|-------------|
| `registry.device.registered` | New device registered |
| `registry.device.active` | Device activated |
| `registry.device.error` | Device error detected |
| `registry.device.decommissioned` | Device decommissioned |

---

## 8. WORKFLOW REGISTRY

**Purpose**: The authoritative source of truth for all workflow definitions in the platform ecosystem.

**Constitution Reference**: Articles III, V

### 8.1 Data Model

```yaml
workflow_entry:
  id: UUIDv4
  name: String
  slug: String
  description: String
  version: SemVer
  status: Enum                  # draft, active, suspended, retired
  repository: UUIDv4
  owner:
    team: String
    contact: String
  trigger_events: List[UUIDv4]  # Events that trigger this workflow
  emitted_events: List[UUIDv4]  # Events emitted by this workflow
  steps: List[WorkflowStep]
  estimated_duration_seconds: Integer
  retry_policy:
    max_retries: Integer
    backoff_seconds: Integer
  timeout_seconds: Integer
  created_at: Timestamp
  updated_at: Timestamp

WorkflowStep:
  id: UUIDv4
  name: String
  type: Enum                    # event_wait, service_call, condition, parallel, delay, compensate
  service: UUIDv4
  action: String
  conditions: List[Condition]
  timeout_seconds: Integer
  retry_policy: Object

Condition:
  field: String
  operator: Enum                # eq, neq, gt, lt, gte, lte, in, not_in
  value: Any
```

### 8.2 Registry Operations

| Operation | Description | Trigger |
|-----------|-------------|---------|
| `register` | Register new workflow | Workflow definition |
| `update` | Update workflow metadata | Workflow change |
| `activate` | Activate workflow | Ready for execution |
| `suspend` | Suspend workflow | Temporary halt |
| `retire` | Retire workflow | End of life |
| `query` | Search workflows | Any time |

### 8.3 Query Capabilities

```
GET /registry/workflows
GET /registry/workflows/{id}
GET /registry/workflows?status=active
GET /registry/workflows?trigger_events={event_id}
```

### 8.4 Events

| Event | Description |
|-------|-------------|
| `registry.workflow.registered` | New workflow registered |
| `registry.workflow.activated` | Workflow activated |
| `registry.workflow.suspended` | Workflow suspended |
| `registry.workflow.retired` | Workflow retired |

---

## 9. POLICY REGISTRY

**Purpose**: The authoritative source of truth for all governance policies in the platform ecosystem.

**Constitution Reference**: Articles III, V, IX, XII

### 9.1 Data Model

```yaml
policy_entry:
  id: UUIDv4
  name: String
  slug: String
  description: String
  type: Enum                    # access_control, data_governance, security, compliance, quality, deployment
  version: SemVer
  status: Enum                  # draft, active, deprecated, archived
  scope: Enum                   # platform, module, service, global
  enforcement: Enum             # enforcing, advisory, audit_only
  rules: List[PolicyRule]
  priority: Integer             # Higher = evaluated first
  owner:
    team: String
    contact: String
  documentation_url: URL
  created_at: Timestamp
  updated_at: Timestamp

PolicyRule:
  id: UUIDv4
  name: String
  description: String
  condition: String             # Boolean expression
  effect: Enum                  # allow, deny
  resources: List[String]       # Affected resources
  actions: List[String]         # Affected actions
```

### 9.2 Registry Operations

| Operation | Description | Trigger |
|-----------|-------------|---------|
| `register` | Register new policy | Policy creation |
| `update` | Update policy | Policy change |
| `activate` | Activate policy | Policy approval |
| `deprecate` | Deprecate policy | Policy replacement |
| `enforce` | Apply policy | Policy evaluation |
| `query` | Search policies | Any time |

### 9.3 Query Capabilities

```
GET /registry/policies
GET /registry/policies/{id}
GET /registry/policies?status=active
GET /registry/policies?type=security
GET /registry/policies?enforcement=enforcing
```

### 9.4 Events

| Event | Description |
|-------|-------------|
| `registry.policy.registered` | New policy registered |
| `registry.policy.activated` | Policy activated |
| `registry.policy.violation` | Policy violation detected |
| `registry.policy.deprecated` | Policy deprecated |

---

## 10. PLUGIN REGISTRY

**Purpose**: The authoritative source of truth for all plugins extending Platform-Core functionality.

**Constitution Reference**: Articles III, V

### 10.1 Data Model

```yaml
plugin_entry:
  id: UUIDv4
  name: String
  slug: String
  description: String
  version: SemVer
  status: Enum                  # draft, active, deprecated, archived
  type: Enum                    # analyzer, dashboard, integration, notification, workflow
  author: String
  repository: UUIDv4
  entry_point: String           # Module or file path
  dependencies: List[UUIDv4]    # Plugin dependencies
  configuration_schema: Object  # JSON Schema for plugin config
  capabilities: List[String]    # What this plugin provides
  hooks: List[String]           # Platform hooks this plugin registers
  owner:
    team: String
    contact: String
  documentation_url: URL
  created_at: Timestamp
  updated_at: Timestamp
```

### 10.2 Registry Operations

| Operation | Description | Trigger |
|-----------|-------------|---------|
| `register` | Register new plugin | Plugin submission |
| `update` | Update plugin metadata | Plugin update |
| `activate` | Activate plugin | Plugin enable |
| `deactivate` | Deactivate plugin | Plugin disable |
| `deprecate` | Deprecate plugin | Plugin replacement |
| `query` | Search plugins | Any time |

### 10.3 Query Capabilities

```
GET /registry/plugins
GET /registry/plugins/{id}
GET /registry/plugins?status=active
GET /registry/plugins?type=analyzer
GET /registry/plugins?capabilities=health_scoring
```

### 10.4 Events

| Event | Description |
|-------|-------------|
| `registry.plugin.registered` | New plugin registered |
| `registry.plugin.activated` | Plugin activated |
| `registry.plugin.deactivated` | Plugin deactivated |
| `registry.plugin.error` | Plugin runtime error |

---

## 11. KNOWLEDGE REGISTRY

**Purpose**: The authoritative source of truth for all platform knowledge, including relationships between entities.

**Constitution Reference**: Article III

### 11.1 Data Model

```yaml
knowledge_entry:
  id: UUIDv4
  type: Enum                    # entity, relationship, metric, decision, standard
  name: String
  description: String
  entity_type: String           # Type of entity this knowledge is about
  entity_id: UUIDv4             # Reference to entity
  attributes: Map               # Knowledge attributes
  confidence: Float             # 0.0 - 1.0
  source: String                # How this knowledge was obtained
  source_repository: UUIDv4     # Repository that provided this knowledge
  valid_from: Timestamp
  valid_until: Timestamp        # null = no expiry
  created_at: Timestamp
  updated_at: Timestamp

RelationshipEntry:
  id: UUIDv4
  source_type: String
  source_id: UUIDv4
  target_type: String
  target_id: UUIDv4
  relationship_type: Enum       # owns, depends-on, implements, publishes, consumes, etc.
  weight: Float                 # Relationship strength
  metadata: Map
  created_at: Timestamp
```

### 11.2 Registry Operations

| Operation | Description | Trigger |
|-----------|-------------|---------|
| `add_knowledge` | Add new knowledge | Discovery/scanning |
| `update_knowledge` | Update knowledge | Re-scanning |
| `remove_knowledge` | Remove knowledge | Entity removal |
| `add_relationship` | Add entity relationship | Discovery |
| `remove_relationship` | Remove relationship | Entity removal |
| `query` | Search knowledge | Any time |
| `graph_query` | Query knowledge graph | Any time |

### 11.3 Query Capabilities

```
GET /registry/knowledge
GET /registry/knowledge/{id}
GET /registry/knowledge?entity_type=repository
GET /registry/knowledge?entity_id={uuid}
GET /registry/knowledge/relationships?source={uuid}
GET /registry/knowledge/relationships?target={uuid}
GET /registry/knowledge/graph?root={uuid}&depth=3
```

### 11.4 Events

| Event | Description |
|-------|-------------|
| `registry.knowledge.added` | New knowledge added |
| `registry.knowledge.updated` | Knowledge updated |
| `registry.knowledge.removed` | Knowledge removed |
| `registry.knowledge.relationship_added` | New relationship added |

---

## 12. REGISTRY INFRASTRUCTURE

### 12.1 Storage Architecture

```
┌─────────────────────────────────────────────┐
│              Platform-Core                   │
│                                             │
│  ┌─────────────┐  ┌─────────────────────┐  │
│  │  PostgreSQL   │  │  Event Bus (Redis)  │  │
│  │  (Primary)    │  │  (Pub/Sub)          │  │
│  └─────────────┘  └─────────────────────┘  │
│         │                    │               │
│         ▼                    ▼               │
│  ┌──────────────────────────────────────┐  │
│  │           Registry Service            │  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐   │  │
│  │  │  Repo   │ │Service │ │  API   │   │  │
│  │  │Registry │ │Registry│ │Registry│   │  │
│  │  └────────┘ └────────┘ └────────┘   │  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐   │  │
│  │  │ Event  │ │Device  │ │Workflow│   │  │
│  │  │Registry│ │Registry│ │Registry│   │  │
│  │  └────────┘ └────────┘ └────────┘   │  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐   │  │
│  │  │ Policy │ │Plugin  │ │Knowledge│  │  │
│  │  │Registry│ │Registry│ │Registry │  │  │
│  │  └────────┘ └────────┘ └────────┘   │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### 12.2 API Design

All registries expose a consistent REST API:

```
GET    /registry/{entity-type}           # List all
GET    /registry/{entity-type}/{id}      # Get by ID
POST   /registry/{entity-type}           # Create
PUT    /registry/{entity-type}/{id}      # Update
DELETE /registry/{entity-type}/{id}      # Soft delete
GET    /registry/{entity-type}/search    # Advanced search
GET    /registry/{entity-type}/export    # Export as JSON/YAML
```

### 12.3 Event Integration

Every registry operation publishes an event to the event bus:

```
registry.{entity-type}.created
registry.{entity-type}.updated
registry.{entity-type}.deleted
registry.{entity-type}.validated
```

### 12.4 Caching Strategy

- **Read cache**: Redis, TTL 5 minutes
- **Write-through**: Writes update cache immediately
- **Cache invalidation**: On entity update/delete

### 12.5 Backup and Recovery

- **Primary**: PostgreSQL with WAL archiving
- **Replica**: Read replica for query load
- **Backup**: Daily full backup, hourly incremental
- **Recovery Point Objective (RPO)**: 1 hour
- **Recovery Time Objective (RTO)**: 15 minutes

---

## 13. REGISTRY GOVERNANCE

### 13.1 Access Control

| Role | Create | Read | Update | Delete |
|------|--------|------|--------|--------|
| Platform Architect | Yes | Yes | Yes | Yes |
| Team Lead | Yes | Yes | Yes | No |
| Developer | Yes | Yes | Yes (own) | No |
| Viewer | No | Yes | No | No |
| Automated System | Yes | Yes | Yes | No |

### 13.2 Validation

- Every write operation triggers validation
- Invalid writes are rejected with detailed error messages
- Validation is asynchronous for read performance

### 13.3 Audit

- All registry operations are logged
- Audit trail is immutable
- Audit logs are retained for 7 years (healthcare requirement)

---

*Document generated as part of Platform-Core V2.0 Bootstrap Program — Phase 4*
*Constitution Reference: Articles III, IV, V, VI, VII, VIII*
