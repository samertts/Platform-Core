# SEARCH PLATFORM

**NHDOS Platform-Core — Foundation Platform 19: Search Platform**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The Search Platform provides comprehensive search capabilities for NHDOS, including full-text search, semantic search, FHIR search, medical search, document search, and knowledge search across 44 million citizens and 4,800 healthcare facilities.

---

## 2. Architecture

### 2.1 Core Principles

| Principle | Description |
|-----------|-------------|
| Fast | Sub-second search results |
| Relevant | Medically relevant results |
| Multilingual | Arabic and English support |
| FHIR Compliant | FHIR search parameters |
| Secure | Role-based search access |
| Offline | Local search on edge sites |

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SEARCH PLATFORM                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Full Text   │  │   Semantic   │  │   FHIR       │          │
│  │  Search      │──▶│   Search     │──▶│   Search     │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │  Medical     │  │   Document   │  │   Knowledge  │          │
│  │  Search      │  │   Search     │  │   Search     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Search Types

### 3.1 Full-Text Search

| Feature | Description |
|---------|-------------|
| Text Matching | Exact and fuzzy text matching |
| Phrase Matching | Exact phrase matching |
| Boolean | AND, OR, NOT operators |
| Wildcard | * and ? wildcards |
| Proximity | Near-match searches |
| Ranking | TF-IDF and BM25 ranking |

### 3.2 Semantic Search

| Feature | Description |
|---------|-------------|
| Vector Search | Embedding-based similarity |
| Concept Search | Medical concept matching |
| Synonym Expansion | Synonym-aware search |
| Contextual | Context-aware results |

### 3.3 FHIR Search

| Resource | Search Parameters |
|----------|-------------------|
| Patient | name, identifier, birthdate, gender, address |
| Encounter | patient, date, type, status, location |
| Condition | patient, code, clinical-status, onset-date |
| Observation | patient, code, date, category, value |
| MedicationRequest | patient, status, intent, medication |
| DiagnosticReport | patient, code, date, status |

### 3.4 Medical Search

| Feature | Description |
|---------|-------------|
| ICD-11 Search | Search by ICD-11 code |
| SNOMED CT Search | Search by SNOMED CT concept |
| LOINC Search | Search by LOINC code |
| Drug Search | Search by medication name |
| Procedure Search | Search by procedure name |

---

## 4. Search Index

### 4.1 Indexed Resources

| Resource | Fields | Records |
|----------|--------|---------|
| Patient | name, identifier, demographics | 44M |
| Encounter | type, date, provider | 200M |
| Condition | code, description | 500M |
| Observation | code, value, date | 1B |
| Medication | name, code, class | 28K |
| Document | content, metadata | 100M |

### 4.2 Index Configuration

| Setting | Value |
|---------|-------|
| Shards | 10 |
| Replicas | 3 |
| Refresh Interval | 1 second |
| Max Result Window | 10,000 |

---

## 5. Search APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/search | GET | Full-text search |
| /api/v1/search/semantic | GET | Semantic search |
| /api/v1/search/fhir/{resource} | GET | FHIR search |
| /api/v1/search/medical | GET | Medical search |
| /api/v1/search/documents | GET | Document search |
| /api/v1/search/suggest | GET | Search suggestions |
| /api/v1/search/autocomplete | GET | Autocomplete |

---

## 6. Offline Support

| Capability | Implementation |
|------------|----------------|
| Local Index | Frequently searched data indexed locally |
| Offline Search | Full search on local index |
| Sync Protocol | Delta sync on reconnect |
| Index Size | ~10GB compressed |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
