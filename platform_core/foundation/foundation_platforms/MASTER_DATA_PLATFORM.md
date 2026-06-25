# MASTER DATA PLATFORM

**NHDOS Platform-Core — Foundation Platform 1: Master Data Management**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The Master Data Platform (MDP) is the authoritative source of truth for all core business entities across the National Healthcare Digital Operating System (NHDOS). It provides golden record management, identity resolution, duplicate detection, merge rules, stewardship, ownership, lifecycle management, and versioning for 11 master data domains serving 44 million citizens.

---

## 2. Architecture

### 2.1 Core Principles

| Principle | Description |
|-----------|-------------|
| Single Source of Truth | Each master domain has one authoritative source |
| Identity Resolution | Deterministic and probabilistic matching |
| Golden Record | Consolidated view of each entity |
| Stewardship | Clear ownership and quality accountability |
| Lifecycle Management | Create → Active → Inactive → Archived |
| Versioning | Every change is versioned with audit trail |

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MASTER DATA PLATFORM                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Identity   │  │   Golden     │  │   Stewardship│          │
│  │   Resolution │──▶│   Record     │──▶│   Engine     │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │  Duplicate   │  │   Merge      │  │   Lifecycle  │          │
│  │  Detection   │  │   Engine     │  │   Manager    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Data Quality│  │  Version     │  │  Audit       │          │
│  │  Engine      │  │  Control     │  │  Trail       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Master Data Domains

### 3.1 Domain Registry

| Domain | Description | Owner | Records |
|--------|-------------|-------|---------|
| Citizen Master | National identity, demographics | Ministry of Health | 44,000,000 |
| Patient Master | Healthcare patient records | Healthcare Facilities | 35,000,000 |
| Professional Master | Healthcare professionals | Ministry of Health | 85,000 |
| Organization Master | Healthcare organizations | Ministry of Health | 2,500 |
| Facility Master | Healthcare facilities | Ministry of Health | 4,800 |
| Laboratory Master | Laboratory information | Laboratory Network | 1,200 |
| Medical Device Master | Medical devices | Device Registry | 45,000 |
| Medication Master | Pharmaceutical products | Drug Authority | 28,000 |
| Reference Organization Master | Reference organizations | Ministry of Health | 500 |
| Location Master | Geographic hierarchy | National Statistics | 18,000 |
| Insurance Master | Insurance providers | Insurance Authority | 350 |

---

## 4. Golden Record

### 4.1 Identity Resolution Process

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Incoming      │────▶│  Matching        │────▶│  Golden Record  │
│   Record        │     │  Engine          │     │  Creation       │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │
                              ▼
                        ┌──────────────────┐
                        │  Duplicate       │
                        │  Detection       │
                        └──────────────────┘
```

### 4.2 Matching Rules

| Rule Type | Description | Confidence | Override |
|-----------|-------------|------------|----------|
| Deterministic | Exact match on national_id | 100% | None |
| Probabilistic | Name + DOB + Gender | 85-99% | Steward |
| Fuzzy | Name similarity + Address | 70-84% | Steward |
| Manual | Human review required | N/A | Committee |

### 4.3 Duplicate Detection

| Detection Method | Description | Performance |
|------------------|-------------|-------------|
| Exact Match | National ID comparison | < 1ms |
| Phonetic Match | Soundex/Metaphone algorithms | < 10ms |
| Fuzzy Match | Levenshtein distance | < 50ms |
| ML-based Match | Trained similarity model | < 100ms |

### 4.4 Merge Rules

| Conflict Type | Resolution Strategy | Escalation |
|---------------|---------------------|------------|
| Data Conflict | Latest wins (by timestamp) | None |
| Source Conflict | Highest authority wins | Steward |
| Missing Data | Fill from any available source | None |
| Contradictory | Flag for manual review | Committee |

---

## 5. Stewardship

### 5.1 Ownership Matrix

| Domain | Steward Role | Escalation |
|--------|--------------|------------|
| Citizen | National Registration Authority | Ministry of Interior |
| Patient | Facility Data Manager | Ministry of Health |
| Professional | Medical Council | Ministry of Health |
| Organization | Ministry Department | Minister |
| Facility | Regional Health Director | Ministry of Health |
| Laboratory | Lab Network Coordinator | Ministry of Health |
| Device | Device Registry Manager | Ministry of Health |
| Medication | Drug Authority Director | Ministry of Health |

### 5.2 Quality Rules

| Rule | Description | Severity | Auto-fix |
|------|-------------|----------|----------|
| Required Fields | All mandatory fields populated | Critical | No |
| Format Validation | Fields match defined formats | High | Yes |
| Uniqueness | Key identifiers unique | Critical | No |
| Consistency | Related records consistent | High | No |
| Timeliness | Updates within defined SLA | Medium | No |
| Referential Integrity | Foreign keys valid | Critical | No |

---

## 6. Lifecycle Management

### 6.1 Entity States

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Draft   │────▶│  Active  │────▶│ Inactive │────▶│ Archived │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
      │               │               │               │
      ▼               ▼               ▼               ▼
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Rejected │     │ Suspended│     │ Merged   │     │ Deleted  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
```

### 6.2 State Transitions

| From | To | Trigger | Conditions |
|------|-----|---------|------------|
| Draft | Active | Validation passed | All quality rules pass |
| Active | Inactive | Deactivation request | No active dependencies |
| Inactive | Archived | Archive policy | Retention period elapsed |
| Active | Suspended | Suspended by authority | Legal/regulatory requirement |
| Any | Merged | Duplicate resolution | Target golden record exists |

---

## 7. Versioning

### 7.1 Version Strategy

| Aspect | Strategy |
|--------|----------|
| Version Format | Semantic Versioning (MAJOR.MINOR.PATCH) |
| Major Version | Breaking changes to master data schema |
| Minor Version | New fields, non-breaking changes |
| Patch Version | Data corrections, no schema changes |
| Version History | Immutable audit trail of all versions |
| Rollback | Support for version rollback within retention |

### 7.2 Version Metadata

```json
{
  "version": "1.0.0",
  "created_at": "2026-01-01T00:00:00Z",
  "created_by": "system",
  "updated_at": "2026-01-15T10:30:00Z",
  "updated_by": "steward_001",
  "change_reason": "Demographic update",
  "previous_version": "1.0.0",
  "version_hash": "sha256:abc123..."
}
```

---

## 8. APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/master-data/{domain} | GET | List master records |
| /api/v1/master-data/{domain}/{id} | GET | Get master record |
| /api/v1/master-data/{domain} | POST | Create master record |
| /api/v1/master-data/{domain}/{id} | PUT | Update master record |
| /api/v1/master-data/{domain}/{id}/version | GET | Get version history |
| /api/v1/master-data/{domain}/{id}/merge | POST | Merge records |
| /api/v1/master-data/{domain}/search | GET | Search master records |
| /api/v1/master-data/{domain}/resolve | POST | Identity resolution |
| /api/v1/master-data/{domain}/quality | GET | Get quality metrics |
| /api/v1/master-data/{domain}/stewardship | GET | Get stewardship info |

---

## 9. Offline Support

| Capability | Support Level |
|------------|---------------|
| Read | Full offline read with local cache |
| Create | Offline create with sync on reconnect |
| Update | Offline update with conflict resolution |
| Delete | Soft delete, sync on reconnect |
| Search | Full-text search on local cache |
| Identity Resolution | Offline probabilistic matching |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
