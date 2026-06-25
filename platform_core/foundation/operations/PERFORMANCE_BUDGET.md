# PERFORMANCE BUDGET

**NHDOS Platform-Core — Performance Budgets**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS Performance Budget framework establishes and enforces performance limits across all platform services. It ensures consistent user experience by setting and monitoring performance thresholds.

---

## 2. Architecture Overview

### 2.1 Performance Budget System

```
┌─────────────────────────────────────────────────────────┐
│              Performance Budget System                     │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Budget     │  │  Monitoring │  │  Alerting   │     │
│  │  Manager    │──▶│  Agent      │──▶│  Engine     │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │              │
│         └────────┬───────┴────────┬───────┘              │
│                  │                │                       │
│         ┌────────▼────────┐ ┌────▼────────────┐         │
│         │  Budget Store   │ │  Metrics Store  │         │
│         │  (PostgreSQL)   │ │  (Prometheus)   │         │
│         └─────────────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Performance Budgets

### 3.1 Web Performance Budgets

| Metric | Budget | Target | Critical |
|--------|--------|--------|----------|
| First Contentful Paint | < 1.5s | < 1.0s | > 3.0s |
| Largest Contentful Paint | < 2.5s | < 2.0s | > 4.0s |
| Time to Interactive | < 3.5s | < 3.0s | > 5.0s |
| Cumulative Layout Shift | < 0.1 | < 0.05 | > 0.25 |
| Total Blocking Time | < 300ms | < 200ms | > 600ms |

### 3.2 API Performance Budgets

| Endpoint | Latency (p95) | Latency (p99) | Throughput |
|----------|---------------|---------------|------------|
| `/patients` | < 100ms | < 200ms | 1000 RPS |
| `/patients/{id}` | < 50ms | < 100ms | 2000 RPS |
| `/appointments` | < 150ms | < 300ms | 500 RPS |
| `/lab-results` | < 100ms | < 200ms | 1000 RPS |

---

## 4. Budget Enforcement

### 4.1 Enforcement Levels

| Level | Action | Threshold |
|-------|--------|-----------|
| Info | Log only | < 80% of budget |
| Warning | Notify team | 80-100% of budget |
| Error | Block deployment | > 100% of budget |
| Critical | Page oncall | > 150% of budget |

### 4.2 CI/CD Integration

```yaml
# .performance-budget.yml
budgets:
  - name: "bundle-size"
    metric: "javascript_bundle_size"
    threshold: "250KB"
    action: "block_merge"
    
  - name: "lcp"
    metric: "largest_contentful_paint"
    threshold: "2.5s"
    action: "warn"
    
  - name: "api-latency"
    metric: "p95_latency"
    threshold: "100ms"
    action: "block_deploy"
```

### 4.3 Budget Monitoring

```python
class PerformanceBudgetMonitor:
    def check_budget(self, service: str, metric: str) -> BudgetResult:
        # 1. Get budget definition
        budget = self.get_budget(service, metric)
        
        # 2. Get current value
        current = self.get_current_value(service, metric)
        
        # 3. Calculate percentage
        percentage = (current / budget.threshold) * 100
        
        # 4. Determine action
        action = self.determine_action(percentage)
        
        return BudgetResult(
            service=service,
            metric=metric,
            budget=budget.threshold,
            current=current,
            percentage=percentage,
            action=action
        )
```

---

## 5. Performance Testing

### 5.1 Test Types

| Type | Description | Frequency |
|------|-------------|-----------|
| Load Test | Normal load | Weekly |
| Stress Test | Peak load | Monthly |
| Soak Test | Extended duration | Quarterly |
| Spike Test | Sudden increase | Monthly |

### 5.2 Performance Test Configuration

```yaml
performance_tests:
  - name: "patient-service-load"
    type: "load"
    target: "https://api.nhdos.iq/patients"
    duration: "30m"
    users: 1000
    ramp_up: "5m"
    thresholds:
      latency_p95: "< 100ms"
      error_rate: "< 0.1%"
      rps: "> 1000"
```

---

## 6. APIs

### 6.1 Performance Budget API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/performance/budgets` | GET | List budgets |
| `/api/v1/performance/budgets` | POST | Create budget |
| `/api/v1/performance/budgets/{id}` | GET | Get budget status |
| `/api/v1/performance/metrics` | GET | Get performance metrics |
| `/api/v1/performance/reports` | GET | Get performance reports |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
