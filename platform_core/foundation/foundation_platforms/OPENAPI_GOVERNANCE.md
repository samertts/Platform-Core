# OPENAPI GOVERNANCE

**NHDOS Platform-Core — Foundation Platform 11: OpenAPI Governance**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The OpenAPI Governance platform defines and enforces OpenAPI specification standards across NHDOS, ensuring consistent API documentation, validation, and discoverability for all REST APIs.

---

## 2. Architecture

### 2.1 Core Principles

| Principle | Description |
|-----------|-------------|
| Specification-First | OpenAPI spec before implementation |
| Consistent | Uniform documentation style |
| Validated | Spec validated against rules |
| Published | Centralized API catalog |
| Tested | Contract testing enforced |

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    OPENAPI GOVERNANCE                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Spec        │  │   Validator  │  │   Publisher  │          │
│  │  Repository  │──▶│   Engine     │──▶│   Portal     │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │  Code Gen    │  │   Contract   │  │   Version    │          │
│  │  Engine      │  │   Testing    │  │   Manager    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. OpenAPI Standards

### 3.1 Required Fields

| Field | Description |
|-------|-------------|
| openapi | OpenAPI version (3.0.3+) |
| info.title | API title |
| info.version | API version |
| info.description | API description |
| servers | Server URLs |
| paths | API endpoints |
| components.schemas | Data models |

### 3.2 Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Paths | kebab-case | `/patient-records` |
| Operations | camelCase | `getPatientRecord` |
| Parameters | camelCase | `patientId` |
| Schemas | PascalCase | `PatientRecord` |
| Properties | camelCase | `firstName` |

### 3.3 Documentation Requirements

| Requirement | Description |
|-------------|-------------|
| Summary | Short description |
| Description | Detailed description |
| Examples | Request/response examples |
| Error Responses | All error responses documented |
| Tags | API grouped by tags |

---

## 4. Validation Rules

### 4.1 Linting Rules

| Rule | Description | Severity |
|------|-------------|----------|
| OperationId | All operations have operationId | Error |
| Description | All endpoints have description | Error |
| ResponseSchema | All responses have schema | Error |
| Examples | All endpoints have examples | Warning |
| Deprecation | Deprecated endpoints marked | Error |

### 4.2 Quality Gates

| Gate | Description | Blocking |
|------|-------------|----------|
| Spec Valid | OpenAPI spec is valid | Yes |
| Lint Pass | Linting rules pass | Yes |
| Contract Test | Contract tests pass | Yes |
| Documentation | Documentation complete | Yes |

---

## 5. Code Generation

### 5.1 Supported Languages

| Language | Generator | Package |
|----------|-----------|---------|
| Python | openapi-generator | nhdos-sdk-python |
| TypeScript | openapi-generator | nhdos-sdk-typescript |
| Flutter | openapi-generator | nhdos-sdk-flutter |
| Kotlin | openapi-generator | nhdos-sdk-kotlin |
| Swift | openapi-generator | nhdos-sdk-swift |
| Java | openapi-generator | nhdos-sdk-java |
| .NET | openapi-generator | nhdos-sdk-dotnet |
| Go | openapi-generator | nhdos-sdk-go |

---

## 6. APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/openapi/specs | GET | List all specs |
| /api/v1/openapi/specs/{api} | GET | Get API spec |
| /api/v1/openapi/specs/{api}/validate | POST | Validate spec |
| /api/v1/openapi/specs/{api}/publish | POST | Publish to portal |
| /api/v1/openapi/specs/{api}/generate | POST | Generate SDK |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
