# RULE ENGINE

**NHDOS Platform-Core — Foundation Platform 21: Rules Engine**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The Rules Engine provides business rules, clinical rules, policy rules, decision tables, rule versioning, simulation, and validation capabilities for NHDOS across 18 governorates and 4,800 healthcare facilities.

---

## 2. Architecture

### 2.1 Core Principles

| Principle | Description |
|-----------|-------------|
| Declarative | Rules expressed declaratively |
| Auditable | All rule executions audited |
| Versioned | Rules versioned with rollback |
| Testable | Rules can be simulated |
| Fast | Sub-millisecond evaluation |
| Offline | Rules cached on edge sites |

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    RULE ENGINE                                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Rule        │  │   Decision   │  │   Simulation │          │
│  │  Repository  │──▶│   Tables     │──▶│   Engine     │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │  Rule        │  │   Validation │  │   Audit      │          │
│  │  Executor    │  │   Engine     │  │   Trail      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Rule Types

### 3.1 Business Rules

| Rule Type | Description | Example |
|-----------|-------------|---------|
| Validation | Data validation rules | Required fields |
| Calculation | Business calculations | Insurance coverage |
| Workflow | Workflow routing rules | Triage routing |
| Alert | Alert generation rules | Critical values |

### 3.2 Clinical Rules

| Rule Type | Description | Example |
|-----------|-------------|---------|
| Drug Interaction | Drug-drug interactions | Warfarin + Aspirin |
| Allergy Alert | Allergy alerts | Penicillin allergy |
| Dosage Check | Dosage validation | Pediatric dosing |
| Lab Value | Lab value interpretation | Critical values |
| Protocol | Clinical protocol adherence | Sepsis protocol |

### 3.3 Policy Rules

| Rule Type | Description | Example |
|-----------|-------------|---------|
| Consent | Consent validation | Treatment consent |
| Authorization | Authorization requirements | Pre-authorization |
| Compliance | Regulatory compliance | Data retention |
| Access | Access control rules | Role-based access |

---

## 4. Decision Tables

### 4.1 Decision Table Format

| Condition 1 | Condition 2 | Action |
|-------------|-------------|--------|
| Age > 65 | Weight < 50kg | Reduce dose 50% |
| Age > 65 | Weight >= 50kg | Standard dose |
| Age <= 65 | Weight < 50kg | Reduce dose 25% |
| Age <= 65 | Weight >= 50kg | Standard dose |

### 4.2 Clinical Decision Tables

| Table | Conditions | Actions |
|-------|------------|---------|
| Sepsis Screening | Temp, HR, RR, WBC | Alert, Protocol |
| Drug Dosing | Age, Weight, Renal | Dose Calculation |
| Triage Level | Vitals, Symptoms | Triage Category |
| Lab Interpretation | Test, Value, Age | Interpretation |

---

## 5. Rule Versioning

### 5.1 Version Strategy

| Aspect | Strategy |
|--------|----------|
| Version Format | Semantic Versioning |
| Major Version | Breaking rule changes |
| Minor Version | New rules added |
| Patch Version | Rule corrections |
| Rollback | Support version rollback |

### 5.2 Version Lifecycle

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Draft   │────▶│  Review  │────▶│ Active   │────▶│ Retired  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
```

---

## 6. Simulation

### 6.1 Simulation Capabilities

| Capability | Description |
|------------|-------------|
| Rule Testing | Test rules against test data |
| Impact Analysis | Analyze rule impact |
| What-If | What-if scenario analysis |
| Regression | Regression testing |

### 6.2 Simulation API

```json
{
  "rule_set": "drug-interaction",
  "test_data": {
    "patient": {"age": 65, "weight": 70},
    "medications": ["warfarin", "aspirin"]
  },
  "expected": {
    "alerts": ["drug-interaction-warfarin-aspirin"]
  }
}
```

---

## 7. Rule APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/rules | GET | List all rules |
| /api/v1/rules/{rule} | GET | Get rule |
| /api/v1/rules/{rule}/evaluate | POST | Evaluate rule |
| /api/v1/rules/{rule}/simulate | POST | Simulate rule |
| /api/v1/rules/{rule}/versions | GET | Get rule versions |
| /api/v1/rules/decision-table/{table} | POST | Evaluate decision table |

---

## 8. Offline Support

| Capability | Implementation |
|------------|----------------|
| Rule Cache | Rules cached on edge |
| Local Evaluation | Rules evaluated locally |
| Sync Protocol | Delta sync on reconnect |
| Cache Size | ~100MB |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
