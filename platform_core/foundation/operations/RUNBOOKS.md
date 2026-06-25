# RUNBOOKS

**NHDOS Platform-Core — Runbooks**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS Runbooks provide step-by-step procedures for common operational tasks, incident response, and maintenance activities. They ensure consistent execution and reduce mean time to recovery (MTTR).

---

## 2. Architecture Overview

### 2.1 Runbook System

```
┌─────────────────────────────────────────────────────────┐
│                    Runbook System                         │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Runbook   │  │  Execution  │  │  Audit      │     │
│  │   Store     │──▶│  Engine     │──▶│  Trail      │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │              │
│         └────────┬───────┴────────┬───────┘              │
│                  │                │                       │
│         ┌────────▼────────┐ ┌────▼────────────┐         │
│         │  Runbook DB     │ │  Execution Log  │         │
│         │  (PostgreSQL)   │ │  (Elasticsearch)│         │
│         └─────────────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Runbook Categories

### 3.1 Runbook Types

| Category | Description | Examples |
|----------|-------------|----------|
| Incident Response | Handle production issues | Service down, data corruption |
| Maintenance | Scheduled operations | Database backup, certificate renewal |
| Deployment | Release procedures | Blue-green deploy, rollback |
| Scaling | Capacity operations | Horizontal scaling, database scaling |
| Recovery | Disaster recovery | Failover, restore |

### 3.2 Runbook Template

```yaml
runbook:
  id: "rb-001"
  name: "Service Down Response"
  category: "incident-response"
  severity: "P1"
  
  trigger:
    - alert: "ServiceHealthCritical"
    - metric: "availability < 99.9%"
    
  steps:
    - id: 1
      name: "Acknowledge Alert"
      action: "acknowledge_alert"
      command: "nhdos-cli alert acknowledge {{alert_id}}"
      
    - id: 2
      name: "Check Service Status"
      action: "check_status"
      command: "nhdos-cli service status {{service_name}}"
      
    - id: 3
      name: "Check Recent Deployments"
      action: "check_deployments"
      command: "nhdos-cli deployments list --recent 1h"
      
    - id: 4
      name: "Check Service Logs"
      action: "check_logs"
      command: "nhdos-cli logs {{service_name}} --tail 100"
      
    - id: 5
      name: "Restart Service"
      action: "restart"
      command: "nhdos-cli service restart {{service_name}}"
      condition: "if steps 2-4 show no issues"
      
  rollback:
    steps:
      - name: "Restore Previous Version"
        command: "nhdos-cli deployment rollback {{deployment_id}}"
```

---

## 4. Runbook Examples

### 4.1 Database Failover Runbook

```yaml
runbook:
  id: "rb-db-001"
  name: "Database Failover"
  category: "incident-response"
  severity: "P1"
  
  steps:
    - name: "Verify Primary Down"
      command: "pg_isready -h primary.db.nhdos.iq"
      
    - name: "Check Replication Lag"
      command: "psql -h replica.db.nhdos.iq -c 'SELECT lag FROM pg_stat_replication'"
      
    - name: "Promote Replica"
      command: "pg_ctl promote -D /var/lib/postgresql/data"
      
    - name: "Update DNS"
      command: "nhdos-cli dns update db.nhdos.iq --ip replica-ip"
      
    - name: "Verify Connectivity"
      command: "psql -h db.nhdos.iq -c 'SELECT 1'"
      
    - name: "Notify Team"
      command: "nhdos-cli notify --channel sre --message 'Database failover completed'"
```

### 4.2 Certificate Renewal Runbook

```yaml
runbook:
  id: "rb-cert-001"
  name: "TLS Certificate Renewal"
  category: "maintenance"
  
  steps:
    - name: "Check Certificate Expiry"
      command: "openssl s_client -connect api.nhdos.iq:443 | openssl x509 -noout -dates"
      
    - name: "Request New Certificate"
      command: "nhdos-cli cert request --domain api.nhdos.iq"
      
    - name: "Verify Certificate"
      command: "openssl verify -CAfile ca.crt new.crt"
      
    - name: "Update Load Balancer"
      command: "nhdos-cli lb update-cert --cert new.crt --key new.key"
      
    - name: "Verify Deployment"
      command: "curl -I https://api.nhdos.iq"
```

---

## 5. Runbook Management

### 5.1 Runbook Lifecycle

| Phase | Description | Responsible |
|-------|-------------|-------------|
| Draft | Initial creation | Author |
| Review | Peer review | SRE Team |
| Approved | Ready for use | SRE Lead |
| Active | In production | Operations |
| Deprecated | No longer used | SRE Lead |

### 5.2 Runbook Testing

```python
class RunbookTester:
    def test_runbook(self, runbook_id: str) -> TestResult:
        runbook = self.get_runbook(runbook_id)
        
        results = []
        for step in runbook.steps:
            result = self.test_step(step)
            results.append(result)
            
            if not result.success and step.critical:
                break
        
        return TestResult(
            runbook_id=runbook_id,
            steps_passed=sum(1 for r in results if r.success),
            steps_total=len(results),
            success=all(r.success for r in results)
        )
```

---

## 6. APIs

### 6.1 Runbook Management API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/runbooks` | GET | List runbooks |
| `/api/v1/runbooks` | POST | Create runbook |
| `/api/v1/runbooks/{id}` | GET | Get runbook |
| `/api/v1/runbooks/{id}` | PUT | Update runbook |
| `/api/v1/runbooks/{id}/execute` | POST | Execute runbook |
| `/api/v1/runbooks/{id}/test` | POST | Test runbook |
| `/api/v1/runbooks/{id}/history` | GET | Execution history |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
