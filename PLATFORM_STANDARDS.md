# PLATFORM STANDARDS — UNIFIED HEALTHCARE PLATFORM

**Document**: Platform Development Standards
**Version**: 1.0.0
**Date**: 2026-06-25
**Status**: ACTIVE
**Constitution Reference**: Articles I, VII, XII, XVII

---

## 1. PURPOSE

This document defines the development standards for every repository in the Unified Healthcare Platform ecosystem. Compliance with these standards is mandatory for module certification.

---

## 2. NAMING CONVENTIONS

### 2.1 Python Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Packages | `snake_case` | `platform_core` |
| Modules | `snake_case` | `registry_service.py` |
| Classes | `PascalCase` | `RepositoryRegistry` |
| Functions | `snake_case` | `calculate_health_score()` |
| Variables | `snake_case` | `max_retry_count` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Private members | `_leading_underscore` | `_internal_state` |
| Type variables | `PascalCase` | `EntityType` |
| Protocols | `PascalCase` | `Lifecycle`, `EventHandler` |
| Enums | `PascalCase` for class, `UPPER_SNAKE` for members | `RuntimeState.RUNNING` |
| Exceptions | `PascalCase` + `Error` suffix | `ValidationError`, `ConfigurationError` |
| Test files | `test_` prefix | `test_registry_service.py` |
| Test classes | `Test` prefix | `TestRepositoryRegistry` |
| Test functions | `test_` prefix | `test_register_repository()` |

### 2.2 TypeScript Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Packages | `kebab-case` | `platform-core-sdk` |
| Files | `kebab-case` | `module-entity.ts` |
| Classes | `PascalCase` | `RepositoryRegistry` |
| Interfaces | `PascalCase` (no `I` prefix) | `EventHandler`, `Lifecycle` |
| Types | `PascalCase` | `RuntimeState`, `HealthStatus` |
| Functions | `camelCase` | `calculateHealthScore()` |
| Variables | `camelCase` | `maxRetryCount` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Enums | `PascalCase` for name, `PascalCase` for members | `RuntimeState.Running` |
| React Components | `PascalCase` | `ModuleDashboard` |
| React Hooks | `camelCase` with `use` prefix | `useModuleRegistry` |
| Test files | `*.spec.ts` or `*.test.ts` | `registry.service.spec.ts` |

### 2.3 Database Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Tables | `snake_case` (singular) | `repository`, `module`, `service` |
| Columns | `snake_case` | `created_at`, `health_score` |
| Primary Keys | `id` (UUID) | `id UUID PRIMARY KEY` |
| Foreign Keys | `{table}_id` | `repository_id UUID REFERENCES repository(id)` |
| Indexes | `idx_{table}_{column}` | `idx_repository_status` |
| Unique Constraints | `uq_{table}_{column}` | `uq_repository_name` |
| Check Constraints | `ck_{table}_{rule}` | `ck_health_score_range` |
| Migrations | `{timestamp}_{description}.sql` | `20260625_001_create_repository.sql` |
| Schemas | `snake_case` | `platform_core`, `governance` |

---

## 3. VERSIONING

### 3.1 Semantic Versioning

All packages follow Semantic Versioning 2.0.0:

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

