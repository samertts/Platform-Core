# PLATFORM MANIFEST VALIDATION RULES

**Document**: Manifest Validation Rules
**Version**: 1.0.0
**Date**: 2026-06-25
**Constitution Reference**: Article IV — Manifest Standard

---

## 1. VALIDATION OVERVIEW

Every manifest submitted to Platform-Core is validated against a comprehensive rule set. Validation results determine whether a manifest is accepted, rejected, or accepted with warnings.

---

## 2. VALIDATION CATEGORIES

### 2.1 SCHEMA VALIDATION

Validates manifest structure against the JSON Schema.

| Rule ID | Rule | Severity |
|---------|------|----------|
| SCHEMA-001 | Manifest must conform to JSON Schema | ERROR |
| SCHEMA-002 | No additional properties allowed at root level | ERROR |
| SCHEMA-003 | All required sections must be present | ERROR |

### 2.2 IDENTITY VALIDATION

Validates repository identity fields.

| Rule ID | Rule | Severity |
|---------|------|----------|
| ID-001 | Name must match pattern `^[a-z][a-z0-9-]*[a-z0-9]$` | ERROR |
| ID-002 | Name must be 3-63 characters | ERROR |
| ID-003 | Slug must match name pattern | ERROR |
| ID-004 | Description must be 10-500 characters | ERROR |
| ID-005 | Name must be globally unique across platform | ERROR |
| ID-006 | Slug must be globally unique across platform | ERROR |
| ID-007 | Type must be one of: platform-core, module, adapter, sdk, tool | ERROR |

### 2.3 OWNERSHIP VALIDATION

Validates ownership fields.

| Rule ID | Rule | Severity |
|---------|------|----------|
| OWN-001 | Team must be non-empty | ERROR |
| OWN-002 | Organization must be non-empty | ERROR |
| OWN-003 | Contact must be valid email format | ERROR |
| OWN-004 | Repository URL must be valid URI | ERROR |

### 2.4 RUNTIME VALIDATION

Validates runtime requirements.

| Rule ID | Rule | Severity |
|---------|------|----------|
| RT-001 | Language must be one of the supported languages | ERROR |
| RT-002 | Language version must be valid semver range | WARNING |
| RT-003 | Environment variable names must match `^[A-Z][A-Z0-9_]*$` | ERROR |
| RT-004 | Container ports must be valid port mappings | ERROR |

### 2.5 MATURITY VALIDATION

Validates maturity and certification.

| Rule ID | Rule | Severity |
|---------|------|----------|
| MAT-001 | Level must be one of: experimental, alpha, beta, stable, mature, legacy | ERROR |
| MAT-002 | Since date must be valid ISO 8601 date | ERROR |
| MAT-003 | Since date must not be in the future | WARNING |
| MAT-004 | Certification level must be one of: basic, standard, clinical, national | ERROR |

### 2.6 SERVICE VALIDATION

Validates service definitions.

| Rule ID | Rule | Severity |
|---------|------|----------|
| SVC-001 | Service name must match pattern `^[a-z][a-z0-9-]*[a-z0-9]$` | ERROR |
| SVC-002 | Service name must be unique within repository | ERROR |
| SVC-003 | Service type must be one of: core, module, adapter, gateway, worker, scheduler | ERROR |
| SVC-004 | Service version must be valid semver | ERROR |
| SVC-005 | Port must be in range 1024-65535 | ERROR |
| SVC-006 | Health endpoint must start with `/` | WARNING |
| SVC-007 | Metrics endpoint must start with `/` | WARNING |
| SVC-008 | Core services can only be in platform-core repositories | ERROR |

### 2.7 API VALIDATION

Validates API definitions.

| Rule ID | Rule | Severity |
|---------|------|----------|
| API-001 | API name must match pattern `^[a-z][a-z0-9-]*[a-z0-9]$` | ERROR |
| API-002 | API name must be unique within repository | ERROR |
| API-003 | Base path must start with `/` | ERROR |
| API-004 | Base path should include version prefix (e.g., `/v1/`) | WARNING |
| API-005 | Version must be valid semver | ERROR |
| API-006 | Authentication must not be `none` for production APIs | WARNING |
| API-007 | Rate limit requests_per_minute must be positive | ERROR |

### 2.8 EVENT VALIDATION

Validates event definitions.

| Rule ID | Rule | Severity |
|---------|------|----------|
| EVT-001 | Event name must match pattern `^[a-z][a-z0-9.]*[a-z0-9]$` | ERROR |
| EVT-002 | Event name must be unique within repository | ERROR |
| EVT-003 | Event name should follow domain.action format | INFO |
| EVT-004 | Version must be valid semver | ERROR |
| EVT-005 | Retention days must be positive | ERROR |
| EVT-006 | Domain events should have retention >= 30 days | WARNING |

### 2.9 DEPENDENCY VALIDATION

Validates dependency declarations.

| Rule ID | Rule | Severity |
|---------|------|----------|
| DEP-001 | Dependency name must be non-empty | ERROR |
| DEP-002 | Dependency type must be valid enum value | ERROR |
| DEP-003 | Version must be valid semver range | WARNING |
| DEP-004 | Platform dependencies must reference existing repositories | WARNING |
| DEP-005 | Circular dependencies are not allowed | ERROR |
| DEP-006 | Critical dependencies must not be optional | ERROR |

