# REFERENCE ARCHITECTURE — UNIFIED HEALTHCARE PLATFORM

**Document**: Standard Module Architecture Reference
**Version**: 1.0.0
**Date**: 2026-06-25
**Status**: ACTIVE
**Constitution Reference**: Articles I, II, V, VII, XII

---

## 1. PURPOSE

This document defines the standard architecture that every module in the Unified Healthcare Platform must follow. It establishes a canonical layered architecture, dependency rules, layer responsibilities, and a reusable module template.

---

## 2. ARCHITECTURE OVERVIEW

Every module in the ecosystem implements a consistent layered architecture. The layers are ordered from external-facing (top) to internal infrastructure (bottom). Dependencies flow strictly downward.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     MODULE ARCHITECTURE                             │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  LAYER 1 — PRESENTATION LAYER                                │  │
│  │  React · Vue · PySide6 · tkinter · CLI                        │  │
│  │  Responsibility: User interaction, rendering, input handling  │  │
│  └───────────────────────────┬───────────────────────────────────┘  │
│                              │ calls                                │
│  ┌───────────────────────────▼───────────────────────────────────┐  │
│  │  LAYER 2 — APPLICATION LAYER                                  │  │
│  │  FastAPI · Express · Flask · gRPC services                    │  │
│  │  Responsibility: Request routing, validation, orchestration   │  │
│  └───────────────────────────┬───────────────────────────────────┘  │
│                              │ calls                                │
│  ┌───────────────────────────▼───────────────────────────────────┐  │
│  │  LAYER 3 — DOMAIN LAYER                                       │  │
│  │  Entities · Value Objects · Domain Services · Aggregates       │  │
│  │  Responsibility: Business rules, invariants, domain logic     │  │
│  └───────────────────────────┬───────────────────────────────────┘  │
│                              │ calls                                │
│  ┌───────────────────────────▼───────────────────────────────────┐  │
│  │  LAYER 4 — INFRASTRUCTURE LAYER                               │  │
│  │  Repositories · External Services · Database Adapters         │  │
│  │  Responsibility: Persistence, external API calls, I/O        │  │
│  └───────────────────────────┬───────────────────────────────────┘  │
│                              │ calls                                │
│  ┌───────────────────────────▼───────────────────────────────────┐  │
│  │  LAYER 5 — INTEGRATION LAYER                                  │  │
│  │  Event Handlers · API Clients · SDK Adapters                   │  │
│  │  Responsibility: Cross-module communication, event processing │  │
│  └───────────────────────────┬───────────────────────────────────┘  │
│                              │ calls                                │
│  ┌───────────────────────────▼───────────────────────────────────┐  │
│  │  LAYER 6 — RUNTIME LAYER                                      │  │
│  │  Platform-Core Runtime · Service Container · Event Bus        │  │
│  │  Responsibility: Lifecycle, DI, configuration, observability │  │
│  └───────────────────────────┬───────────────────────────────────┘  │
│                              │ calls                                │
│  ┌───────────────────────────▼───────────────────────────────────┐  │
│  │  LAYER 7 — SDK LAYER                                          │  │
│  │  Python SDK · TypeScript SDK · Client Libraries               │  │
│  │  Responsibility: Platform API consumption, typed clients      │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. LAYER DEFINITIONS

### 3.1 Presentation Layer

**Purpose**: Render UI and handle user input.

**Technologies**:
| Technology | Use Case |
|------------|----------|
| React 18+ | Web dashboards, admin panels |
| Vue 3+ | Lightweight web interfaces |
| PySide6 | Desktop applications (Windows/Linux) |
| tkinter | Government desktop tools |
| React Native | Mobile PWA / Capacitor |
| Click / Typer | CLI tools |

**Responsibilities**:
- Render views based on Application Layer responses
- Validate user input client-side
- Manage UI state (Redux, Pinia, QSettings)
- Handle authentication UI flows (OAuth2, JWT)
- Emit user actions as typed events