MAJOR: Breaking changes
MINOR: New features (backward compatible)
PATCH: Bug fixes (backward compatible)
PRERELEASE: alpha.1, beta.1, rc.1
BUILD: build metadata
```

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| Breaking API change | MAJOR | 1.0.0 → 2.0.0 |
| New feature | MINOR | 1.0.0 → 1.1.0 |
| Bug fix | PATCH | 1.0.0 → 1.0.1 |
| Pre-release | PRERELEASE | 1.0.0-alpha.1 → 1.0.0-beta.1 |
| Dependency update (non-breaking) | PATCH | 1.0.0 → 1.0.1 |

### 3.2 API Versioning

| Style | Convention | Example |
|-------|-----------|---------|
| URL path | `/api/v{N}/` | `/api/v1/repositories` |
| Header | `Accept: application/vnd.platform.v1+json` | — |
| Deprecation | `Sunset` header + docs | `Sunset: 2027-06-25` |

**API Version Lifecycle**:
```
v1 (current) ──→ v2 (developing) ──→ v1 (deprecated, 12-month window) ──→ v1 (removed)
```

### 3.3 Package Versioning

| Package | Registry | Version Constraint |
|---------|----------|-------------------|
| Python packages | PyPI | `>=MAJOR.MINOR.0,<MAJOR+1.0.0` |
| TypeScript packages | npm | `^MAJOR.MINOR.PATCH` |
| Docker images | Container Registry | `MAJOR.MINOR.PATCH` |
| Platform Manifest | Platform-Core | `MAJOR.MINOR.PATCH` |

### 3.4 Manifest Versioning

| Field | Versioning Rule |
|-------|----------------|
| `metadata.version` | Semantic versioning |
| `spec.platformCore.version` | Range constraint (`>=X.Y.Z`) |
| `spec.services[].version` | Semantic versioning |
| `spec.apis[].version` | `v{N}` format |
| `spec.events.published[].schema` | `{name}-v{N}` format |

---

## 4. REPOSITORY STRUCTURE

### 4.1 Root Structure

```
repository-name/
├── manifest.yaml                 # Platform manifest (MANDATORY)
├── README.md                     # Module documentation
├── LICENSE                       # License file
├── CHANGELOG.md                  # Release history
├── pyproject.toml                # Python config (Python modules)
├── package.json                  # Node.js config (TS modules)
├── Cargo.toml                    # Rust config (Rust modules)
├── go.mod                        # Go config (Go modules)
├── src/                          # Source code
├── tests/                        # Test suite
├── docs/                         # Documentation
├── scripts/                      # Build/deploy scripts
├── .github/                      # CI/CD workflows
├── .gitignore                    # Git ignore rules
├── Dockerfile                    # Container build
├── docker-compose.yml            # Local development stack
└── .env.example                  # Environment variable template
```

### 4.2 Source Code Structure

Follow the Reference Architecture layered structure defined in `REFERENCE_ARCHITECTURE.md`:

```
src/
├── presentation/          # Layer 1
├── application/           # Layer 2
├── domain/                # Layer 3
├── infrastructure/        # Layer 4
└── integration/           # Layer 5
```

### 4.3 Test Structure

```
tests/
├── conftest.py            # Shared fixtures
├── unit/                  # Unit tests (mirrors src/ structure)
│   ├── domain/
│   ├── application/
│   └── infrastructure/
├── integration/           # Integration tests
├── contract/              # API and event contract tests
├── e2e/                   # End-to-end tests
└── performance/           # Load and stress tests
```

---

## 5. FOLDER ORGANIZATION

### 5.1 Feature-Based Organization

```
src/domain/
├── repository/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   └── repository_entity.py
│   ├── value_objects/
│   │   ├── __init__.py
│   │   └── repository_status.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── repository_health_service.py
│   ├── events/
│   │   ├── __init__.py
│   │   └── repository_registered.py
│   └── repositories/
│       ├── __init__.py
│       └── repository_repository.py     # Interface
```

### 5.2 Shared Utilities

```
shared/
├── __init__.py
├── types.py               # Common type definitions
├── constants.py           # Shared constants
├── exceptions.py          # Base exception classes
├── events.py              # Base event classes
├── utils.py               # Utility functions
└── testing/
    ├── __init__.py
    ├── fixtures.py         # Shared test fixtures
    ├── factories.py        # Test data factories
    └── mocks.py            # Shared mock objects
```

---

## 6. EVENT STANDARDS

### 6.1 Event Naming

Pattern: `{domain}.{entity}.{action}`

| Domain | Entity | Action | Full Event Name |
|--------|--------|--------|----------------|
| platform | repository | registered | `platform.repository.registered` |
| platform | module | installed | `platform.module.installed` |
| platform | service | published | `platform.service.published` |
| governance | finding | raised | `governance.finding.raised` |
| governance | review | completed | `governance.review.completed` |
| governance | certification | granted | `governance.certification.granted` |
| discovery | scan | completed | `discovery.scan.completed` |
| discovery | health | scored | `discovery.health.scored` |

### 6.2 Event Structure

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "platform.repository.registered",
  "source": "platform-core/registry",
  "data": {
    "repositoryId": "repo-123",
    "name": "module-name",
    "version": "1.0.0",
    "registeredAt": "2026-06-25T10:00:00Z"
  },
  "timestamp": "2026-06-25T10:00:00Z",
  "priority": "normal",
  "correlationId": "corr-456",
  "metadata": {
    "userId": "user-789",
    "sourceIp": "10.0.0.1",
    "userAgent": "platform-core/1.0.0"
  }
}
```

