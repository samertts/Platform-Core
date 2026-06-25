# CONFIGURATION PLATFORM

**NHDOS Platform-Core — Centralized Configuration Management**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS Configuration Platform provides centralized, hierarchical configuration management for all platform services. It supports environment-aware configuration, dynamic updates, encrypted secrets, and audit logging to ensure consistent and secure configuration across all deployment targets.

---

## 2. Architecture Overview

### 2.1 Configuration Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│                   Configuration Platform                 │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Global    │  │ Environment │  │   Service   │     │
│  │   Config    │  │   Config    │  │   Config    │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │              │
│         └────────┬───────┴────────┬───────┘              │
│                  │                │                       │
│         ┌────────▼────────┐ ┌────▼────────────┐         │
│         │  Secret Store   │ │ Feature Flags   │         │
│         │  (Encrypted)    │ │ (Dynamic)       │         │
│         └─────────────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Configuration Sources

| Source | Priority | Scope | Description |
|--------|----------|-------|-------------|
| Environment Variables | 1 (Highest) | Runtime | OS-level overrides |
| Secrets Manager | 2 | Service | Encrypted secrets |
| Service Config | 3 | Service | Service-specific settings |
| Environment Profile | 4 | Environment | Per-environment defaults |
| Global Config | 5 (Lowest) | Platform | Platform-wide defaults |

---

## 3. Configuration Model

### 3.1 Configuration Schema

```json
{
  "service": "patient-service",
  "version": "1.0.0",
  "environment": "production",
  "config": {
    "database": {
      "host": "${DB_HOST}",
      "port": 5432,
      "name": "patient_db",
      "pool_size": 20,
      "ssl_mode": "require"
    },
    "cache": {
      "redis_url": "${REDIS_URL}",
      "ttl_seconds": 300
    },
    "logging": {
      "level": "INFO",
      "format": "json"
    }
  },
  "secrets": {
    "database_password": "${vault:secret/data/db/password}",
    "api_key": "${vault:secret/data/api/key}"
  }
}
```

### 3.2 Configuration Types

| Type | Description | Validation |
|------|-------------|------------|
| `string` | Text values | Regex pattern |
| `integer` | Numeric values | Min/max range |
| `boolean` | True/false | Strict boolean |
| `enum` | Allowed values | Value list |
| `json` | Structured data | JSON Schema |
| `encrypted` | Sensitive data | Vault reference |
| `reference` | Cross-service ref | Service discovery |

---

## 4. Configuration Management

### 4.1 Configuration Operations

| Operation | Description | Audit Required |
|-----------|-------------|----------------|
| `create` | New configuration | Yes |
| `update` | Modify existing | Yes |
| `delete` | Remove config | Yes |
| `promote` | Move between envs | Yes |
| `rollback` | Revert changes | Yes |

### 4.2 Change Management Process

```
1. Developer submits config change request
2. Automated validation (schema, dependencies)
3. Peer review (for production changes)
4. Staged deployment (staging → canary → production)
5. Post-deployment verification
6. Audit log entry
```

---

## 5. Configuration Storage

### 5.1 Storage Architecture

| Layer | Technology | Purpose |
|-------|------------|---------|
| Configuration Service | Custom API | CRUD operations |
| Schema Validation | JSON Schema | Input validation |
| Encrypted Store | Vault | Secret management |
| Cache Layer | Redis | Performance |
| Audit Store | PostgreSQL | Change history |

### 5.2 Configuration Caching

```python
class ConfigurationCache:
    def get(self, service: str, key: str) -> ConfigValue:
        # 1. Check in-memory cache (TTL: 30s)
        # 2. Check Redis cache (TTL: 5min)
        # 3. Fetch from Configuration Service
        # 4. Update caches
        pass

    def invalidate(self, service: str) -> None:
        # Invalidate all caches for service
        pass
```

---

## 6. APIs

### 6.1 Configuration Service API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/config/{service}` | GET | Get service config |
| `/api/v1/config/{service}` | PUT | Update service config |
| `/api/v1/config/{service}/validate` | POST | Validate config |
| `/api/v1/config/{service}/history` | GET | Get change history |
| `/api/v1/config/{service}/promote` | POST | Promote to environment |

### 6.2 Configuration Client SDK

```python
from platform_config import ConfigurationClient

client = ConfigurationClient(environment="production")

# Get configuration
db_config = client.get("patient-service", "database")

# Get with default
cache_ttl = client.get("patient-service", "cache.ttl", default=300)

# Watch for changes
client.watch("patient-service", "database", callback=on_config_change)
```

---

## 7. Implementation Details

### 7.1 Configuration File Structure

```
config/
├── global/
│   ├── platform.yaml
│   ├── security.yaml
│   └── monitoring.yaml
├── environments/
│   ├── development.yaml
│   ├── staging.yaml
│   ├── production.yaml
│   └── disaster-recovery.yaml
├── services/
│   ├── patient-service/
│   │   ├── base.yaml
│   │   ├── development.yaml
│   │   ├── staging.yaml
│   │   └── production.yaml
│   └── ...other services
└── secrets/
    └── vault/
        └── secrets.yaml
```

### 7.2 Configuration Validation Rules

```yaml
validation_rules:
  required_fields:
    - database.host
    - database.port
    - logging.level
  type_constraints:
    database.port: integer
    database.pool_size: integer
    cache.ttl_seconds: integer
  range_constraints:
    database.port: [1, 65535]
    database.pool_size: [1, 100]
    cache.ttl_seconds: [0, 86400]
  secret_references:
    pattern: "^\\$\\{vault:.*\\}$"
    allowed_paths:
      - secret/data/db/*
      - secret/data/api/*
```

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