**Constraints**:
- Must not contain business logic
- Must not access infrastructure directly
- Must communicate only with the Application Layer
- Must use shared UI component libraries where available

---

### 3.2 Application Layer

**Purpose**: Receive external requests and orchestrate domain operations.

**Technologies**:
| Technology | Use Case |
|------------|----------|
| FastAPI | REST APIs (Python) |
| Express | REST APIs (TypeScript) |
| gRPC | Service-to-service RPC |
| WebSocket | Real-time event streams |

**Responsibilities**:
- Route requests to appropriate handlers
- Validate request payloads (Pydantic, Zod)
- Orchestrate domain service calls
- Format and return responses
- Handle authentication and authorization
- Rate limiting and request throttling
- OpenAPI documentation generation

**Constraints**:
- Must not contain business logic (delegate to Domain Layer)
- Must use DTOs for request/response payloads
- Must expose `/health`, `/metrics`, `/ready` endpoints
- Must use structured error responses (RFC 7807)

---

### 3.3 Domain Layer

**Purpose**: Encapsulate core business rules and domain logic.

**Components**:
| Component | Description |
|-----------|-------------|
| Entities | Objects with identity and lifecycle (e.g., Repository, Module, Service) |
| Value Objects | Immutable objects without identity (e.g., Version, Email, APIEndpoint) |
| Aggregates | Consistency boundaries (e.g., RepositoryAggregate) |
| Domain Services | Stateless business operations (e.g., HealthScorer, CertificationEngine) |
| Domain Events | Significant business occurrences (e.g., ModuleCertified, FindingRaised) |
| Repository Interfaces | Contracts for persistence (implemented in Infrastructure) |

**Responsibilities**:
- Enforce business invariants
- Execute domain logic
- Emit domain events
- Validate state transitions

**Constraints**:
- Must not depend on any infrastructure technology
- Must not import database, HTTP, or filesystem libraries
- Must define repository interfaces (ports) for infrastructure implementation
- All state changes must go through domain entities

---

### 3.4 Infrastructure Layer

**Purpose**: Implement technical concerns and external integrations.

**Components**:
| Component | Description |
|-----------|-------------|
| Repository Implementations | Database access (PostgreSQL, SQLite) |
| External Service Clients | Third-party API integrations |
| Message Queue Producers/Consumers | Event publishing and subscription |
| Cache Adapters | Redis, in-memory caching |
| File System Adapters | Local/remote file operations |
| Certificate Managers | TLS, signing, verification |

**Responsibilities**:
- Persist domain entities
- Query databases
- Call external services
- Implement repository interfaces from Domain Layer
- Handle serialization and deserialization

**Constraints**:
- Must implement interfaces defined in Domain Layer
- Must not contain business logic
- Must handle connection lifecycle and retry logic
- Must use parameterized queries (no SQL injection)

---

### 3.5 Integration Layer

**Purpose**: Enable cross-module and cross-repository communication.

**Components**:
| Component | Description |
|-----------|-------------|
| Event Handlers | React to domain events from other modules |
| API Clients | Call APIs of other modules |
| SDK Wrappers | Consume Platform-Core SDKs |
| Webhook Receivers | Process incoming webhooks |
| Contract Validators | Verify API/event contract compliance |

**Responsibilities**:
- Subscribe to and process cross-module events
- Call external module APIs
- Validate incoming contracts against schemas
- Transform data between module boundaries
- Handle eventual consistency patterns

**Constraints**:
- Must use published contracts (API specs, event schemas)
- Must not assume direct database access to other modules
- Must handle API versioning and backward compatibility
- Must implement circuit breaker patterns for external calls

---

### 3.6 Runtime Layer

**Purpose**: Provide platform infrastructure consumed by all modules.