### 6.3 Event Schema Versioning

- Schema name: `{domain}-{entity}-{action}-v{N}`
- Breaking changes require new major schema version
- Old schemas retained for 12 months
- Schema registry managed by Platform-Core

---

## 7. API STANDARDS

### 7.1 REST API Design

| Standard | Convention |
|----------|-----------|
| Base URL | `/api/v{N}/{resource}` |
| Plural nouns | `/repositories`, `/modules`, `/services` |
| Nested resources | `/repositories/{id}/services` |
| Filtering | Query parameters: `?status=active&category=clinical` |
| Sorting | `?sort=created_at:desc` |
| Pagination | `?limit=20&cursor={cursor}` |
| Partial response | `?fields=id,name,status` |

### 7.2 HTTP Methods

| Method | Purpose | Response |
|--------|---------|----------|
| `GET` | Read resource(s) | 200 OK |
| `POST` | Create resource | 201 Created |
| `PUT` | Replace resource | 200 OK |
| `PATCH` | Partial update | 200 OK |
| `DELETE` | Remove resource | 204 No Content |

### 7.3 Response Format

**Success**:
```json
{
  "data": { ... },
  "meta": {
    "requestId": "req-123",
    "timestamp": "2026-06-25T10:00:00Z",
    "duration": "15ms"
  }
}
```

**Paginated**:
```json
{
  "data": [ ... ],
  "pagination": {
    "limit": 20,
    "cursor": "eyJpZCI6MTAwfQ==",
    "hasMore": true,
    "total": 150
  },
  "meta": { ... }
}
```

**Error** (RFC 7807):
```json
{
  "type": "https://platform.unified/errors/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "Repository name already exists",
  "instance": "/api/v1/repositories",
  "errors": [
    {
      "field": "name",
      "message": "Name 'my-repo' already exists",
      "code": "DUPLICATE"
    }
  ],
  "meta": {
    "requestId": "req-124",
    "timestamp": "2026-06-25T10:00:01Z"
  }
}
```

### 7.4 Standard Endpoints

Every module must expose:

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Liveness probe |
| `GET /ready` | Readiness probe |
| `GET /metrics` | Prometheus metrics |
| `GET /api/v{N}` | API root with links |
| `GET /api/v{N}/docs` | OpenAPI documentation |

### 7.5 OpenAPI Documentation

Every API must include:
- Title, description, version
- Contact information
- License
- Tagged operations by resource
- Request/response schemas
- Error response schemas
- Security schemes (Bearer token, API key)
- Example values for all parameters

---

## 8. DTO PATTERNS

### 8.1 Request DTOs

```python
# Python (Pydantic v2)
from pydantic import BaseModel, Field

class CreateRepositoryRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, pattern=r'^[a-z0-9-]+$')
    description: str = Field(..., max_length=500)
    category: Literal["clinical", "operational", "infrastructure"]
    version: str = Field(..., pattern=r'^\d+\.\d+\.\d+$')
```

### 8.2 Response DTOs

```python
class RepositoryResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    version: str
    status: str
    healthScore: float | None
    createdAt: datetime
    updatedAt: datetime
```

### 8.3 Internal DTOs (Domain Transfer)

```python
class RepositoryData(BaseModel):
    """Internal transfer between layers — not exposed via API."""
    id: str
    name: str
    status: RepositoryStatus
    metadata: dict[str, Any]
```

---

## 9. ERROR HANDLING

### 9.1 Exception Hierarchy

```
PlatformError (base)
├── ValidationError
│   ├── FieldValidationError
│   ├── SchemaValidationError
│   └── BusinessRuleValidationError
├── NotFoundError
│   ├── RepositoryNotFoundError
│   ├── ModuleNotFoundError
│   └── ServiceNotFoundError
├── ConflictError
│   ├── DuplicateError
│   ├── VersionConflictError
│   └── StateConflictError
├── AuthenticationError
│   ├── InvalidTokenError
│   └── ExpiredTokenError
├── AuthorizationError
│   └── InsufficientPermissionsError
├── ExternalServiceError
│   ├── ServiceUnavailableError
│   └── ServiceTimeoutError
└── InternalError
    ├── ConfigurationError
    ├── DatabaseError
    └── SerializationError
```

