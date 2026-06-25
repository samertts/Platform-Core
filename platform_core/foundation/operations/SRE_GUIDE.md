# SRE GUIDE

**NHDOS Platform-Core — SRE Guide**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS SRE Guide provides operational guidelines for Site Reliability Engineers managing the platform. It covers service level objectives, incident management, toil reduction, and best practices for maintaining high availability.

---

## 2. Architecture Overview

### 2.1 SRE Operations Model

```
┌─────────────────────────────────────────────────────────┐
│                    SRE Operations                         │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │    SLO      │  │  Incident   │  │   Toil      │     │
│  │  Management │──▶│  Response   │──▶│  Reduction  │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │              │
│         └────────┬───────┴────────┬───────┘              │
│                  │                │                       │
│         ┌────────▼────────┐ ┌────▼────────────┐         │
│         │  Error Budget   │ │  Runbook        │         │
│         │  Tracking       │ │  Library        │         │
│         └─────────────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Service Level Objectives

### 3.1 SLO Definitions

| Service | SLI | SLO Target | Error Budget |
|---------|-----|------------|--------------|
| Patient Service | Availability | 99.95% | 21.6 min/month |
| Patient Service | Latency (p99) | < 200ms | - |
| API Gateway | Availability | 99.99% | 4.3 min/month |
| API Gateway | Throughput | 10K RPS | - |
| Database | Availability | 99.99% | 4.3 min/month |
| Database | Latency (p95) | < 50ms | - |

### 3.2 Error Budget Policy

```yaml
error_budget_policy:
  burn_rate_thresholds:
    - name: "critical"
      burn_rate: 14.4
      window: 1 hour
      action: "page_oncall"
      
    - name: "warning"
      burn_rate: 6
      window: 6 hours
      action: "notify_channel"
      
    - name: "ok"
      burn_rate: 1
      window: 3 days
      action: "log_only"
      
  budget_exhaustion:
    - threshold: 50%
      action: "review_deployments"
    - threshold: 75%
      action: "freeze_non_critical"
    - threshold: 100%
      action: "stop_all_changes"
```

---

## 4. Incident Management

### 4.1 Severity Levels

| Severity | Description | Response Time | Resolution Time |
|----------|-------------|---------------|-----------------|
| P1 | Complete outage | 5 minutes | 1 hour |
| P2 | Major degradation | 15 minutes | 4 hours |
| P3 | Minor degradation | 1 hour | 24 hours |
| P4 | Cosmetic issue | 4 hours | 1 week |

### 4.2 Incident Response Flow

```
1. Detection
   - Automated alerting
   - User reports
   - Monitoring anomalies

2. Triage
   - Assess impact
   - Determine severity
   - Page appropriate responders

3. Response
   - Acknowledge incident
   - Begin investigation
   - Communicate status

4. Resolution
   - Implement fix
   - Verify resolution
   - Monitor stability

5. Post-mortem
   - Timeline review
   - Root cause analysis
   - Action items
```

---

## 5. Toil Reduction

### 5.1 Toil Definition

| Category | Description | Target |
|----------|-------------|--------|
| Manual operations | Repetitive tasks | Automate |
| Troubleshooting | Common issues | Self-heal |
| Deployment | Release processes | Automate |
| Monitoring | Alert management | Optimize |

### 5.2 Automation Priority

```python
class ToilTracker:
    def calculate_toil_score(self, task: Task) -> float:
        frequency = task.frequency_per_week
        duration = task.duration_minutes
        impact = task.impact_score
        
        return (frequency * duration * impact) / 100
    
    def prioritize_automation(self) -> List[Task]:
        tasks = self.get_all_tasks()
        scored = [(task, self.calculate_toil_score(task)) for task in tasks]
        return sorted(scored, key=lambda x: x[1], reverse=True)
```

---

## 6. APIs

### 6.1 SRE Operations API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/sre/slos` | GET | List SLOs |
| `/api/v1/sre/slos/{id}/budget` | GET | Get error budget |
| `/api/v1/sre/incidents` | GET | List incidents |
| `/api/v1/sre/incidents` | POST | Create incident |
| `/api/v1/sre/incidents/{id}` | PUT | Update incident |
| `/api/v1/sre/runbooks` | GET | List runbooks |
| `/api/v1/sre/runbooks/{id}` | GET | Get runbook |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
