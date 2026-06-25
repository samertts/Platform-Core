# DEVELOPER PORTAL

**NHDOS Platform-Core — Developer Portal**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS Developer Portal provides a centralized interface for API discovery, documentation, testing, and management. It enables internal and external developers to explore APIs, obtain credentials, monitor usage, and access support resources.

---

## 2. Architecture Overview

### 2.1 Portal Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Developer Portal                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │    API      │  │    Docs     │  │   Sandbox   │     │
│  │  Explorer   │  │  Viewer     │  │   Console   │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │              │
│         └────────┬───────┴────────┬───────┘              │
│                  │                │                       │
│         ┌────────▼────────┐ ┌────▼────────────┐         │
│         │   API Gateway   │ │  User           │         │
│         │   (Proxy)       │ │  Management     │         │
│         └─────────────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Portal Features

| Feature | Description | Access |
|---------|-------------|--------|
| API Explorer | Interactive API browser | All users |
| Documentation | OpenAPI-based docs | All users |
| Sandbox | Test API calls | Registered users |
| API Keys | Credential management | Registered users |
| Usage Dashboard | API usage metrics | Registered users |
| Support | Tickets and chat | All users |

---

## 3. Portal Pages

### 3.1 Main Navigation

| Page | Description | URL |
|------|-------------|-----|
| Home | Portal overview | `/portal` |
| APIs | API catalog | `/portal/apis` |
| Documentation | API docs | `/portal/docs` |
| Sandbox | Test console | `/portal/sandbox` |
| Credentials | API key management | `/portal/credentials` |
| Usage | Usage analytics | `/portal/usage` |
| Support | Help center | `/portal/support` |

### 3.2 API Catalog

```yaml
apis:
  - name: "Patient Service"
    version: "1.0"
    description: "Patient management endpoints"
    category: "Healthcare"
    auth_required: true
    rate_limit: "1000/hour"
    
  - name: "Appointment Service"
    version: "1.0"
    description: "Appointment scheduling"
    category: "Healthcare"
    auth_required: true
    rate_limit: "500/hour"
    
  - name: "Lab Results Service"
    version: "1.0"
    description: "Laboratory results access"
    category: "Healthcare"
    auth_required: true
    rate_limit: "2000/hour"
```

---

## 4. Credential Management

### 4.1 API Key Types

| Type | Scope | Rate Limit | Usage |
|------|-------|------------|-------|
| `sandbox` | Test only | 100/hour | Development |
| `development` | Dev environment | 1000/hour | Integration |
| `production` | Live environment | Custom | Production |

### 4.2 Key Management Flow

```
1. Register for developer account
2. Verify email address
3. Accept terms of service
4. Create application
5. Request API key
6. Key approval (for production)
7. Start integrating
```

### 4.3 Key Management API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/portal/api/keys` | GET | List API keys |
| `/portal/api/keys` | POST | Create API key |
| `/portal/api/keys/{id}` | DELETE | Revoke API key |
| `/portal/api/keys/{id}/rotate` | POST | Rotate API key |

---

## 5. Documentation

### 5.1 Documentation Structure

```
portal/docs/
├── getting-started/
│   ├── quickstart.md
│   ├── authentication.md
│   └── rate-limits.md
├── guides/
│   ├── patient-management.md
│   ├── appointment-scheduling.md
│   └── lab-results.md
├── sdks/
│   ├── python.md
│   ├── typescript.md
│   └── java.md
└── api-reference/
    ├── patient-service/
    ├── appointment-service/
    └── lab-service/
```

### 5.2 Interactive Documentation

```yaml
# Swagger UI Integration
swagger_ui:
  enabled: true
  path: "/portal/docs/api"
  try_it_out: true
  persist_authorization: true

# Redoc Integration
redoc:
  enabled: true
  path: "/portal/docs/redoc"
```

---

## 6. Sandbox

### 6.1 Sandbox Environment

| Feature | Description |
|---------|-------------|
| Mock Data | Synthetic patient data |
| Rate Limits | 100 requests/hour |
| Authentication | Sandbox API keys |
| Persistence | No data persistence |
| Cleanup | Auto-reset every 24h |

### 6.2 Sandbox Usage

```python
# Connect to sandbox
from nhdos_sdk import Client

client = Client(
    api_key="nhdos_sandbox_abc123",
    environment="sandbox"
)

# Make test calls
patient = client.patients.create(
    national_id="1234567890",
    given_name="Test",
    family_name="Patient"
)
```

---

## 7. APIs

### 7.1 Portal Management API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/portal/api/catalog` | GET | Get API catalog |
| `/portal/api/usage` | GET | Get usage metrics |
| `/portal/api/tickets` | GET | List support tickets |
| `/portal/api/tickets` | POST | Create support ticket |
| `/portal/api/feedback` | POST | Submit feedback |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
