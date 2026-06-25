# FEATURE FLAGS

**NHDOS Platform-Core — Feature Flag Platform**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS Feature Flag Platform enables progressive rollout, A/B testing, and operational toggles across all platform services. It provides real-time flag evaluation, user targeting, percentage rollouts, and comprehensive audit trails for feature management.

---

## 2. Architecture Overview

### 2.1 Feature Flag Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Feature Flag Platform                    │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │    Flag     │  │  Targeting  │  │  Rollout    │     │
│  │  Evaluation │  │   Engine    │  │  Controller │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │              │
│         └────────┬───────┴────────┬───────┘              │
│                  │                │                       │
│         ┌────────▼────────┐ ┌────▼────────────┐         │
│         │  Flag Config    │ │  Event Stream   │         │
│         │  Store          │ │  (Kafka)        │         │
│         └─────────────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Flag Types

| Type | Description | Use Case |
|------|-------------|----------|
| `release` | Feature rollout | New feature enablement |
| `experiment` | A/B testing | User experience testing |
| `ops` | Operational toggle | Circuit breakers, maintenance |
| `permission` | Access control | User permissions |
| `contract` | API versioning | API compatibility |

---

## 3. Feature Flag Model

### 3.1 Flag Definition

```json
{
  "flag_key": "patient-portal-v2",
  "name": "Patient Portal V2",
  "description": "Enable new patient portal experience",
  "type": "release",
  "enabled": true,
  "default_variant": "control",
  "variants": {
    "control": {"enabled": false},
    "treatment_a": {"enabled": true},
    "treatment_b": {"enabled": true}
  },
  "targeting_rules": [
    {
      "conditions": [
        {"attribute": "country", "operator": "in", "values": ["IQ"]},
        {"attribute": "user_type", "operator": "eq", "value": "patient"}
      ],
      "variant": "treatment_a"
    }
  ],
  "rollout_percentage": 25,
  "scheduled_rollout": [
    {"percentage": 25, "date": "2026-06-25"},
    {"percentage": 50, "date": "2026-07-01"},
    {"percentage": 100, "date": "2026-07-15"}
  ]
}
```

### 3.2 Targeting Rules

| Operator | Description | Example |
|----------|-------------|---------|
| `eq` | Equals | `user_type eq patient` |
| `neq` | Not equals | `status neq suspended` |
| `in` | In list | `country in [IQ, KW]` |
| `nin` | Not in list | `role nin [admin]` |
| `gt` | Greater than | `age gt 18` |
| `lt` | Less than | `risk_score lt 0.5` |
| `contains` | String contains | `email contains @hospital` |
| `starts_with` | Prefix match | `id starts_with PAT` |

---

## 4. Flag Evaluation

### 4.1 Evaluation Flow

```
1. SDK requests flag evaluation
2. Check local cache (in-memory, 30s TTL)
3. If cache miss, fetch from Flag Service
4. Apply targeting rules in order
5. Calculate rollout bucket (user hash % 100)
6. Return variant result
7. Update local cache
```

### 4.2 Evaluation Algorithm

```python
def evaluate_flag(flag_key: str, context: UserContext) -> Variant:
    flag = get_flag(flag_key)

    # 1. Check if flag is globally enabled
    if not flag.enabled:
        return flag.default_variant

    # 2. Apply targeting rules
    for rule in flag.targeting_rules:
        if matches_conditions(rule.conditions, context):
            return rule.variant

    # 3. Apply percentage rollout
    bucket = hash_user(context.user_id) % 100
    if bucket < flag.rollout_percentage:
        return "treatment"
    else:
        return "control"
```

---

## 5. APIs

### 5.1 Flag Management API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/flags` | GET | List all flags |
| `/api/v1/flags/{key}` | GET | Get flag details |
| `/api/v1/flags` | POST | Create flag |
| `/api/v1/flags/{key}` | PUT | Update flag |
| `/api/v1/flags/{key}` | DELETE | Delete flag |
| `/api/v1/flags/{key}/evaluate` | POST | Evaluate flag |

### 5.2 SDK Integration

```python
from platform_flags import FeatureFlagClient

client = FeatureFlagClient(environment="production")

# Simple boolean check
if client.is_enabled("patient-portal-v2", user_context):
    show_new_portal()

# Get variant
variant = client.get_variant("patient-portal-v2", user_context)
if variant == "treatment_a":
    apply_treatment_a()

# Track experiment event
client.track("patient-portal-v2", user_context, "portal_accessed")
```

---

## 6. Implementation Details

### 6.1 Flag Storage

| Component | Technology | Purpose |
|-----------|------------|---------|
| Flag Service | Go microservice | Flag management |
| Configuration Store | etcd | Flag definitions |
| Cache Layer | Redis | Evaluation cache |
| Event Stream | Kafka | Flag change events |

### 6.2 SDK Architecture

```
┌─────────────────────────────────────────┐
│           Feature Flag SDK              │
├─────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐      │
│  │  In-Memory  │  │  Streaming  │      │
│  │    Cache    │  │   Updates   │      │
│  └──────┬──────┘  └──────┬──────┘      │
│         │                │              │
│         └────────┬───────┘              │
│                  │                      │
│         ┌────────▼────────┐            │
│         │    Evaluation   │            │
│         │     Engine      │            │
│         └─────────────────┘            │
└─────────────────────────────────────────┘
```

### 6.3 Rollout Strategy

| Phase | Percentage | Duration | Monitoring |
|-------|------------|----------|------------|
| Canary | 5% | 24 hours | Error rate, latency |
| Early Adopters | 25% | 48 hours | User feedback |
| Gradual Rollout | 50% | 72 hours | Business metrics |
| Full Rollout | 100% | - | All metrics |

---

## 7. Audit and Compliance

### 7.1 Audit Events

| Event | Description | Retention |
|-------|-------------|-----------|
| `flag.created` | New flag created | 2 years |
| `flag.updated` | Flag modified | 2 years |
| `flag.enabled` | Flag turned on | 2 years |
| `flag.disabled` | Flag turned off | 2 years |
| `flag.evaluated` | Flag evaluated | 90 days |
| `rollout.changed` | Rollout percentage changed | 2 years |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
