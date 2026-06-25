# API VERSIONING

**NHDOS Platform-Core — API Versioning Strategy**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS API Versioning Strategy ensures backward compatibility, controlled evolution, and clear communication of API changes across all platform services. It establishes versioning conventions, deprecation policies, and migration paths to maintain stable integrations.

---

## 2. Architecture Overview

### 2.1 Versioning Strategy

```
┌─────────────────────────────────────────────────────────┐
│                   API Versioning                         │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  URL-Based  │  │   Header    │  │   Content   │     │
│  │  Versioning │  │  Versioning │  │  Negotiation│     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │              │
│         └────────┬───────┴────────┬───────┘              │
│                  │                │                       │
│         ┌────────▼────────┐ ┌────▼────────────┐         │
│         │   Version       │ │  Deprecation    │         │
│         │   Router        │ │  Manager        │         │
│         └─────────────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Versioning Methods

| Method | Usage | Example |
|--------|-------|---------|
| URL Path | Primary (external APIs) | `/api/v1/patients` |
| Header | Secondary (internal APIs) | `X-API-Version: 1` |
| Query Parameter | Fallback | `?api_version=1` |

---

## 3. Versioning Conventions

### 3.1 Version Number Format

```
MAJOR.MINOR

MAJOR: Breaking changes (incompatible API changes)
MINOR: Backward-compatible additions
```

### 3.2 Version Lifecycle

| Phase | Duration | Description |
|-------|----------|-------------|
| Active | 24 months | Full support, new features |
| Maintenance | 12 months | Bug fixes only |
| Deprecated | 6 months | Migration period |
| Retired | - | Removed from service |

---

## 4. Breaking Changes

### 4.1 Breaking Change Definition

| Change Type | Breaking | Migration Required |
|-------------|----------|-------------------|
| Remove field | Yes | Yes |
| Rename field | Yes | Yes |
| Change field type | Yes | Yes |
| Change enum values | Yes | Yes |
| Add required field | Yes | Yes |
| Change URL structure | Yes | Yes |
| Add optional field | No | No |
| Add new endpoint | No | No |
| Add new enum value | No | No |

### 4.2 Version Compatibility Matrix

| Change | v1 | v2 | v3 | Notes |
|--------|----|----|----|----|
| Patient endpoints | ✓ | ✓ | ✓ | Core API |
| Appointment endpoints | ✓ | ✓ | ✓ | Core API |
| Lab results endpoints | ✓ | ✓ | ✓ | Core API |
| FHIR integration | - | ✓ | ✓ | Added in v2 |
| GraphQL gateway | - | - | ✓ | Added in v3 |

---

## 5. Deprecation Policy

### 5.1 Deprecation Process

```
1. Announce deprecation (90 days notice)
2. Add deprecation headers
3. Document migration guide
4. Monitor usage reduction
5. Final warning (30 days)
6. Remove deprecated endpoints
```

### 5.2 Deprecation Headers

```http
HTTP/1.1 200 OK
Deprecation: Sat, 01 Sep 2026 00:00:00 GMT
Sunset: Sun, 01 Mar 2027 00:00:00 GMT
Link: <https://docs.nhdos.iq/api/v2/migration>; rel="successor-version"
```

---

## 6. APIs

### 6.1 Version Management API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/versions` | GET | List all versions |
| `/api/v1/versions/{version}` | GET | Get version details |
| `/api/v1/versions/{version}/deprecate` | POST | Deprecate version |
| `/api/v1/versions/{version}/retire` | POST | Retire version |
| `/api/v1/versions/compare` | GET | Compare versions |

### 6.2 Client SDK Versioning

```python
from nhdos_sdk import Client

# Specific version
client = Client(api_version="v1", environment="production")

# Auto-negotiate
client = Client(api_version="latest", environment="production")

# Version check
current_version = client.get_api_version()
if current_version.is_deprecated:
    print(f"Warning: API {current_version} is deprecated")
```

---

## 7. Implementation Details

### 7.1 Version Router

```python
class APIVersionRouter:
    def route(self, request: Request) -> Response:
        version = self.extract_version(request)
        
        if version not in self.supported_versions:
            return self.handle_unsupported_version(version)
        
        if version.is_deprecated:
            return self.add_deprecation_headers(response, version)
        
        return self.dispatch_to_version(version, request)
```

### 7.2 Version Discovery

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/versions` | GET | List available versions |
| `/api/versions/{version}/changelog` | GET | Version changelog |
| `/api/versions/{version}/spec` | GET | OpenAPI specification |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
