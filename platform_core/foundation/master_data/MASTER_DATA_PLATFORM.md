# MASTER DATA PLATFORM

**NHDOS Platform-Core — Foundation Platform 1**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The Master Data Platform (MDP) is the authoritative source of truth for all core business entities across the National Healthcare Digital Operating System (NHDOS). It provides identity resolution, duplicate detection, merge rules, stewardship, ownership, lifecycle management, and versioning for master data domains.

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

### 2.2 Master Data Domains

| Domain | Description | Owner |
|--------|-------------|-------|
| Citizen Master | National identity, demographics | Ministry of Health |
| Patient Master | Healthcare patient records | Healthcare Facilities |
| Professional Master | Healthcare professionals | Ministry of Health |
| Organization Master | Healthcare organizations | Ministry of Health |
| Facility Master | Healthcare facilities | Ministry of Health |
| Laboratory Master | Laboratory information | Laboratory Network |
| Medical Device Master | Medical devices | Device Registry |
| Medication Master | Pharmaceutical products | Drug Authority |
| Reference Organization Master | Reference organizations | Ministry of Health |
| Location Master | Geographic hierarchy | National Statistics |
| Insurance Master | Insurance providers | Insurance Authority |

---

## 3. Golden Record

### 3.1 Identity Resolution Process

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

### 3.2 Matching Rules

| Rule Type | Description | Confidence |
|-----------|-------------|------------|
| Deterministic | Exact match on national_id | 100% |
| Probabilistic | Name + DOB + Gender | 85-99% |
| Fuzzy | Name similarity + Address | 70-84% |
| Manual | Human review required | N/A |

### 3.3 Merge Rules

| Conflict Type | Resolution Strategy |
|---------------|---------------------|
| Data Conflict | Latest wins (by timestamp) |
| Source Conflict | Highest authority wins |
| Missing Data | Fill from any available source |
| Contradictory | Flag for manual review |

---

## 4. Stewardship

### 4.1 Ownership Matrix

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

### 4.2 Quality Rules

| Rule | Description | Severity |
|------|-------------|----------|
| Required Fields | All mandatory fields must be populated | Critical |
| Format Validation | Fields must match defined formats | High |
| Uniqueness | Key identifiers must be unique | Critical |
| Consistency | Related records must be consistent | High |
| Timeliness | Updates must be within defined SLA | Medium |

---

## 5. Lifecycle Management

### 5.1 Entity States

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

### 5.2 State Transitions

| From | To | Trigger | Conditions |
|------|-----|---------|------------|
| Draft | Active | Validation passed | All quality rules pass |
| Active | Inactive | Deactivation request | No active dependencies |
| Inactive | Archived | Archive policy | Retention period elapsed |
| Active | Suspended | Suspended by authority | Legal/regulatory requirement |
| Any | Merged | Duplicate resolution | Target golden record exists |

---

## 6. Versioning

### 6.1 Version Strategy

| Aspect | Strategy |
|--------|----------|
| Version Format | Semantic Versioning (MAJOR.MINOR.PATCH) |
| Major Version | Breaking changes to master data schema |
| Minor Version | New fields, non-breaking changes |
| Patch Version | Data corrections, no schema changes |
| Version History | Immutable audit trail of all versions |
| Rollback | Support for version rollback within retention |

### 6.2 Version Metadata

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

## 7. APIs

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

---

## 8. Offline Support

| Capability | Support Level |
|------------|---------------|
| Read | Full offline read with local cache |
| Create | Offline create with sync on reconnect |
| Update | Offline update with conflict resolution |
| Delete | Soft delete, sync on reconnect |
| Search | Full-text search on local cache |

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
