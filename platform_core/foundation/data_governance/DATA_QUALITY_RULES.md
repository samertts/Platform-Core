# DATA QUALITY RULES

**NHDOS Platform-Core — Data Quality Rules**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS Data Quality Rules engine validates data across all platform services, ensuring accuracy, completeness, consistency, and timeliness. It provides configurable rules, automated validation, and quality scoring to maintain high data standards.

---

## 2. Architecture Overview

### 2.1 Data Quality Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Data Quality System                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Rule      │  │  Validation │  │  Quality    │     │
│  │   Engine    │──▶│  Pipeline   │──▶│  Scorer     │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│         │                │                │              │
│         ▼                ▼                ▼              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Rules     │  │  Validation │  │  Quality    │     │
│  │   Store     │  │  Results    │  │  Reports    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Quality Dimensions

### 3.1 Quality Dimensions

| Dimension | Description | Measurement |
|-----------|-------------|-------------|
| Accuracy | Data matches real-world values | % correct values |
| Completeness | Required fields populated | % fields filled |
| Consistency | Data matches across systems | % consistent |
| Timeliness | Data is current and available | Latency |
| Uniqueness | No duplicate records | % unique |
| Validity | Data conforms to rules | % valid |

### 3.2 Quality Score Formula

```python
def calculate_quality_score(record: Record) -> float:
    weights = {
        "accuracy": 0.25,
        "completeness": 0.25,
        "consistency": 0.20,
        "timeliness": 0.15,
        "uniqueness": 0.10,
        "validity": 0.05
    }
    
    scores = {
        "accuracy": calculate_accuracy(record),
        "completeness": calculate_completeness(record),
        "consistency": calculate_consistency(record),
        "timeliness": calculate_timeliness(record),
        "uniqueness": calculate_uniqueness(record),
        "validity": calculate_validity(record)
    }
    
    return sum(scores[dim] * weights[dim] for dim in weights)
```

---

## 4. Quality Rules

### 4.1 Rule Types

| Type | Description | Example |
|------|-------------|---------|
| `required` | Field must exist | National ID required |
| `format` | Matches pattern | Date format YYYY-MM-DD |
| `range` | Within bounds | Age between 0-150 |
| `reference` | References valid entity | Facility ID exists |
| `uniqueness` | Value is unique | National ID unique |
| `custom` | Business logic | Valid diagnosis code |

### 4.2 Rule Definition

```json
{
  "rule_id": "patient-national-id-required",
  "entity": "patient",
  "field": "national_id",
  "type": "required",
  "severity": "error",
  "message": "National ID is required",
  "enabled": true
}

{
  "rule_id": "patient-age-range",
  "entity": "patient",
  "field": "date_of_birth",
  "type": "custom",
  "severity": "warning",
  "message": "Patient age must be between 0 and 150",
  "expression": "age >= 0 AND age <= 150",
  "enabled": true
}
```

### 4.3 Predefined Rules

| Rule ID | Entity | Field | Type | Severity |
|---------|--------|-------|------|----------|
| patient-national-id | patient | national_id | required | error |
| patient-national-id-format | patient | national_id | format | error |
| patient-dob-valid | patient | date_of_birth | custom | error |
| patient-phone-format | patient | phone | format | warning |
| patient-email-format | patient | email | format | warning |
| appointment-future-date | appointment | date | custom | error |
| prescription-medication-id | prescription | medication_id | reference | error |

---

## 5. Validation Pipeline

### 5.1 Pipeline Stages

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Pre-     │───▶│    Core     │───▶│    Post-    │───▶│   Quality   │
│  Validation │    │  Validation │    │  Validation │    │   Report    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                 │                  │                   │
       ▼                 ▼                  ▼                   ▼
  Format Check      Rule Engine        Business Logic      Score Calc
  Type Check        Reference Check    Cross-field         Alert Gen
```

### 5.2 Validation Implementation

```python
class DataQualityValidator:
    def validate(self, record: Record) -> ValidationResult:
        errors = []
        warnings = []
        
        # 1. Pre-validation
        if not self.validate_format(record):
            errors.append(ValidationError("Invalid format"))
        
        # 2. Core validation
        for rule in self.get_rules(record.entity_type):
            result = self.evaluate_rule(rule, record)
            if result.severity == "error":
                errors.append(result)
            elif result.severity == "warning":
                warnings.append(result)
        
        # 3. Post-validation
        business_errors = self.validate_business_logic(record)
        errors.extend(business_errors)
        
        # 4. Calculate quality score
        quality_score = self.calculate_quality_score(record)
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            quality_score=quality_score
        )
```

---

## 6. APIs

### 6.1 Quality Management API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/quality/rules` | GET | List quality rules |
| `/api/v1/quality/rules` | POST | Create quality rule |
| `/api/v1/quality/rules/{id}` | PUT | Update quality rule |
| `/api/v1/quality/validate` | POST | Validate record |
| `/api/v1/quality/scores/{entity}` | GET | Get quality scores |
| `/api/v1/quality/reports` | GET | Get quality reports |

### 6.2 Quality Dashboard

| Metric | Description | Target |
|--------|-------------|--------|
| Overall Score | Average quality score | > 95% |
| Error Rate | Records with errors | < 1% |
| Warning Rate | Records with warnings | < 5% |
| Completeness | Required fields filled | > 99% |
| Accuracy | Correct values | > 98% |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