**Components** (provided by Platform-Core):
| Component | Description |
|-----------|-------------|
| Service Container | Dependency injection and lifecycle management |
| Configuration Engine | Hierarchical, hot-reloadable configuration |
| Logging Engine | Structured logging with correlation IDs |
| Telemetry Engine | Metrics, traces, health checks |
| Identity Engine | Authentication, authorization, RBAC |
| Policy Engine | Policy evaluation and enforcement |
| Event Bus | Async publish/subscribe event system |
| Plugin Engine | Dynamic plugin loading and lifecycle |
| Manifest Loader | Manifest parsing and validation |
| SDK Loader | SDK version negotiation |

**Responsibilities**:
- Manage service lifecycles
- Inject dependencies
- Provide configuration, logging, telemetry
- Route events between modules
- Load and manage plugins

**Constraints**:
- Must not contain business logic
- Must be thread-safe and hot-reloadable
- Must support graceful startup and shutdown
- Must work offline (core functions)

---

### 3.7 SDK Layer

**Purpose**: Provide typed clients for Platform-Core API consumption.

**SDKs**:
| SDK | Language | Package |
|-----|----------|---------|
| Platform SDK | Python | `platform-core-sdk` |
| Platform SDK | TypeScript | `@platform-core/sdk` |
| Platform CLI | Python | `platform-core-cli` |

**Responsibilities**:
- Provide typed API clients
- Handle authentication and token management
- Implement retry and circuit breaker logic
- Validate responses against schemas
- Publish to package registries (PyPI, npm)

**Constraints**:
- Must follow semantic versioning
- Must maintain backward compatibility within major versions
- Must provide type stubs or generated types
- Must include comprehensive documentation

---

## 4. DEPENDENCY RULES

```
┌─────────────────────────────────────────────────────────┐
│                   DEPENDENCY FLOW                        │
│                                                         │
│   Presentation ──→ Application ──→ Domain ←── App      │
│                                    │                    │
│                              depends on                  │
│                                    │                    │
│                              Infrastructure             │
│                                    │                    │
│                              depends on                  │
│                                    │                    │
│                              Integration                │
│                                    │                    │
│                              depends on                  │
│                                    │                    │
│                              Runtime (Platform-Core)    │
│                                    │                    │
│                              depends on                  │
│                                    │                    │
│                              SDK Layer                  │
└─────────────────────────────────────────────────────────┘
```

### 4.1 Dependency Matrix

| Layer | May Depend On | Must NOT Depend On |
|-------|---------------|-------------------|
| Presentation | Application | Domain, Infrastructure, Integration, Runtime |
| Application | Domain, Runtime | Infrastructure, Integration, SDK |
| Domain | Nothing (pure) | Presentation, Application, Infrastructure, Integration, Runtime, SDK |
| Infrastructure | Domain interfaces | Presentation, Application |
| Integration | Domain, Infrastructure, Runtime | Presentation, Application |
| Runtime | Nothing (platform) | Presentation, Application, Domain, Integration |
| SDK | Runtime (Platform-Core API) | Presentation, Application, Domain, Infrastructure |

### 4.2 Inversion of Control

Domain Layer defines interfaces (ports). Infrastructure Layer implements them (adapters). This is the Dependency Inversion Principle.

```
Domain Layer
┌─────────────────────────────┐
│ RepositoryInterface (Port)  │  ← defines contract
└─────────────┬───────────────┘
              │
              │ implemented by
              ▼
Infrastructure Layer
┌─────────────────────────────┐
│ PostgresRepository (Adapter)│  ← fulfills contract
└─────────────────────────────┘
```

---

## 5. CROSS-CUTTING CONCERNS

### 5.1 Policies

| Concern | Implementation |
|---------|---------------|
| Authentication | JWT tokens, API keys, OAuth2 (Runtime Identity Engine) |
| Authorization | RBAC with roles: Architect, Lead, Developer, Viewer (Runtime Policy Engine) |
| Rate Limiting | Token bucket per API key, configurable thresholds |
| Governance | Constitution compliance checks on every deployment |

