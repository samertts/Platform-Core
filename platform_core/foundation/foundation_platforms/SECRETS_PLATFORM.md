# SECRETS PLATFORM

**NHDOS Platform-Core — Foundation Platform 26: Secrets Platform**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The Secrets Platform provides secure secrets management for NHDOS, including secrets, certificates, PKI, vault, key rotation, and HSM readiness across 18 governorates and 4,800 healthcare facilities.

---

## 2. Architecture

### 2.1 Core Principles

| Principle | Description |
|-----------|-------------|
| Zero Trust | Never trust, always verify |
| Least Privilege | Minimum required access |
| Rotation | Regular key rotation |
| Audit | Full audit trail |
| HSM | Hardware security module ready |

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECRETS PLATFORM                               │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Vault       │  │   PKI        │  │   Certificate│          │
│  │  Manager     │──▶│   Authority  │──▶│   Manager    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │  Key         │  │   HSM        │  │   Audit      │          │
│  │  Rotation    │  │   Integration│  │   Trail      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Secrets Management

### 3.1 Secret Types

| Type | Description | Rotation |
|------|-------------|----------|
| API Key | API authentication keys | 90 days |
| Database Password | Database credentials | 30 days |
| TLS Certificate | TLS certificates | 365 days |
| Encryption Key | Data encryption keys | 90 days |
| Service Account | Service account credentials | 60 days |

### 3.2 Secret Storage

| Storage | Description | Use Case |
|---------|-------------|----------|
| Vault | Central secrets store | All secrets |
| HSM | Hardware security module | Critical secrets |
| Local Cache | Edge site cache | Offline access |

---

## 4. Certificate Management

### 4.1 Certificate Types

| Type | Purpose | Validity |
|------|---------|----------|
| Root CA | Root certificate authority | 10 years |
| Intermediate CA | Intermediate CA | 5 years |
| Server Certificate | TLS server certificates | 1 year |
| Client Certificate | Client authentication | 1 year |
| Code Signing | Code signing certificates | 2 years |

### 4.2 Certificate Lifecycle

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Request │────▶│  Issue   │────▶│  Active  │────▶│  Renew   │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
                                              │
                                              ▼
                                        ┌──────────┐
                                        │  Revoke  │
                                        └──────────┘
```

---

## 5. Key Rotation

### 5.1 Rotation Schedule

| Key Type | Frequency | Method |
|----------|-----------|--------|
| Database Password | 30 days | Automatic |
| API Key | 90 days | Automatic |
| Encryption Key | 90 days | Automatic |
| TLS Certificate | 365 days | Semi-automatic |

### 5.2 Rotation Process

```
1. Generate new key
2. Update key in vault
3. Deploy to services
4. Verify new key works
5. Revoke old key
6. Audit trail
```

---

## 6. HSM Readiness

### 6.1 HSM Integration

| Feature | Description |
|---------|-------------|
| Key Storage | Keys stored in HSM |
| Key Generation | Keys generated in HSM |
| Key Usage | Keys used in HSM |
| FIPS 140-2 | FIPS 140-2 Level 3 ready |

### 6.2 HSM Use Cases

| Use Case | Description |
|----------|-------------|
| Root CA | Root certificate private key |
| Encryption Keys | Data encryption master keys |
| Signing Keys | Code signing private keys |
| Authentication | Authentication keys |

---

## 7. Secrets APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/secrets | GET | List secrets |
| /api/v1/secrets/{secret} | GET | Get secret |
| /api/v1/secrets/{secret} | PUT | Update secret |
| /api/v1/secrets/{secret}/rotate | POST | Rotate secret |
| /api/v1/secrets/certificates | GET | List certificates |
| /api/v1/secrets/certificates/{cert} | GET | Get certificate |
| /api/v1/secrets/certificates/{cert}/revoke | POST | Revoke certificate |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