### 9.2 Error Response Mapping

| Exception | HTTP Status | Error Code |
|-----------|------------|------------|
| ValidationError | 400 | VALIDATION_ERROR |
| NotFoundError | 404 | NOT_FOUND |
| ConflictError | 409 | CONFLICT |
| AuthenticationError | 401 | UNAUTHORIZED |
| AuthorizationError | 403 | FORBIDDEN |
| ExternalServiceError | 502 | BAD_GATEWAY |
| InternalError | 500 | INTERNAL_ERROR |

### 9.3 Logging on Error

```python
try:
    result = await service.register_repository(request)
except ValidationError as e:
    logger.warning("Validation failed", error=str(e), requestId=request_id)
    raise
except Exception as e:
    logger.error("Unexpected error", error=str(e), exc_info=True, requestId=request_id)
    raise InternalError("An unexpected error occurred") from e
```

---

## 10. LOGGING STANDARDS

### 10.1 Structured Log Format

```json
{
  "timestamp": "2026-06-25T10:00:00.123Z",
  "level": "info",
  "message": "Repository registered successfully",
  "logger": "platform_core.registry.repository_service",
  "correlationId": "corr-789",
  "requestId": "req-123",
  "userId": "user-456",
  "module": "registry",
  "action": "register_repository",
  "repositoryName": "my-module",
  "duration": "45ms",
  "traceId": "abc123def456",
  "spanId": "span789"
}
```

### 10.2 Log Levels

| Level | When to Use |
|-------|------------|
| `DEBUG` | Detailed diagnostic information, development only |
| `INFO` | Normal operations: startup, shutdown, successful operations |
| `WARN` | Unexpected but recoverable: degraded performance, retry |
| `ERROR` | Failures requiring attention: operation failed, exception |
| `CRITICAL` | System-wide failures: data loss, security breach |

### 10.3 Correlation IDs

- Every request gets a correlation ID (UUID v4)
- Correlation ID propagated across all service calls
- Correlation ID included in all log entries for the request
- Correlation ID returned in response headers

### 10.4 Audit Logging

Every mutation must produce an audit log entry:

```json
{
  "timestamp": "2026-06-25T10:00:00Z",
  "action": "repository.registered",
  "subject": "my-module",
  "actor": "user-456",
  "sourceIp": "10.0.0.1",
  "changes": {
    "status": { "from": null, "to": "active" },
    "healthScore": { "from": null, "to": 85.5 }
  },
  "result": "success"
}
```

---

## 11. TELEMETRY STANDARDS

### 11.1 Metrics

**RED Metrics** (every service):
| Metric | Type | Labels |
|--------|------|--------|
| `http_requests_total` | Counter | method, path, status |
| `http_request_duration_seconds` | Histogram | method, path |
| `http_request_size_bytes` | Histogram | method, path |
| `http_response_size_bytes` | Histogram | method, path |

**Business Metrics** (per module):
| Metric | Type | Labels |
|--------|------|--------|
| `platform_repositories_total` | Gauge | status, category |
| `platform_modules_installed_total` | Gauge | status, category |
| `platform_health_score` | Gauge | repository, category |
| `platform_findings_total` | Counter | severity, type |
| `platform_certifications_total` | Gauge | level, status |

### 11.2 Distributed Tracing

- Use OpenTelemetry SDK
- Propagate trace context via W3C TraceContext headers
- Create spans for every significant operation
- Record span attributes: `repository.name`, `module.version`, etc.
- Sample rate: 100% in development, 10% in production

### 11.3 Health Checks

```python
# Liveness: Is the process alive?
GET /health → 200 { "status": "healthy" }

# Readiness: Can the service accept traffic?
GET /ready → 200 {
  "status": "ready",
  "checks": {
    "database": "healthy",
    "redis": "healthy",
    "eventBus": "healthy"
  }
}
```

---

## 12. CONFIGURATION STANDARDS

### 12.1 Configuration Sources (Priority Order)