### 5.2 Events

Every significant business action publishes an event.

**Event Structure**:
```
{
  "id": "uuid",
  "type": "module.installed",
  "source": "platform-core",
  "data": { ... },
  "timestamp": "ISO-8601",
  "priority": "normal",
  "correlation_id": "uuid"
}
```

**Event Categories**:
| Category | Examples |
|----------|----------|
| Registry | repository.registered, service.published, api.versioned |
| Governance | finding.raised, review.completed, certification.granted |
| Discovery | scan.completed, health.score.calculated, anomaly.detected |
| Lifecycle | module.installed, module.updated, module.removed |
| System | runtime.started, runtime.shutting_down, error.detected |

### 5.3 APIs

All APIs follow these standards:

| Standard | Requirement |
|----------|-------------|
| Versioning | URL path versioning (`/api/v1/`) |
| Documentation | OpenAPI 3.1 auto-generated |
| Error Format | RFC 7807 Problem Details |
| Pagination | Cursor-based with `limit` and `cursor` |
| Filtering | Query parameter based (`?status=active`) |
| Sorting | Query parameter based (`?sort=created_at:desc`) |
| Health | `/health` (liveness), `/ready` (readiness), `/metrics` |

### 5.4 Storage

| Concern | Strategy |
|---------|----------|
| Primary Database | PostgreSQL 16 (ACID, JSONB, extensions) |
| Graph Database | Apache AGE (graph queries on PostgreSQL) |
| Cache | Redis 7 (in-memory, pub/sub) |
| Event Store | Redis Streams (durable, replayable) |
| File Storage | Local filesystem (development), S3-compatible (production) |
| Backups | Daily full, hourly incremental, WAL archiving |

### 5.5 Security

| Practice | Implementation |
|----------|---------------|
| Secrets Management | Environment variables, never hardcoded |
| TLS | TLS 1.3 for all in-transit data |
| Encryption at Rest | PostgreSQL TDE, disk encryption |
| Certificate Rotation | Automated rotation with 90-day validity |
| Digital Signatures | Ed25519 for manifests and packages |
| Audit Logging | All mutations logged with user, timestamp, change |
| Dependency Scanning | Automated CVE scanning in CI/CD |
| SAST | Static analysis on every commit |

### 5.6 Observability

| Signal | Tool | Purpose |
|--------|------|---------|
| Metrics | Prometheus + OpenTelemetry | Request rates, latencies, errors |
| Logs | Structured JSON + correlation IDs | Debugging, audit trail |
| Traces | OpenTelemetry distributed tracing | Request flow across services |
| Dashboards | Grafana | Real-time operational visibility |
| Alerts | Alertmanager | Critical issue notification |

### 5.7 Testing

| Level | Scope | Target Coverage |
|-------|-------|----------------|
| Unit | Individual functions/methods | >90% |
| Integration | Service interactions | >80% |
| Contract | API and event contracts | 100% of public contracts |
| E2E | Full user workflows | Critical paths |
| Performance | Load and stress testing | Meet SLA targets |
| Security | Penetration, vulnerability scanning | Zero critical findings |

---

## 6. MODULE TEMPLATE

### 6.1 Repository Structure

