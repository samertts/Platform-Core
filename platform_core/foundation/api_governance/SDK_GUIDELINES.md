# SDK GUIDELINES

**NHDOS Platform-Core — SDK Guidelines**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS SDK Guidelines establish standards for creating, maintaining, and distributing client SDKs across all supported programming languages. It ensures consistent developer experience, proper error handling, and security best practices across all platform SDKs.

---

## 2. Architecture Overview

### 2.1 SDK Ecosystem

```
┌─────────────────────────────────────────────────────────┐
│                    SDK Ecosystem                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  OpenAPI    │  │   Code      │  │  Package    │     │
│  │  Specs      │──▶│  Generator  │──▶│  Registry   │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│         │                │                │              │
│         ▼                ▼                ▼              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Python    │  │ TypeScript  │  │    Java     │     │
│  │    SDK      │  │    SDK      │  │    SDK      │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Supported Languages

| Language | Package Manager | Version | Status |
|----------|-----------------|---------|--------|
| Python | PyPI | 3.8+ | Active |
| TypeScript | npm | 16+ | Active |
| Java | Maven | 11+ | Active |
| Go | Go Modules | 1.21+ | Active |
| C# | NuGet | .NET 6+ | Planned |

---

## 3. SDK Structure

### 3.1 Python SDK Structure

```python
from nhdos_sdk import Client
from nhdos_sdk.models import Patient, Appointment
from nhdos_sdk.exceptions import NHDOSException, ValidationError

# Initialize client
client = Client(
    api_key="your-api-key",
    environment="production"
)

# Use models
patient = client.patients.get(patient_id="123")
appointments = client.appointments.list(patient_id="123")

# Handle exceptions
try:
    patient = client.patients.get(patient_id="invalid")
except ValidationError as e:
    print(f"Validation error: {e}")
except NHDOSException as e:
    print(f"API error: {e}")
```

### 3.2 TypeScript SDK Structure

```typescript
import { NHDOSClient } from '@nhdos/sdk';
import { Patient, Appointment } from '@nhdos/sdk/models';

// Initialize client
const client = new NHDOSClient({
  apiKey: 'your-api-key',
  environment: 'production'
});

// Use models
const patient = await client.patients.get('123');
const appointments = await client.appointments.list({ patientId: '123' });

// Handle errors
try {
  const patient = await client.patients.get('invalid');
} catch (error) {
  if (error instanceof ValidationError) {
    console.log(`Validation error: ${error.message}`);
  }
}
```

---

## 4. Error Handling

### 4.1 Error Types

| Error Type | HTTP Code | Description |
|------------|-----------|-------------|
| `ValidationError` | 400 | Invalid request |
| `AuthenticationError` | 401 | Invalid credentials |
| `ForbiddenError` | 403 | Insufficient permissions |
| `NotFoundError` | 404 | Resource not found |
| `ConflictError` | 409 | Resource conflict |
| `RateLimitError` | 429 | Rate limit exceeded |
| `ServerError` | 500 | Internal server error |

### 4.2 Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid patient data",
    "details": [
      {
        "field": "nationalId",
        "message": "Must be 10 digits"
      }
    ],
    "request_id": "req_abc123",
    "timestamp": "2026-06-25T10:00:00Z"
  }
}
```

---

## 5. Authentication

### 5.1 API Key Authentication

```python
client = Client(api_key="nhdos_live_abc123")
```

### 5.2 OAuth 2.0 Authentication

```python
client = Client(
    client_id="your-client-id",
    client_secret="your-client-secret",
    scopes=["patient:read", "patient:write"]
)
```

### 5.3 Token Refresh

```python
# Automatic token refresh
client = Client(
    access_token="your-access-token",
    refresh_token="your-refresh-token",
    auto_refresh=True
)
```

---

## 6. Retry and Resilience

### 6.1 Retry Configuration

```python
from nhdos_sdk import Client
from nhdos_sdk.retry import RetryConfig

retry_config = RetryConfig(
    max_retries=3,
    backoff_factor=0.5,
    retryable_status_codes=[429, 500, 502, 503, 504]
)

client = Client(api_key="your-api-key", retry=retry_config)
```

### 6.2 Circuit Breaker

```python
from nhdos_sdk import Client
from nhdos_sdk.circuit_breaker import CircuitBreaker

circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=30
)

client = Client(api_key="your-api-key", circuit_breaker=circuit_breaker)
```

---

## 7. APIs

### 7.1 SDK Management API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/sdks` | GET | List available SDKs |
| `/api/v1/sdks/{language}` | GET | Get SDK details |
| `/api/v1/sdks/{language}/versions` | GET | List versions |
| `/api/v1/sdks/{language}/changelog` | GET | Get changelog |
| `/api/v1/sdks/{language}/download` | GET | Download SDK |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
