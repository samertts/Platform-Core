# REFERENCE DATA PLATFORM

**NHDOS Platform-Core — Foundation Platform 2: National Reference Data**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The Reference Data Platform provides authoritative, versioned reference data for all NHDOS systems. It supports international standards (ICD-11, SNOMED CT, LOINC, UCUM, ATC, ISO codes) and national reference data (governorates, districts, facilities, organizations, devices, tests, medications) serving 44 million citizens across 18 governorates.

---

## 2. Architecture

### 2.1 Core Principles

| Principle | Description |
|-----------|-------------|
| Authoritative Source | One source of truth for each reference dataset |
| Version Control | Every reference data change is versioned |
| Standard Compliance | Adherence to international healthcare standards |
| Offline Support | Full offline access to reference data |
| Cache Strategy | Multi-level caching for performance |
| API-First | RESTful APIs for all reference data access |

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    REFERENCE DATA PLATFORM                       │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  International│  │   National   │  │  Validation  │          │
│  │  Standards   │──▶│  Reference  │──▶│  Engine      │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │  Code System │  │   Version    │  │   Cache      │          │
│  │  Manager     │  │   Control    │  │   Layer      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. International Standards

### 3.1 ICD-11 (International Classification of Diseases)

| Attribute | Description |
|-----------|-------------|
| Purpose | Disease and health condition coding |
| Scope | All diagnoses, symptoms, procedures |
| Version | 2024 release |
| Language | English, Arabic |
| Update Frequency | Annual |
| Record Count | ~55,000 codes |

### 3.2 SNOMED CT (Systematized Nomenclature of Medicine)

| Attribute | Description |
|-----------|-------------|
| Purpose | Clinical term coding |
| Scope | Clinical findings, procedures, organisms |
| Version | January 2026 release |
| Language | English, Arabic |
| Update Frequency | Semi-annual |
| Record Count | ~350,000 codes |

### 3.3 LOINC (Logical Observation Identifiers Names and Codes)

| Attribute | Description |
|-----------|-------------|
| Purpose | Laboratory and clinical observation coding |
| Scope | Lab tests, vital signs, clinical measurements |
| Version | 2.76 |
| Language | English |
| Update Frequency | Tri-annual |
| Record Count | ~90,000 codes |

### 3.4 UCUM (Unified Code for Units of Measure)

| Attribute | Description |
|-----------|-------------|
| Purpose | Unit of measure coding |
| Scope | All clinical and laboratory units |
| Version | 2.1 |
| Language | English |
| Update Frequency | As needed |
| Record Count | ~3,000 codes |

### 3.5 ATC (Anatomical Therapeutic Chemical)

| Attribute | Description |
|-----------|-------------|
| Purpose | Medication classification |
| Scope | All pharmaceutical products |
| Version | 2026 |
| Language | English |
| Update Frequency | Annual |
| Record Count | ~5,000 codes |

### 3.6 ISO Codes

| Standard | Purpose | Record Count |
|----------|---------|--------------|
| ISO 3166-1 | Country codes | ~250 |
| ISO 3166-2 | Subdivision codes | ~5,000 |
| ISO 639-1 | Language codes | ~180 |
| ISO 4217 | Currency codes | ~170 |

---

## 4. National Reference Data

### 4.1 Geographic Reference Data

| Domain | Description | Record Count |
|--------|-------------|--------------|
| Governorates | 18 national governorates | 18 |
| Districts | District codes | ~100 |
| Cities | City codes | ~500 |
| Villages | Village codes | ~5,000 |
| Postal Codes | Postal code system | ~3,000 |

### 4.2 Healthcare Structure Reference Data

| Domain | Description | Record Count |
|--------|-------------|--------------|
| Organizations | Healthcare organizations | ~100 |
| Facilities | Healthcare facilities | ~4,800 |
| Departments | Facility departments | ~5,000 |
| Laboratories | Laboratory units | ~1,200 |
| Medical Devices | Device classifications | ~45,000 |

### 4.3 Clinical Reference Data

| Domain | Description | Record Count |
|--------|-------------|--------------|
| Test Catalog | Laboratory tests | ~1,000 |
| Medication Catalog | Drug products | ~28,000 |
| Procedure Catalog | Clinical procedures | ~2,000 |
| Device Catalog | Medical devices | ~45,000 |

---

## 5. Versioning Strategy

### 5.1 Version Format

```
{standard}_{version}_{release_date}
Example: ICD11_2024.01_2026-01-01
```

### 5.2 Version Lifecycle

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Draft   │────▶│  Review  │────▶│ Approved │────▶│  Active  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
                                              │
                                              ▼
                                        ┌──────────┐
                                        │ Deprecated│
                                        └──────────┘
```

### 5.3 Backward Compatibility

| Change Type | Compatibility | Migration |
|-------------|---------------|-----------|
| New Code Added | Compatible | None required |
| Code Description Updated | Compatible | None required |
| Code Deprecated | Compatible | Warning issued |
| Code Removed | Breaking | Migration required |
| Hierarchy Changed | Breaking | Migration required |

---

## 6. APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/reference-data/{standard} | GET | List codes for standard |
| /api/v1/reference-data/{standard}/{code} | GET | Get specific code |
| /api/v1/reference-data/{standard}/search | GET | Search codes |
| /api/v1/reference-data/{standard}/version | GET | Get version info |
| /api/v1/reference-data/{standard}/validate | POST | Validate code |
| /api/v1/reference-data/{standard}/expand | POST | Expand value set |
| /api/v1/reference-data/{standard}/map | POST | Map between standards |

---

## 7. Offline Support

| Capability | Implementation |
|------------|----------------|
| Local Cache | Full reference data cached locally |
| Sync Protocol | Delta sync on reconnect |
| Conflict Resolution | Version-based conflict resolution |
| Cache Invalidation | TTL-based with manual override |
| Storage | SQLite for offline reference data |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
