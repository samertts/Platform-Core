# ENGINEERING STANDARDS

**NHDOS Platform-Core — Phase 19: Platform Execution Framework**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

This document defines mandatory engineering standards for all modules in the National Healthcare Digital Operating System (NHDOS). Every repository, module, service, and component SHALL comply with these standards.

---

## 2. Repository Structure

### 2.1 Standard Repository Layout

```
repository/
├── src/
│   └── {module_name}/
│       ├── __init__.py
│       ├── core/
│       ├── api/
│       ├── models/
│       ├── services/
│       ├── events/
│       ├── contracts/
│       └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/
├── migrations/
├── config/
├── scripts/
├── .github/
│   └── workflows/
├── manifest.json
├── pyproject.toml
├── README.md
└── CHANGELOG.md
```

### 2.2 Directory Purposes

| Directory | Purpose |
|-----------|---------|
| src/ | Source code |
| tests/ | Test suite |
| docs/ | Documentation |
| migrations/ | Database migrations |
| config/ | Configuration files |
| scripts/ | Build and utility scripts |
| .github/workflows/ | CI/CD pipelines |

---

## 3. Coding Standards

### 3.1 Python Standards

| Standard | Requirement |
|----------|-------------|
| Python Version | 3.10+ |
| Type Hints | Mandatory for all public APIs |
| Docstrings | Google style, mandatory for all public functions |
| Line Length | 100 characters maximum |
| Imports | Sorted with isort |
| Formatting | Black formatter |
| Linting | Ruff linter |
| Naming | snake_case for functions/variables, PascalCase for classes |

### 3.2 TypeScript Standards

| Standard | Requirement |
|----------|-------------|
| TypeScript Version | 5.0+ |
| Strict Mode | Enabled |
| ESLint | Mandatory |
| Prettier | Mandatory |
| Naming | camelCase for functions/variables, PascalCase for classes/interfaces |

---

## 4. Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Module Name | snake_case | patient_registry |
| Class Name | PascalCase | PatientRegistry |
| Function Name | snake_case | get_patient_by_id |
| Variable Name | snake_case | patient_count |
| Constant Name | UPPER_SNAKE_CASE | MAX_RETRY_COUNT |
| API Endpoint | kebab-case | /api/v1/patients |
| Event Name | dot.notation | patient.created |
| Database Table | snake_case | patients |
| Database Column | snake_case | created_at |

---

## 5. Module Standards

### 5.1 Module Manifest

Every module SHALL have a `manifest.json`:

```json
{
  "name": "module_name",
  "version": "1.0.0",
  "type": "core|business|api|plugin",
  "description": "Module description",
  "author": "Organization",
  "license": "MIT",
  "dependencies": [],
  "provides": [],
  "events": [],
  "api": {},
  "health": {},
  "certification": {}
}
```

### 5.2 Module Requirements

| Requirement | Description |
|-------------|-------------|
| Manifest | Required manifest.json |
| Tests | Minimum 80% code coverage |
| Documentation | API documentation required |
| Health Check | Health endpoint required |
| Telemetry | Metrics and tracing required |
| Security | Security scan passing |
| Offline | Offline support documented |

---

## 6. API Standards

### 6.1 REST Standards

| Standard | Requirement |
|----------|-------------|
| Versioning | URL versioning (/api/v1/) |
| Naming | plural nouns for resources |
| Methods | GET, POST, PUT, DELETE, PATCH |
| Status Codes | Proper HTTP status codes |
| Pagination | Page and page_size parameters |
| Filtering | Query parameters for filtering |
| Sorting | sort_by and sort_order parameters |
| Errors | Consistent error response format |

### 6.2 Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [],
    "timestamp": "2026-01-15T10:30:00Z",
    "request_id": "uuid"
  }
}
```

---

## 7. Event Standards

### 7.1 Event Format

```json
{
  "event_id": "uuid",
  "event_type": "entity.action",
  "entity_type": "Patient",
  "entity_id": "uuid",
  "timestamp": "2026-01-15T10:30:00Z",
  "data": {},
  "metadata": {},
  "version": "1.0.0"
}
```

### 7.2 Event Naming

| Pattern | Example |
|---------|---------|
| entity.created | patient.created |
| entity.updated | patient.updated |
| entity.deleted | patient.deleted |
| entity.status_changed | patient.discharged |

---

## 8. Testing Standards

### 8.1 Test Types

| Type | Coverage | Execution |
|------|----------|-----------|
| Unit Tests | 80% minimum | Every commit |
| Integration Tests | Critical paths | Every PR |
| Performance Tests | SLA requirements | Weekly |
| Security Tests | OWASP Top 10 | Weekly |
| E2E Tests | User journeys | Release |

### 8.2 Test Naming

```python
def test_should_return_patient_when_valid_id():
    pass

def test_should_raise_error_when_patient_not_found():
    pass
```

---

## 9. Documentation Standards

| Document | Required | Content |
|----------|----------|---------|
| README.md | Yes | Overview, installation, usage |
| API Documentation | Yes | OpenAPI/Swagger spec |
| CHANGELOG.md | Yes | Version history |
| Architecture Decision Records | Yes | Key decisions |
| Runbooks | Yes | Operational procedures |

---

## 10. Security Standards

| Standard | Requirement |
|----------|-------------|
| Authentication | JWT with RS256 |
| Authorization | RBAC + ABAC |
| Encryption | AES-256-GCM at rest |
| Transport | TLS 1.3 in transit |
| Secrets | HashiCorp Vault |
| Scanning | SAST + DAST + Dependency |
| Audit | Complete audit trail |

---

*Generated as part of NHDOS Platform-Core Phase 19 Engineering Factory*