```
module-name/
├── manifest.yaml                    # Platform manifest (mandatory)
├── README.md                        # Module documentation
├── pyproject.toml                   # Python project config (Python modules)
├── package.json                     # Node.js project config (TS modules)
├── src/
│   ├── presentation/                # Layer 1: UI components
│   │   ├── api/                     # FastAPI/Express route handlers
│   │   ├── cli/                     # CLI entry points
│   │   └── web/                     # Web UI (React/Vue)
│   ├── application/                 # Layer 2: Application services
│   │   ├── services/                # Application service classes
│   │   └── dto/                     # Data Transfer Objects
│   ├── domain/                      # Layer 3: Domain model
│   │   ├── entities/                # Entity classes
│   │   ├── value_objects/           # Value object classes
│   │   ├── services/                # Domain services
│   │   ├── events/                  # Domain events
│   │   └── repositories/           # Repository interfaces (ports)
│   ├── infrastructure/              # Layer 4: Infrastructure
│   │   ├── database/                # Database adapters
│   │   ├── external/                # External service clients
│   │   └── repositories/           # Repository implementations
│   └── integration/                 # Layer 5: Cross-module integration
│       ├── events/                  # Event handlers
│       ├── api_clients/            # API clients for other modules
│       └── contracts/              # Contract validators
├── tests/
│   ├── unit/                        # Unit tests
│   ├── integration/                 # Integration tests
│   ├── contract/                    # Contract tests
│   └── e2e/                        # End-to-end tests
├── docs/
│   ├── api/                         # API documentation
│   ├── architecture/               # Architecture decision records
│   └── operations/                 # Runbooks, deployment guides
├── scripts/                         # Build, deploy, utility scripts
├── .github/
│   └── workflows/                   # CI/CD pipelines
└── Dockerfile                       # Container build
```

### 6.2 Manifest Template

```yaml
# manifest.yaml — Platform Module Manifest v1.0
apiVersion: platform.unified/v1
kind: Module
metadata:
  name: module-name
  displayName: "Module Display Name"
  version: "1.0.0"
  description: "Module description"
  author: "Team Name"
  license: "Proprietary"

spec:
  category: clinical|operational|infrastructure|integration
  maturity: prototype|alpha|beta|stable|production
  
  languages:
    - python: ">=3.11"
    - typescript: ">=5.0"
  
  frameworks:
    - fastapi: ">=0.100.0"
    - react: ">=18.0"
  
  platformCore:
    version: ">=1.0.0"
    requiredServices:
      - identity
      - configuration
      - logging
      - telemetry
      - eventBus
  
  services:
    - name: module-service
      type: rest
      port: 8080
      healthEndpoint: /health
  
  apis:
    - name: Module API
      type: rest
      version: "v1"
      basePath: /api/v1
      spec: openapi
  
  events:
    published:
      - name: module.entity.created
        schema: module-entity-created-v1
      - name: module.entity.updated
        schema: module-entity-updated-v1
    subscribed:
      - name: platform.repository.registered
        schema: repository-registered-v1
  
  dependencies:
    repositories:
      - name: platform-core
        version: ">=1.0.0"
        required: true
    services:
      - name: identity-service
        version: ">=1.0.0"
  
  runtime:
    minMemory: "256Mi"
    maxMemory: "1Gi"
    minCpu: "0.25"
    maxCpu: "1.0"
    replicas:
      min: 1
      max: 3
  
  certification:
    level: basic|standard|clinical|national
    requiredReviews:
      - architecture
      - security
      - api
      - testing
      - compatibility

status:
  registeredAt: "2026-06-25T00:00:00Z"
  lastScannedAt: null
  healthScore: null
  certificationLevel: null
```

### 6.3 Python Module Structure

```
src/
├── domain/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   └── module_entity.py
│   ├── value_objects/
│   │   ├── __init__.py
│   │   └── version.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── module_service.py
│   └── repositories/
│       ├── __init__.py
│       └── module_repository.py       # Interface only
├── infrastructure/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── postgres_module_repository.py
│   └── external/
│       ├── __init__.py
│       └── platform_core_client.py
├── application/
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── module_application_service.py
│   └── dto/
│       ├── __init__.py
│       ├── module_request.py
│       └── module_response.py
└── presentation/
    ├── __init__.py
    ├── api/
    │   ├── __init__.py
    │   └── module_router.py
    └── cli/
        ├── __init__.py
        └── module_cli.py
```

### 6.4 TypeScript Module Structure

