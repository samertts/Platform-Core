# TERMINOLOGY PLATFORM

**NHDOS Platform-Core — Foundation Platform 3: National Terminology Server**
**Version:** 1.0.0 | **Date:** 2026-06-25 | **Status:** CERTIFIED

---

## 1. Executive Summary

The Terminology Platform is the National Terminology Server for NHDOS, providing FHIR-compatible terminology services including code systems, value sets, concept maps, validation, expansion, translation, versioning, and terminology APIs for all healthcare data exchange across 18 governorates.

---

## 2. Architecture

### 2.1 Core Principles

| Principle | Description |
|-----------|-------------|
| FHIR Compliance | Full HL7 FHIR R4 terminology service |
| Standard Support | ICD-11, SNOMED CT, LOINC, UCUM, ATC |
| Bilingual | Arabic and English terminology |
| Offline Capable | Local terminology cache for edge sites |
| Versioned | All terminology versions tracked |
| API-First | RESTful terminology APIs |

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    TERMINOLOGY PLATFORM                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  FHIR        │  │   Code       │  │   Value Set  │          │
│  │  Terminology │──▶│   Systems   │──▶│   Manager    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                  │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │  Concept     │  │   Validation │  │   Expansion  │          │
│  │  Maps        │  │   Engine     │  │   Engine     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. FHIR Terminology Service

### 3.1 FHIR Resources

| Resource | Description | Implementation |
|----------|-------------|----------------|
| CodeSystem | Defines a code system | Full support |
| ValueSet | Defines a value set | Full support |
| ConceptMap | Maps between code systems | Full support |
| ExpansionProfile | Controls value set expansion | Full support |

### 3.2 FHIR Operations

| Operation | Description | Performance |
|-----------|-------------|-------------|
| $validate-code | Validate a code against value set | < 50ms |
| $expand | Expand a value set | < 500ms |
| $lookup | Look up a code | < 25ms |
| $translate | Translate between code systems | < 200ms |
| $subsumes | Test subsumption relationship | < 100ms |
| $closure | Closure table maintenance | < 1s |

---

## 4. Code Systems

### 4.1 Supported Code Systems

| System | URI | Version | Records |
|--------|-----|---------|---------|
| ICD-11 | http://who.int/icd/11 | 2024 | ~55,000 |
| SNOMED CT | http://snomed.info/sct | 2026.01 | ~350,000 |
| LOINC | http://loinc.org | 2.76 | ~90,000 |
| UCUM | http://unitsofmeasure.org | 2.1 | ~3,000 |
| ATC | http://who.int/atc | 2026 | ~5,000 |
| NHDOS-National | http://nhdos.iq/code-system | 1.0 | ~50,000 |

### 4.2 Custom Code Systems

| System | Purpose | Records |
|--------|---------|---------|
| NHDOS-Facility | Facility identifiers | ~4,800 |
| NHDOS-Provider | Provider identifiers | ~85,000 |
| NHDOS-Test | Lab test identifiers | ~1,000 |
| NHDOS-Medication | Medication identifiers | ~28,000 |
| NHDOS-Procedure | Procedure identifiers | ~2,000 |

---

## 5. Value Sets

### 5.1 Core Value Sets

| Value Set | Description | Codes |
|-----------|-------------|-------|
| NHDOS-Gender | Administrative gender | 4 |
| NHDOS-MaritalStatus | Marital status | 8 |
| NHDOS-EncounterType | Encounter types | 25 |
| NHDOS-ConditionCategory | Condition categories | 15 |
| NHDOS-ObservationCategory | Observation categories | 20 |
| NHDOS-AllergyCategory | Allergy categories | 10 |
| NHDOS-ImmunizationStatus | Immunization status | 6 |

### 5.2 Clinical Value Sets

| Value Set | Description | Codes |
|-----------|-------------|-------|
| NHDOS-BloodPressure | Blood pressure interpretation | 5 |
| NHDOS-PainScale | Pain assessment scale | 11 |
| NHDOS-GlasgowComaScale | Glasgow coma scale | 13 |
| NHDOS-APGAR | APGAR score | 11 |

---

## 6. Concept Maps

### 6.1 Cross-Standard Mappings

| Source | Target | Direction | Mappings |
|--------|--------|-----------|----------|
| ICD-11 | SNOMED CT | Bidirectional | ~40,000 |
| SNOMED CT | LOINC | Bidirectional | ~25,000 |
| ICD-11 | LOINC | Bidirectional | ~15,000 |
| NHDOS-National | ICD-11 | Unidirectional | ~10,000 |
| NHDOS-National | SNOMED CT | Unidirectional | ~10,000 |

### 6.2 Translation Maps

| Source | Target | Purpose |
|--------|--------|---------|
| English Terms | Arabic Terms | Bilingual terminology |
| Lay Terms | Clinical Terms | Patient-friendly mapping |
| Legacy Codes | Modern Codes | Migration support |

---

## 7. Validation

### 7.1 Validation Rules

| Rule | Description | Severity |
|------|-------------|----------|
| Code Exists | Code exists in code system | Error |
| Active Status | Code is active | Warning |
| Effective Period | Code is in effective period | Warning |
| Value Set Membership | Code is in required value set | Error |
| Format Validation | Code format is correct | Error |

### 7.2 Validation API

| Endpoint | Method | Description |
|----------|--------|-------------|
| /fhir/ValueSet/$validate-code | GET | Validate code against value set |
| /fhir/CodeSystem/$validate-code | GET | Validate code format |
| /api/v1/terminology/validate | POST | Bulk validation |

---

## 8. APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| /fhir/CodeSystem | GET | List code systems |
| /fhir/CodeSystem/{id} | GET | Get code system |
| /fhir/ValueSet | GET | List value sets |
| /fhir/ValueSet/$expand | GET | Expand value set |
| /fhir/ConceptMap | GET | List concept maps |
| /fhir/ConceptMap/$translate | GET | Translate code |
| /api/v1/terminology/search | GET | Search terminology |
| /api/v1/terminology/version | GET | Get version info |

---

## 9. Offline Support

| Capability | Implementation |
|------------|----------------|
| Local Cache | Full terminology cache on edge |
| Sync Protocol | Delta sync on reconnect |
| Offline Validation | Local validation engine |
| Cache Size | ~500MB compressed |
| Update Frequency | Daily delta sync |

---

*Generated as part of NHDOS Platform-Core Phase 18 National Foundation Platforms*
