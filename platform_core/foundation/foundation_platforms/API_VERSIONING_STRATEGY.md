# API VERSIONING STRATEGY

**NHDOS Platform-Core — Foundation Platform 10: API Versioning Strategy**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The API Versioning Strategy ensures backward compatibility, controlled evolution, and clear communication of API changes across all NHDOS platform services. It establishes versioning conventions, deprecation policies, and migration paths.

---

## 2. Architecture Overview

### 2.1 Versioning Methods

| Method | Usage | Example |
|--------|-------|---------|
| URL Path | Primary (external APIs) | `/api/v1/patients` |
| Header | Secondary (internal APIs) | `X-API-Version: 1` |
| Query Parameter | Fallback | `?api_version=1` |

### 2.2 Version Lifecycle

| Phase | Duration | Description |
|-------|----------|-------------|
| Active | 24 months | Full support, new features |
| Maintenance | 12 months | Bug fixes only |
| Deprecated | 6 months | Migration period |
| Retired | - | Removed from service |

---

## 3. Versioning Conventions

### 3.1 Version Number Format

```
MAJOR.MINOR

MAJOR: Breaking changes (incompatible API changes)
MINOR: Backward-compatible additions
```

### 3.2 Breaking Changes

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

---

## 4. Deprecation Policy

### 4.1 Deprecation Process

```
1. Announce deprecation (90 days notice)
2. Add deprecation headers
3. Document migration guide
4. Monitor usage reduction
5. Final warning (30 days)
6. Remove deprecated endpoints
```

### 4.2 Deprecation Headers

```http
HTTP/1.1 200 OK
Deprecation: Sat, 01 Sep 2026 00:00:00 GMT
Sunset: Sun, 01 Mar 2027 00:00:00 GMT
Link: <https://docs.nhdos.iq/api/v2/migration>; rel="successor-version"
```

---

## 5. Version Compatibility Matrix

| Change | v1 | v2 | v3 | Notes |
|--------|----|----|----|-------|
| Patient endpoints | ✓ | ✓ | ✓ | Core API |
| Appointment endpoints | ✓ | ✓ | ✓ | Core API |
| Lab results endpoints | ✓ | ✓ | ✓ | Core API |
| FHIR integration | - | ✓ | ✓ | Added in v2 |
| GraphQL gateway | - | - | ✓ | Added in v3 |

---

## 6. APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/versions` | GET | List all versions |
| `/api/v1/versions/{version}` | GET | Get version details |
| `/api/v1/versions/{version}/deprecate` | POST | Deprecate version |
| `/api/v1/versions/{version}/retire` | POST | Retire version |
| `/api/v1/versions/compare` | GET | Compare versions |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
