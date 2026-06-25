# SERVICE REGISTRY

**NHDOS Platform-Core — Service Registry**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS Service Registry provides service discovery, health monitoring, and load balancing for all platform microservices. It enables dynamic service registration, health checking, and intelligent routing for service-to-service communication.

---

## 2. Architecture Overview

### 2.1 Service Registry Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Service Registry                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Service    │  │   Health    │  │   Load      │     │
│  │  Discovery  │──▶│   Checker   │──▶│  Balancer   │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │              │
│         └────────┬───────┴────────┬───────┘              │
│                  │                │                       │
│         ┌────────▼────────┐ ┌────▼────────────┐         │
│         │  Service Store  │ │  Health Store   │         │
│         │  (Consul)       │ │  (Redis)        │         │
│         └─────────────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Service Types

| Type | Description | Discovery | Health Check |
|------|-------------|-----------|--------------|
| `http` | REST services | DNS/HTTP | HTTP endpoint |
| `grpc` | gRPC services | DNS/gRPC | gRPC health |
| `database` | Data stores | Connection | Connection test |
| `cache` | Cache stores | Connection | Connection test |
| `queue` | Message queues | Connection | Connection test |

---

## 3. Service Model

### 3.1 Service Registration

```json
{
  "service_id": "patient-service-001",
  "service_name": "patient-service",
  "version": "1.2.3",
  "instance": "patient-service-001.prod.nhdos.iq",
  "address": "10.0.1.100",
  "port": 8080,
  "protocol": "http",
  "tags": ["healthcare", "core", "v1"],
  "metadata": {
    "environment": "production",
    "region": "baghdad",
    "cluster": "prod-cluster-01"
  },
  "health_check": {
    "type": "http",
    "path": "/health",
    "interval": "10s",
    "timeout": "5s"
  }
}
```

### 3.2 Service Health States

| State | Description | Action |
|-------|-------------|--------|
| `passing` | Healthy | Route traffic |
| `warning` | Degraded | Reduce traffic |
| `critical` | Unhealthy | Stop routing |
| `unknown` | Unknown | Investigate |

---

## 4. Service Discovery

### 4.1 Discovery Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| DNS | Service DNS lookup | Simple discovery |
| HTTP | HTTP API query | Complex queries |
| Watch | Event-based updates | Real-time changes |

### 4.2 Discovery Implementation

```python
class ServiceDiscovery:
    def discover(self, service_name: str) -> List[ServiceInstance]:
        # 1. Query service registry
        instances = self.registry.query(
            service_name=service_name,
            passing_only=True
        )
        
        # 2. Filter by health
        healthy = [i for i in instances if i.health == "passing"]
        
        # 3. Apply load balancing
        selected = self.load_balancer.select(healthy)
        
        return selected
    
    def watch(self, service_name: str, callback: Callable) -> None:
        # Watch for service changes
        self.registry.watch(service_name, callback)
```

---

## 5. Health Checking

### 5.1 Health Check Types

| Type | Description | Implementation |
|------|-------------|----------------|
| HTTP | HTTP GET request | Check `/health` endpoint |
| gRPC | gRPC health check | Use gRPC health protocol |
| TCP | TCP connection | Check port connectivity |
| Script | Custom script | Run health check script |

### 5.2 Health Check Configuration

```yaml
health_checks:
  - id: patient-service-health
    name: Patient Service Health
    type: http
    target: "http://patient-service:8080/health"
    interval: 10s
    timeout: 5s
    retries: 3
    
  - id: database-health
    name: Database Health
    type: tcp
    target: "postgres:5432"
    interval: 30s
    timeout: 10s
    retries: 3
```

---

## 6. APIs

### 6.1 Service Registry API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/services` | GET | List services |
| `/api/v1/services/{name}` | GET | Get service details |
| `/api/v1/services/{name}/instances` | GET | List instances |
| `/api/v1/services/{name}/health` | GET | Get service health |
| `/api/v1/services/{name}/register` | POST | Register instance |
| `/api/v1/services/{name}/deregister` | DELETE | Deregister instance |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