```
1. Environment variables (highest priority)
2. Configuration files (.env, config.yaml, config.json)
3. Default values (lowest priority)
```

### 12.2 Environment Variables

Naming: `MODULE_SUBSECTION_KEY`

```
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/platform_core
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://localhost:6379/0

# API
API_HOST=0.0.0.0
API_PORT=8080
API_WORKERS=4

# Auth
JWT_SECRET_KEY=env:JWT_SECRET_KEY
JWT_ALGORITHM=HS256
JWT_EXPIRATION_SECONDS=3600

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_OUTPUT=stdout

# Telemetry
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_SERVICE_NAME=platform-core
OTEL_SAMPLE_RATE=0.1
```

### 12.3 Configuration File Format

```yaml
# config.yaml
server:
  host: "0.0.0.0"
  port: 8080
  workers: 4

database:
  url: "${DATABASE_URL}"
  pool_size: 20
  max_overflow: 10

redis:
  url: "${REDIS_URL}"

logging:
  level: INFO
  format: json
```

### 12.4 Secrets Management

- Never commit secrets to version control
- Use environment variables for all secrets
- Use platform secret manager in production (Vault, AWS Secrets Manager)
- Rotate secrets on a schedule (90-day maximum)
- Support secret references: `env:SECRET_NAME` or `vault:secret/path`

---

## 13. TESTING STANDARDS

### 13.1 Test Pyramid

```
         ╱╲
        ╱  ╲         E2E Tests (5%)
       ╱    ╲        Manual exploratory
      ╱──────╲
     ╱        ╲      Integration Tests (25%)
    ╱          ╲     Service interactions, database
   ╱────────────╲
  ╱              ╲   Unit Tests (70%)
 ╱                ╲  Individual functions, domain logic
╱──────────────────╲
```

### 13.2 Unit Tests

- Test individual functions and methods
- Mock all external dependencies
- Target: >90% code coverage
- Framework: `pytest` (Python), `vitest` (TypeScript)

```python
def test_register_repository_success():
    repo = InMemoryRepositoryRepository()
    service = RepositoryService(repository=repo)
    
    result = service.register(name="test-repo", version="1.0.0")
    
    assert result.name == "test-repo"
    assert result.status == RepositoryStatus.ACTIVE

def test_register_repository_duplicate_raises():
    repo = InMemoryRepositoryRepository()
    repo.save(Repository(name="existing", version="1.0.0"))
    service = RepositoryService(repository=repo)
    
    with pytest.raises(ConflictError):
        service.register(name="existing", version="1.0.0")
```

### 13.3 Integration Tests

- Test service interactions
- Use real databases (test containers)
- Test API endpoints end-to-end
- Target: >80% coverage of integration paths

### 13.4 Contract Tests

- Validate API contracts against OpenAPI specs
- Validate event schemas against registered schemas
- Run on every CI build
- Target: 100% of public contracts

### 13.5 Test Naming Convention

Pattern: `test_{function_name}_{scenario}_{expected_result}`

```python
def test_register_repository_with_duplicate_name_raises_conflict():
def test_health_score_calculator_with_valid_data_returns_score():
def test_event_bus_publish_with_no_subscribers_succeeds():
```

---

## 14. DOCUMENTATION STANDARDS

### 14.1 Required Documentation

| Document | Location | Mandatory |
|----------|----------|-----------|
| README.md | Root | Yes |
| CHANGELOG.md | Root | Yes |
| manifest.yaml | Root | Yes |
| API documentation | Auto-generated OpenAPI | Yes |
| Architecture Decision Records | `docs/adr/` | Yes (significant decisions) |
| Runbooks | `docs/operations/` | Yes (production modules) |
| Inline docstrings | Source code | Yes (public API) |

### 14.2 README Template

```markdown
# Module Name

## Overview
## Quick Start
## Installation
## Configuration
## API Reference
## Architecture
## Development
## Testing
## Deployment
## License
```

### 14.3 Changelog Format

Follow Keep a Changelog:

```markdown
# Changelog

## [1.1.0] - 2026-06-25
### Added
- New feature X

### Changed
- Improved performance of Y

### Fixed
- Bug in Z

### Deprecated
- Feature W (will be removed in 2.0.0)

### Removed
- Legacy support for V
```

### 14.4 Code Documentation