### 2.10 COMPATIBILITY VALIDATION

Validates version compatibility.

| Rule ID | Rule | Severity |
|---------|------|----------|
| COMP-001 | platform_core must be valid semver range | ERROR |
| COMP-002 | min_platform_core must be valid semver range | ERROR |
| COMP-003 | min_platform_core must be <= platform_core | ERROR |
| COMP-004 | min_platform_core should not be more than 2 major versions behind | WARNING |

### 2.11 CROSS-SECTION VALIDATION

Validates consistency across manifest sections.

| Rule ID | Rule | Severity |
|---------|------|----------|
| XSEC-001 | If services are declared, at least one API or event must exist | WARNING |
| XSEC-002 | If type is module, at least one service must exist | ERROR |
| XSEC-003 | If type is adapter, at least one device must exist | ERROR |
| XSEC-004 | Event publisher must be a declared service | WARNING |
| XSEC-005 | API must be associated with a declared service | WARNING |

### 2.12 SECURITY VALIDATION

Validates security requirements.

| Rule ID | Rule | Severity |
|---------|------|----------|
| SEC-001 | No environment variable may have a default value containing "secret", "password", "key", or "token" (case-insensitive) | ERROR |
| SEC-002 | No hardcoded URLs containing credentials | ERROR |
| SEC-003 | Signed manifest recommended for production | INFO |
| SEC-004 | API authentication should not be `none` | WARNING |

### 2.13 CONSTITUTION VALIDATION

Validates compliance with Constitution.

| Rule ID | Rule | Severity |
|---------|------|----------|
| GOV-001 | Manifest must exist in repository root | ERROR |
| GOV-002 | Repository must not share databases (inferred from dependencies) | WARNING |
| GOV-003 | Shared services (type=core) must only be in platform-core | ERROR |
| GOV-004 | All APIs must be versioned | ERROR |
| GOV-005 | All events must be versioned | ERROR |

---

## 3. VALIDATION SEVERITY LEVELS

| Level | Count | Action |
|-------|-------|--------|
| `error` | 0 | Manifest is VALID, register in Repository Registry |
| `error` | > 0 | Manifest is INVALID, reject registration |
| `warning` | > 0 | Manifest is VALID with advisories, log warnings |
| `info` | > 0 | Manifest is VALID with suggestions, log info |

---

## 4. VALIDATION PROCESS

```
┌─────────────┐
│  Manifest    │
│  Submitted   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Schema      │
│  Validation  │──── ERROR ────→ REJECTED
└──────┬──────┘
       │ PASS
       ▼
┌─────────────┐
│  Field       │
│  Validation  │──── ERROR ────→ REJECTED
└──────┬──────┘
       │ PASS
       ▼
┌─────────────┐
│  Cross-      │
│  Section     │──── ERROR ────→ REJECTED
│  Validation  │
└──────┬──────┘
       │ PASS
       ▼
┌─────────────┐
│  Security    │
│  Validation  │──── ERROR ────→ REJECTED
└──────┬──────┘
       │ PASS
       ▼
┌─────────────┐
│  Constitution│
│  Validation  │──── ERROR ────→ REJECTED
└──────┬──────┘
       │ PASS
       ▼
┌─────────────┐
│  VALID       │
│  (register)  │
└─────────────┘
```

---

## 5. VALIDATION OUTPUT

### 5.1 Success Response

```json
{
  "status": "valid",
  "manifest_id": "uuid",
  "repository": "platform-core",
  "validated_at": "2026-06-25T00:00:00Z",
  "warnings": [],
  "info": []
}
```

### 5.2 Failure Response

```json
{
  "status": "invalid",
  "manifest_id": null,
  "repository": "platform-core",
  "validated_at": "2026-06-25T00:00:00Z",
  "errors": [
    {
      "rule_id": "ID-005",
      "section": "identity.name",
      "message": "Name 'Platform-Core' does not match required pattern",
      "severity": "error"
    }
  ],
  "warnings": [],
  "info": []
}
```

### 5.3 Warning Response

```json
{
  "status": "valid_with_warnings",
  "manifest_id": "uuid",
  "repository": "platform-core",
  "validated_at": "2026-06-25T00:00:00Z",
  "errors": [],
  "warnings": [
    {
      "rule_id": "API-006",
      "section": "apis[0].authentication",
      "message": "API 'platform-api' has authentication set to 'none'",
      "severity": "warning"
    }
  ],
  "info": []
}
```

---

## 6. VALIDATION FREQUENCY

| Trigger | Validation Type |
|---------|----------------|
| Manifest submission | Full validation |
| Scheduled (daily) | Re-validation of all active manifests |
| Platform-Core version update | Re-validation with new rules |
| Security rule update | Security-focused re-validation |

---

## 7. EXCEPTIONS AND WAIVERS

| Exception Type | Approval Required | Duration |
|---------------|-------------------|----------|
| Temporary waiver | Platform Architect | Max 30 days |
| Permanent exception | Governance Board | Until revoked |
| Emergency override | On-call Platform Architect | Max 72 hours |

---

*Document generated as part of Platform-Core V2.0 Bootstrap Program — Phase 3*
*Constitution Reference: Article IV — Manifest Standard*
