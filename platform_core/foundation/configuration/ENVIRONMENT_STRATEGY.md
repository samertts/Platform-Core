# ENVIRONMENT STRATEGY

**NHDOS Platform-Core — Environment Profiles**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS Environment Strategy defines standardized deployment environments, their purposes, configurations, and promotion paths. It ensures consistent, reproducible deployments across development, testing, staging, and production environments while maintaining appropriate isolation and security boundaries.

---

## 2. Architecture Overview

### 2.1 Environment Topology

```
┌─────────────────────────────────────────────────────────────┐
│                    Environment Hierarchy                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │     Dev      │───▶│   Staging    │───▶│  Production  │  │
│  │   (Local)    │    │  (Shared)    │    │  (Isolated)  │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                  │                   │             │
│         ▼                  ▼                   ▼             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Testing    │    │   Canary     │    │   DR Site    │  │
│  │  (Automated) │    │  (Shadow)    │    │  (Standby)   │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Environment Matrix

| Environment | Purpose | Isolation | Data | Access |
|-------------|---------|-----------|------|--------|
| `development` | Local development | Namespace | Synthetic | Developers |
| `testing` | Automated tests | Namespace | Synthetic | CI/CD |
| `staging` | Pre-production | Cluster | Anonymized | QA, SRE |
| `canary` | Production subset | Production | Production (subset) | SRE |
| `production` | Live system | Cluster | Production | Operators |
| `disaster-recovery` | Failover | Cluster | Production (replica) | SRE |

---

## 3. Environment Definitions

### 3.1 Development Environment

```yaml
environment:
  name: development
  purpose: "Local development and unit testing"
  cluster: "dev-cluster-01"
  namespace: "nhdos-dev-{developer}"
  
  resources:
    cpu: "2 cores"
    memory: "4 GB"
    storage: "50 GB"
    
  services:
    patient-service:
      replicas: 1
      resources:
        cpu: "500m"
        memory: "512Mi"
    api-gateway:
      replicas: 1
      resources:
        cpu: "250m"
        memory: "256Mi"
        
  database:
    type: "PostgreSQL"
    version: "15"
    single_node: true
    backup: "none"
    
  features:
    debug_mode: true
    verbose_logging: true
    mock_external_services: true
```

### 3.2 Staging Environment

```yaml
environment:
  name: staging
  purpose: "Integration testing and QA validation"
  cluster: "staging-cluster-01"
  namespace: "nhdos-staging"
  
  resources:
    cpu: "16 cores"
    memory: "64 GB"
    storage: "500 GB"
    
  services:
    patient-service:
      replicas: 2
      resources:
        cpu: "1 core"
        memory: "1Gi"
    api-gateway:
      replicas: 2
      resources:
        cpu: "500m"
        memory: "512Mi"
        
  database:
    type: "PostgreSQL"
    version: "15"
    replicas: 2
    backup: "daily"
    
  features:
    debug_mode: false
    verbose_logging: false
    mock_external_services: false
    audit_logging: true
```

### 3.3 Production Environment

```yaml
environment:
  name: production
  purpose: "Live system serving real users"
  cluster: "prod-cluster-{region}"
  namespace: "nhdos-prod"
  
  resources:
    cpu: "64 cores"
    memory: "256 GB"
    storage: "2 TB"
    
  services:
    patient-service:
      replicas: 6
      resources:
        cpu: "2 cores"
        memory: "4Gi"
      autoscaling:
        min: 3
        max: 12
        target_cpu: 70
    api-gateway:
      replicas: 4
      resources:
        cpu: "1 core"
        memory: "2Gi"
      autoscaling:
        min: 2
        max: 8
        target_cpu: 60
        
  database:
    type: "PostgreSQL"
    version: "15"
    replicas: 3
    backup: "continuous"
    encryption: "AES-256"
    
  features:
    debug_mode: false
    verbose_logging: false
    audit_logging: true
    encryption_at_rest: true
    encryption_in_transit: true
```

---

## 4. Environment Promotion

### 4.1 Promotion Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Developer   │───▶│    CI       │───▶│   Staging   │───▶│  Production │
│    Local     │    │  Pipeline   │    │   Deploy    │    │   Deploy    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                 │                  │                   │
       ▼                 ▼                  ▼                   ▼
  Unit Tests        Build/Test        Integration         Canary/Blue-Green
  Lint/Format       Artifact          E2E Tests           Rollout
                    Generation        Performance         Monitoring
```

### 4.2 Promotion Criteria

| Stage | Criteria | Approval |
|-------|----------|----------|
| Dev → Testing | Unit tests pass, lint clean | Automated |
| Testing → Staging | Integration tests pass, security scan | Automated |
| Staging → Canary | E2E tests pass, performance baseline | Manual |
| Canary → Production | Canary metrics acceptable | Manual |

---

## 5. Environment Isolation

### 5.1 Network Isolation

| Environment | Network | Access |
|-------------|---------|--------|
| Development | `dev-network` | VPN only |
| Testing | `test-network` | VPN only |
| Staging | `staging-network` | VPN + limited public |
| Production | `prod-network` | Public + VPN |

### 5.2 Data Isolation

| Environment | Data Strategy | PII Handling |
|-------------|---------------|--------------|
| Development | Synthetic data | No real PII |
| Testing | Synthetic data | No real PII |
| Staging | Anonymized production | Anonymized |
| Production | Real production data | Full encryption |

---

## 6. APIs

### 6.1 Environment Management API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/environments` | GET | List environments |
| `/api/v1/environments/{name}` | GET | Get environment details |
| `/api/v1/environments/{name}/status` | GET | Get environment health |
| `/api/v1/environments/{name}/promote` | POST | Promote to environment |
| `/api/v1/environments/{name}/rollback` | POST | Rollback environment |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
