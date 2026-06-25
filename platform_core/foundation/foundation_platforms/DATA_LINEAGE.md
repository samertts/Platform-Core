# DATA LINEAGE

**NHDOS Platform-Core — Foundation Platform 17: Data Lineage**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The Data Lineage platform tracks the complete data flow across NHDOS, providing source-to-destination visibility, transformation tracking, impact analysis, and compliance reporting for 44 million citizens' health data.

---

## 2. Architecture

### 2.1 Core Principles

| Principle | Description |
|-----------|-------------|
| End-to-End | Complete lineage from source to consumption |
| Automated | Automated lineage discovery |
| Real-time | Real-time lineage updates |
| Impact Analysis | Downstream impact analysis |
| Compliance | Regulatory compliance support |

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA LINEAGE                                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Lineage     │  │   Impact     │  │   Compliance │          │
│  │  Discovery   │──▶│   Analysis   │──▶│   Reporter   │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │  Graph       │  │   Query      │  │   Visualizer │          │
│  │  Store       │  │   Engine     │  │   Dashboard  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Lineage Model

### 3.1 Lineage Graph

| Node Type | Description | Example |
|-----------|-------------|---------|
| Source | Data origin | EMR System |
| Transformation | Data transformation | ETL Job |
| Dataset | Data storage | Patient Table |
| Consumer | Data consumer | Analytics Dashboard |

### 3.2 Lineage Relationships

| Relationship | Description |
|--------------|-------------|
| SOURCE_OF | Source provides data to target |
| TRANSFORMS | Transformation processes data |
| DERIVES | Target derived from source |
| REFERENCES | Target references source |

---

## 4. Lineage Tracking

### 4.1 Tracked Elements

| Element | Description |
|---------|-------------|
| Sources | All data sources |
| Transformations | All data transformations |
| Datasets | All data storage |
| Consumers | All data consumers |
| Quality Checks | All quality validations |

### 4.2 Lineage Metadata

| Field | Description |
|-------|-------------|
| source | Source system |
| target | Target system |
| transformation | Transformation applied |
| frequency | How often data flows |
| volume | Data volume |
| quality | Quality metrics |

---

## 5. Impact Analysis

### 5.1 Impact Types

| Type | Description |
|------|-------------|
| Schema Change | Impact of schema changes |
| Data Quality | Impact of quality issues |
| System Outage | Impact of system outages |
| Regulatory | Impact of regulatory changes |

### 5.2 Impact Report

```yaml
impact_analysis:
  target: "patient-diagnosis"
  changes:
    - type: "schema_change"
      field: "diagnosis_code"
      impact:
        downstream:
          - "analytics-dashboard"
          - "reporting-system"
        severity: "high"
        recommendation: "Update all downstream consumers"
```

---

## 6. APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/lineage | GET | Get full lineage graph |
| /api/v1/lineage/{dataset} | GET | Get dataset lineage |
| /api/v1/lineage/{dataset}/impact | GET | Get impact analysis |
| /api/v1/lineage/{dataset}/upstream | GET | Get upstream lineage |
| /api/v1/lineage/{dataset}/downstream | GET | Get downstream lineage |
| /api/v1/lineage/search | GET | Search lineage |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
