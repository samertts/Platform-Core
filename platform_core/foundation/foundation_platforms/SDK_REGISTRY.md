# SDK REGISTRY

**NHDOS Platform-Core — Foundation Platform 13: SDK Registry**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The SDK Registry provides a centralized catalog of all official NHDOS SDKs, their versions, compatibility information, and lifecycle status for developers across 18 governorates.

---

## 2. Architecture

### 2.1 Core Principles

| Principle | Description |
|-----------|-------------|
| Centralized | Single source of truth for SDKs |
| Discoverable | Easy SDK discovery |
| Versioned | Full version history |
| Compatible | API compatibility tracked |
| Maintained | Active maintenance status |

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SDK REGISTRY                                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  SDK         │  │   Search     │  │   Version    │          │
│  │  Catalog     │──▶│   Engine     │──▶│   Manager    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │  Compatibility│  │   Lifecycle  │  │   Analytics  │          │
│  │  Matrix      │  │   Manager    │  │   Dashboard  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. SDK Catalog

### 3.1 Registry Fields

| Field | Description |
|-------|-------------|
| name | SDK name |
| language | Programming language |
| package | Package manager identifier |
| version | Current version |
| status | Active/Deprecated/Retired |
| apiCompatibility | Supported API versions |
| documentation | Documentation URL |
| repository | Source repository URL |
| maintainers | SDK maintainers |
| lastUpdated | Last update timestamp |

### 3.2 SDK Entries

| SDK | Language | Package | Status | API v1 | API v2 | API v3 |
|-----|----------|---------|--------|--------|--------|--------|
| nhdos-sdk-python | Python | pypi:nhdos-sdk | Active | ✓ | ✓ | ✓ |
| nhdos-sdk-typescript | TypeScript | npm:@nhdos/sdk | Active | ✓ | ✓ | ✓ |
| nhdos-sdk-flutter | Flutter | pub:nhdos_sdk | Active | ✓ | ✓ | ✓ |
| nhdos-sdk-kotlin | Kotlin | maven:nhdos-sdk | Active | ✓ | ✓ | ✓ |
| nhdos-sdk-swift | Swift | spm:NHDOSsdk | Active | ✓ | ✓ | ✓ |
| nhdos-sdk-java | Java | maven:nhdos-sdk-java | Active | ✓ | ✓ | ✓ |
| nhdos-sdk-dotnet | .NET | nuget:NHDOS.SDK | Active | ✓ | ✓ | ✓ |
| nhdos-sdk-go | Go | github:nhdos/sdk-go | Active | ✓ | ✓ | ✓ |
| nhdos-sdk-rust | Rust | cargo:nhdos-sdk | Active | - | ✓ | ✓ |

---

## 4. Lifecycle Management

### 4.1 Lifecycle States

| State | Description | Support Level |
|-------|-------------|---------------|
| Active | Fully supported | Full |
| Maintenance | Bug fixes only | Limited |
| Deprecated | Migration period | Critical fixes |
| Retired | No longer supported | None |

### 4.2 Version Lifecycle

| Phase | Duration | Action |
|-------|----------|--------|
| Alpha | 1 month | Testing |
| Beta | 2 months | Feedback |
| Stable | 24 months | Full support |
| Maintenance | 12 months | Bug fixes |
| Deprecated | 6 months | Migration |
| Retired | - | Removed |

---

## 5. APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/sdk-registry | GET | List all SDKs |
| /api/v1/sdk-registry/{sdk} | GET | Get SDK details |
| /api/v1/sdk-registry/{sdk}/versions | GET | List versions |
| /api/v1/sdk-registry/{sdk}/versions/{version} | GET | Get version |
| /api/v1/sdk-registry/{sdk}/search | GET | Search SDK |
| /api/v1/sdk-registry/{sdk}/analytics | GET | Get usage analytics |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