- All public classes and functions must have docstrings
- Use Google-style docstrings (Python) or JSDoc (TypeScript)
- Document parameters, return values, and exceptions
- Include usage examples for complex functions

---

## 15. SECURITY PRACTICES

### 15.1 Development Security

| Practice | Requirement |
|----------|------------|
| Secrets in code | NEVER — use environment variables |
| Dependencies | Automated vulnerability scanning |
| Input validation | Validate all external inputs |
| Output encoding | Encode all outputs to prevent injection |
| Authentication | JWT tokens with short expiration |
| Authorization | RBAC on every endpoint |
| Rate limiting | Token bucket per client |
| CORS | Whitelist allowed origins only |

### 15.2 CI/CD Security

| Practice | Requirement |
|----------|------------|
| SAST | Static analysis on every commit |
| SCA | Software composition analysis |
| Container scanning | Scan images before push |
| Secret scanning | Detect committed secrets |
| Signed commits | GPG signing required |
| Branch protection | Require reviews, CI pass |

### 15.3 Production Security

| Practice | Requirement |
|----------|------------|
| TLS | TLS 1.3 for all traffic |
| Encryption at rest | Database and disk encryption |
| Audit logging | All mutations logged |
| Incident response | Documented runbooks |
| Penetration testing | Annual third-party audit |
| SOC 2 compliance | Required for production |

---

## 16. CERTIFICATE MANAGEMENT

### 16.1 Certificate Types

| Type | Purpose | Validity | Rotation |
|------|---------|----------|----------|
| TLS Server | HTTPS encryption | 90 days | Automated (certbot) |
| TLS Client | mTLS service-to-service | 90 days | Automated |
| Code Signing | Package integrity | 1 year | Manual + automated |
| Manifest Signing | Manifest integrity | 1 year | Manual + automated |

### 16.2 Certificate Lifecycle

```
Generate → Store (Vault/KMS) → Deploy → Monitor → Rotate → Revoke
    │            │                │         │          │         │
    └────────────┴────────────────┴─────────┴──────────┴─────────┘
                         Automated Pipeline
```

### 16.3 Key Storage

| Environment | Storage | Access |
|-------------|---------|--------|
| Development | Local `.env` file | Developer workstation |
| Staging | Platform secret manager | CI/CD pipeline |
| Production | Vault / AWS KMS | Runtime identity engine |

---

## 17. DIGITAL SIGNATURES

### 17.1 Signing Requirements

| Artifact | Signing Required | Algorithm |
|----------|-----------------|-----------|
| Platform Manifests | Yes | Ed25519 |
| Release Packages | Yes | Ed25519 |
| Container Images | Yes | cosign (Sigstore) |
| Git Commits | Recommended | GPG / SSH |
| API Requests | Optional (mTLS) | ECDSA |

### 17.2 Signature Verification Flow

```
Artifact → Download → Fetch Public Key → Verify Signature → Trust Decision
                                          │
                                          ├── Key in trust store? → ACCEPT
                                          └── Key not in store? → REJECT
```

### 17.3 Trust Store

- Platform-Core maintains the trust store
- Public keys registered per module owner
- Trust store backed by PostgreSQL
- Trust chain: Root CA → Intermediate → Module Keys

---

## 18. CI/CD STANDARDS

### 18.1 Pipeline Stages

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Lint    │──→│  Test    │──→│  Build   │──→│  Scan    │──→│  Deploy  │
│          │   │          │   │          │   │          │   │          │
│ ruff     │   │ pytest   │   │ docker   │   │ trivy    │   │ k8s/     │
│ mypy     │   │ coverage │   │ build    │   │ sast     │   │ docker   │
│ eslint   │   │ contract │   │ package  │   │ sca      │   │ compose  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

### 18.2 Gate Criteria

| Gate | Criteria |
|------|----------|
| Lint | Zero errors, zero warnings (or approved waivers) |
| Test | >90% coverage, all tests pass |
| Build | Image builds successfully, manifest valid |
| Scan | Zero critical/high vulnerabilities |
| Deploy | Staging deployment succeeds, smoke tests pass |

---

*Document generated as part of Platform-Core V2.0 Bootstrap Program*
*Constitution Reference: Articles I, VII, XII, XVII*
