# OPENAPI STANDARDS

**NHDOS Platform-Core — OpenAPI Governance**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS OpenAPI Standards establish consistent API documentation, validation, and governance across all platform services. It defines OpenAPI specification requirements, naming conventions, security schemes, and automated validation to ensure high-quality API contracts.

---

## 2. Architecture Overview

### 2.1 OpenAPI Governance Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 OpenAPI Governance                       │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Schema    │  │  Validation │  │  Generator  │     │
│  │   Registry  │  │   Engine    │  │   (SDKs)    │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │              │
│         └────────┬───────┴────────┬───────┘              │
│                  │                │                       │
│         ┌────────▼────────┐ ┌────▼────────────┐         │
│         │  OpenAPI Store  │ │  Linting Rules  │         │
│         │  (Git + Registry│ │  (Spectral)     │         │
│         └─────────────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. OpenAPI Specification Requirements

### 3.1 Required Fields

```yaml
openapi: "3.0.3"
info:
  title: "NHDOS Patient Service API"
  version: "1.0.0"
  description: "Patient management endpoints"
  contact:
    name: "Platform Core Team"
    email: "platform-core@nhdos.iq"
  license:
    name: "NHDOS Internal"
    url: "https://nhdos.iq/licenses/internal"

servers:
  - url: "https://api.nhdos.iq/v1"
    description: "Production"
  - url: "https://staging-api.nhdos.iq/v1"
    description: "Staging"

paths: {}
components:
  securitySchemes: {}
```

### 3.2 Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Paths | kebab-case | `/patient-records` |
| Operations | camelCase | `getPatientRecord` |
| Parameters | camelCase | `patientId` |
| Properties | camelCase | `medicalRecordNumber` |
| Enums | SCREAMING_SNAKE_CASE | `ACTIVE`, `INACTIVE` |

### 3.3 Response Schema

```yaml
components:
  schemas:
    Patient:
      type: object
      required:
        - id
        - nationalId
        - status
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        nationalId:
          type: string
          pattern: "^[0-9]{10}$"
        status:
          $ref: "#/components/schemas/PatientStatus"
        createdAt:
          type: string
          format: date-time
          readOnly: true

    PatientStatus:
      type: string
      enum:
        - ACTIVE
        - INACTIVE
        - DECEASED
```

---

## 4. Security Schemes

### 4.1 Authentication Methods

| Method | Usage | Description |
|--------|-------|-------------|
| Bearer JWT | External APIs | OAuth 2.0 tokens |
| API Key | Service-to-service | Internal API keys |
| mTLS | Service mesh | Mutual TLS |
| OAuth 2.0 | Third-party | OAuth flows |

### 4.2 Security Scheme Definition

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
      
    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: "https://auth.nhdos.iq/authorize"
          tokenUrl: "https://auth.nhdos.iq/token"
          scopes:
            patient:read: Read patient data
            patient:write: Write patient data
```

---

## 5. Validation Rules

### 5.1 Spectral Rules

```yaml
rules:
  # Naming conventions
  operation-operationId: warn
  operation-operationId-pascal-case: error
  
  # Response codes
  operation-4xx-response: error
  operation-5xx-response: warn
  
  # Documentation
  oas3-api-servers: error
  oas3-operation-security-defined: error
  
  # Schema
  oas3-schema: error
```

### 5.2 Validation Pipeline

```
1. Schema validation (OpenAPI spec)
2. Linting (Spectral rules)
3. Breaking change detection
4. Security review
5. Documentation completeness
6. SDK generation test
```

---

## 6. APIs

### 6.1 OpenAPI Management API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/openapi/specs` | GET | List all specs |
| `/api/v1/openapi/specs/{service}` | GET | Get service spec |
| `/api/v1/openapi/specs/{service}/validate` | POST | Validate spec |
| `/api/v1/openapi/specs/{service}/lint` | POST | Lint spec |
| `/api/v1/openapi/compare` | POST | Compare specs |

### 6.2 SDK Generation

```yaml
# sdk-generation.yaml
generator: openapi-generator
templates:
  python:
    package_name: "nhdos-patient-sdk"
    version: "1.0.0"
  typescript:
    package_name: "@nhdos/patient-sdk"
    version: "1.0.0"
  java:
    package_name: "iq.nhdos.patient.sdk"
    version: "1.0.0"
```

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
