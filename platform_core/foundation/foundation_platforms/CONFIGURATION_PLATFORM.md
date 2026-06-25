# CONFIGURATION PLATFORM

**NHDOS Platform-Core — Foundation Platform 7: Centralized Configuration**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The Configuration Platform provides centralized configuration management for NHDOS, featuring hierarchical configuration, dynamic reload, environment profiles, validation, configuration registry, and central configuration API across 18 governorates and 4,800 healthcare facilities.

---

## 2. Architecture

### 2.1 Core Principles

| Principle | Description |
|-----------|-------------|
| Centralized | Single source of truth for configuration |
| Hierarchical | Environment → Region → Facility → Service |
| Dynamic | Runtime configuration changes |
| Validated | All configuration validated before deployment |
| Versioned | Configuration changes tracked |
| Offline Capable | Local configuration cache |

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONFIGURATION PLATFORM                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Central     │  │   Hierarchical│  │   Dynamic    │          │
│  │  Config Store│──▶│   Resolver   │──▶│   Reload     │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │  Config      │  │   Environment│  │   Validation │          │
│  │  Registry    │  │   Profiles   │  │   Engine     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Hierarchical Configuration

### 3.1 Configuration Levels

| Level | Scope | Priority | Example |
|-------|-------|----------|---------|
| Global | All environments | 1 (lowest) | Platform defaults |
| Environment | Dev/Staging/Prod | 2 | Environment-specific |
| Region | Governorate | 3 | Regional settings |
| Facility | Healthcare facility | 4 | Facility-specific |
| Service | Microservice | 5 (highest) | Service-specific |

### 3.2 Configuration Resolution

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Global     │────▶│  Environment │────▶│   Region     │
│   Config     │     │   Config     │     │   Config     │
└──────────────┘     └──────────────┘     └──────────────┘
                                               │
                                               ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Service    │◀────│   Facility   │◀────│   Override   │
│   Config     │     │   Config     │     │   Config     │
└──────────────┘     └──────────────┘     └──────────────┘
```

---

## 4. Environment Profiles

### 4.1 Environments

| Environment | Purpose | Data |
|-------------|---------|------|
| Development | Development testing | Synthetic |
| Staging | Pre-production testing | Anonymized |
| Production | Live environment | Real data |
| DR | Disaster recovery | Replica |

### 4.2 Environment Configuration

| Setting | Development | Staging | Production |
|---------|-------------|---------|------------|
| Debug Mode | Enabled | Disabled | Disabled |
| Logging Level | DEBUG | INFO | WARN |
| Cache TTL | 60s | 300s | 3600s |
| Rate Limit | 1000/min | 5000/min | 10000/min |
| Encryption | Optional | Required | Required + HSM |

---

## 5. Configuration Validation

### 5.1 Validation Rules

| Rule | Description | Severity |
|------|-------------|----------|
| Type Check | Configuration type matches schema | Error |
| Range Check | Values within defined ranges | Error |
| Format Check | Values match defined formats | Error |
| Dependency Check | Dependencies exist | Error |
| Security Check | No secrets in plain text | Error |

### 5.2 Schema Validation

```yaml
config_schema:
  database:
    host:
      type: string
      required: true
      format: hostname
    port:
      type: integer
      required: true
      min: 1
      max: 65535
    ssl:
      type: boolean
      required: false
      default: true
```

---

## 6. Dynamic Reload

### 6.1 Reload Triggers

| Trigger | Description | Downtime |
|---------|-------------|----------|
| Config Change | Configuration updated | None (hot reload) |
| Feature Flag | Feature toggled | None (hot reload) |
| Environment Change | Environment switch | Restart required |
| Schema Change | Configuration schema updated | Restart required |

### 6.2 Reload Strategy

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Hot Reload | No restart required | Feature flags |
| Rolling Reload | Gradual restart | Database config |
| Full Restart | Complete restart | Schema changes |

---

## 7. APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/config/{service} | GET | Get service configuration |
| /api/v1/config/{service} | PUT | Update service configuration |
| /api/v1/config/{service}/validate | POST | Validate configuration |
| /api/v1/config/{service}/reload | POST | Trigger configuration reload |
| /api/v1/config/registry | GET | List configuration registry |
| /api/v1/config/history | GET | Get configuration history |

---

## 8. Offline Support

| Capability | Implementation |
|------------|----------------|
| Local Cache | Configuration cached locally |
| Fallback | Use last known good config |
| Sync Protocol | Delta sync on reconnect |
| Conflict Resolution | Latest version wins |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