```
src/
├── domain/
│   ├── entities/
│   │   ├── module.entity.ts
│   │   └── index.ts
│   ├── value-objects/
│   │   ├── version.vo.ts
│   │   └── index.ts
│   ├── services/
│   │   ├── module.service.ts
│   │   └── index.ts
│   └── repositories/
│       ├── module.repository.ts         # Interface only
│       └── index.ts
├── infrastructure/
│   ├── database/
│   │   ├── postgres-module.repository.ts
│   │   └── index.ts
│   └── external/
│       ├── platform-core.client.ts
│       └── index.ts
├── application/
│   ├── services/
│   │   ├── module.application.service.ts
│   │   └── index.ts
│   └── dto/
│       ├── module.request.ts
│       ├── module.response.ts
│       └── index.ts
└── presentation/
    ├── api/
    │   ├── module.router.ts
    │   └── index.ts
    ├── cli/
    │   ├── module.cli.ts
    │   └── index.ts
    └── web/
        ├── components/
        │   └── ModuleDashboard.tsx
        └── index.ts
```

---

## 7. EXISTING MODULE EXAMPLES

| Module | Repository | Presentation | Application | Domain | Infrastructure |
|--------|-----------|--------------|-------------|--------|----------------|
| Platform-Core | `Platform-Core` | FastAPI, CLI | FastAPI routes | Registry, Governance, Discovery | PostgreSQL, Redis |
| Front-end | `Front-end` | React, Capacitor | React hooks | HLIMS domain | API client |
| govlab-platform | `govlab-platform` | React, Express | Express routes | Government lab | PostgreSQL |
| identity-credential | `identity-credential` | PySide6 | Qt services | Credential mgmt | Local DB |
| LabLink-Core | `LabLink-Core` | FastAPI | FastAPI routes | Device integration | ASTM, HL7 |
| OGLG | `OGLG` | tkinter | Tk services | Correspondence | Local DB |
| Receipt-and-delivery | `Receipt-and-delivery` | Vue3, FastAPI | FastAPI + Vue | Sample mgmt | PostgreSQL |
| Iraq-National-Workforce | `Iraq-National-Workforce-Platform-INWP` | Rust TUI | Rust services | Workforce mgmt | SQLite |

---

## 8. ARCHITECTURE VALIDATION

### 8.1 Automated Checks

| Check | Tool | Enforcement |
|-------|------|-------------|
| Layer dependency | Custom linter | CI/CD gate |
| No business logic in Presentation | Code review + linter | PR review |
| Domain purity | Import graph analysis | CI/CD gate |
| Repository interface pattern | Architecture review | Governance review |
| Event contract compliance | Schema validation | Runtime check |
| API contract compliance | Contract tests | CI/CD gate |

### 8.2 Governance Review

Every module must pass architecture review before certification:

1. **Layer Compliance**: All layers follow dependency rules
2. **Domain Purity**: Domain layer has no infrastructure imports
3. **Contract Compliance**: APIs and events follow published contracts
4. **Observability**: All services expose health and metrics
5. **Security**: No hardcoded secrets, proper authentication
6. **Testing**: Unit, integration, and contract tests present

---

## 9. CONSTITUTION ALIGNMENT

| Architecture Element | Constitution Article |
|---------------------|---------------------|
| Layered architecture | Article I — Platform Principles |
| Module independence | Article II — Repository Governance |
| Manifest requirement | Article IV — Manifest Standard |
| Platform-Core runtime | Article V — Shared Platform Services |
| Event-driven integration | Article VI — Event Governance |
| API standards | Article VII — API Governance |
| Device protocol layers | Article VIII — Device Platform |
| AI-assisted reviews | Article IX — AI Governance |
| Observability layers | Article X — Self Evolution |
| Health scoring layers | Article XI — Operational Intelligence |
| Certification gates | Article XII — Certification |

---

*Document generated as part of Platform-Core V2.0 Bootstrap Program*
*Constitution Reference: Articles I, II, V, VII, XII*
