# National Healthcare Digital Operating System (NHDOS) - Domain Catalog

**Version:** 1.0.0  
**Status:** CANONICAL MODEL  
**Last Updated:** 2026-06-25  
**Classification:** Production-Ready Documentation

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Domain Catalog Overview](#domain-catalog-overview)
3. [Complete Domain Registry](#complete-domain-registry)
4. [Domain Maturity Assessment](#domain-maturity-assessment)
5. [Domain Priority Matrix](#domain-priority-matrix)
6. [Domain Ownership Matrix](#domain-ownership-matrix)
7. [Domain Statistics Summary](#domain-statistics-summary)

---

## Executive Summary

This document serves as the **CANONICAL CATALOG** of all business domains within the National Healthcare Digital Operating System (NHDOS). It provides a comprehensive inventory of 35+ domains with detailed metadata including ownership, maturity, priority, and key metrics.

### Catalog Purpose

1. **Single Source of Truth**: Authoritative list of all platform domains
2. **Ownership Clarity**: Clear business and technical ownership for each domain
3. **Maturity Tracking**: Assessment of domain development status
4. **Priority Alignment**: Strategic alignment with business objectives
5. **Metrics Dashboard**: Key counts for entities, events, and APIs per domain

---

## Domain Catalog Overview

### Domain Categories

| Category | Description | Domain Count |
|----------|-------------|--------------|
| **Foundation** | Core platform services | 3 |
| **Clinical Care** | Patient care delivery | 12 |
| **Business Operations** | Financial and operational | 6 |
| **Intelligence** | Analytics and AI | 5 |
| **Engagement** | Patient and provider engagement | 4 |
| **Integration** | External connectivity | 3 |
| **Platform Services** | Infrastructure and configuration | 2 |

### Key Metrics

- **Total Domains**: 35
- **Total Core Entities**: 450+
- **Total Domain Events**: 500+
- **Total APIs**: 600+
- **Avg Entities per Domain**: 13
- **Avg Events per Domain**: 15
- **Avg APIs per Domain**: 17

---

## Complete Domain Registry

### Foundation Domains

| Domain ID | Domain Name | Description | Business Owner | Platform Owner | Core Entities | Events | APIs | Maturity | Priority |
|-----------|-------------|-------------|----------------|----------------|---------------|--------|------|----------|----------|
| IDENTITY | Identity & Access Management | User authentication, authorization, and identity management | Chief Information Security Officer | Security Engineering Team | 10 | 10 | 12 | Production | Critical |
| AUTHZ | Authorization & Policy | Role-based access control, permission management, and policy enforcement | Chief Information Security Officer | Security Engineering Team | 8 | 8 | 10 | Production | Critical |
| AUDIT | Audit & Compliance Logging | Comprehensive audit trails, compliance logging, and regulatory reporting | Chief Compliance Officer | Compliance Engineering Team | 6 | 6 | 8 | Production | Critical |

### Clinical Care Domains

| Domain ID | Domain Name | Description | Business Owner | Platform Owner | Core Entities | Events | APIs | Maturity | Priority |
|-----------|-------------|-------------|----------------|----------------|---------------|--------|------|----------|----------|
| PATIENT | Patient Management | Patient demographics, medical history, and master patient index | Chief Medical Officer | Clinical Engineering Team | 12 | 12 | 12 | Production | Critical |
| ENCOUNTER | Encounter Management | Healthcare encounters, clinical documentation, and visit lifecycle | Chief Medical Officer | Clinical Engineering Team | 12 | 12 | 12 | Production | Critical |
| LABORATORY | Laboratory Management | Test orders, specimen tracking, result reporting, and quality control | Laboratory Director | Lab Systems Team | 14 | 14 | 13 | Production | Critical |
| RADIOLOGY | Radiology & Imaging | Imaging orders, DICOM management, PACS integration, and reporting | Radiology Director | Imaging Systems Team | 13 | 13 | 10 | Production | Critical |
| PHARMACY | Pharmacy Management | Medication orders, dispensing, administration, and formulary | Chief Pharmacy Officer | Pharmacy Systems Team | 13 | 13 | 12 | Production | Critical |
| EMERGENCY | Emergency Department | ED triage, patient tracking, critical care, and disaster management | Emergency Medicine Director | ED Systems Team | 12 | 12 | 10 | Production | High |
| BLOOD_BANK | Blood Bank Management | Blood donation, component processing, compatibility testing, and transfusion | Blood Bank Director | Blood Systems Team | 12 | 12 | 10 | Production | High |
| SURGERY | Surgical Services | Surgical scheduling, OR management, anesthesia, and operative reports | Surgery Director | Surgical Systems Team | 10 | 10 | 8 | Beta | High |
| MENTAL_HEALTH | Mental Health Services | Behavioral health, psychiatry, counseling, and mental health records | Behavioral Health Director | Mental Health Systems Team | 8 | 8 | 6 | Beta | Medium |
| REHABILITATION | Rehabilitation Services | Physical therapy, occupational therapy, and rehabilitation programs | Rehabilitation Director | Rehab Systems Team | 8 | 8 | 6 | Beta | Medium |
| CHRONIC_DISEASE | Chronic Disease Management | Chronic condition monitoring, care plans, and disease management programs | Population Health Director | Chronic Care Team | 10 | 10 | 8 | Beta | High |
| HOME_CARE | Home Health Services | Home health visits, remote monitoring, and home-based care coordination | Home Health Director | Home Care Systems Team | 8 | 8 | 6 | Alpha | Medium |

### Operational Support Domains

| Domain ID | Domain Name | Description | Business Owner | Platform Owner | Core Entities | Events | APIs | Maturity | Priority |
|-----------|-------------|-------------|----------------|----------------|---------------|--------|------|----------|----------|
| HOSPITAL | Hospital Operations | Facility management, departments, bed management, and capacity | Chief Operating Officer | Operations Engineering Team | 13 | 10 | 10 | Production | Critical |
| SCHEDULING | Scheduling & Appointments | Appointment booking, resource scheduling, and capacity management | Chief Operating Officer | Scheduling Systems Team | 12 | 12 | 10 | Production | Critical |
| INVENTORY | Inventory Management | Medical supplies, pharmaceuticals, and equipment inventory | Supply Chain Director | Inventory Systems Team | 12 | 12 | 12 | Production | High |
| SUPPLY_CHAIN | Supply Chain & Procurement | Procurement, logistics, vendor management, and supply tracking | Supply Chain Director | Supply Chain Systems Team | 12 | 12 | 12 | Beta | High |
| FINANCE | Financial Management | Billing, revenue cycle, claims processing, and financial reporting | Chief Financial Officer | Finance Systems Team | 14 | 13 | 12 | Production | Critical |
| REVENUE_CYCLE | Revenue Cycle Management | Pre-authorization, claims, payment posting, and denial management | Chief Financial Officer | Revenue Cycle Team | 13 | 13 | 12 | Production | Critical |
| INSURANCE | Insurance & Payer Management | Insurance plans, coverage verification, and payer relationships | Chief Financial Officer | Payer Relations Team | 12 | 10 | 8 | Production | High |
| MEDICAL_DEVICES | Medical Device Management | Device inventory, maintenance, calibration, and clinical integration | Biomedical Engineering Director | Device Systems Team | 12 | 11 | 10 | Beta | High |

### Intelligence & Analytics Domains

| Domain ID | Domain Name | Description | Business Owner | Platform Owner | Core Entities | Events | APIs | Maturity | Priority |
|-----------|-------------|-------------|----------------|----------------|---------------|--------|------|----------|----------|
| ANALYTICS | Analytics & BI | Data analytics, business intelligence, and population health analytics | Chief Data Officer | Analytics Engineering Team | 12 | 11 | 11 | Beta | High |
| AI_ML | AI/ML & Clinical Decision Support | AI models, CDS rules, bias detection, and AI governance | Chief Data Officer | AI Engineering Team | 12 | 11 | 10 | Beta | High |
| REPORTING | Reporting & Dashboards | Operational, clinical, and financial reporting | Chief Data Officer | Reporting Systems Team | 12 | 10 | 10 | Production | High |
| KNOWLEDGE | Clinical Knowledge Management | Medical literature, CDS rules, evidence-based guidelines | Chief Medical Officer | Knowledge Systems Team | 12 | 10 | 10 | Beta | Medium |
| RESEARCH | Clinical Research | Clinical trials, research protocols, and study management | Research Director | Research Systems Team | 12 | 12 | 11 | Beta | Medium |

### Engagement Domains

| Domain ID | Domain Name | Description | Business Owner | Platform Owner | Core Entities | Events | APIs | Maturity | Priority |
|-----------|-------------|-------------|----------------|----------------|---------------|--------|------|----------|----------|
| PATIENT_ENGAGEMENT | Patient Engagement | Patient portal, care plans, health education, and PROs | Chief Patient Experience Officer | Patient Engagement Team | 12 | 12 | 11 | Beta | High |
| TELEHEALTH | Telehealth & Virtual Care | Video visits, remote monitoring, and digital therapeutics | Chief Medical Officer | Telehealth Systems Team | 12 | 11 | 10 | Beta | High |
| NOTIFICATIONS | Notifications & Alerts | Clinical alerts, operational alerts, and multi-channel notifications | Chief Operating Officer | Notification Systems Team | 12 | 10 | 10 | Production | High |
| MESSAGING | Messaging & Communication | Secure messaging, team communication, and collaboration | Chief Operating Officer | Communication Systems Team | 8 | 8 | 8 | Beta | Medium |

### Data & Integration Domains

| Domain ID | Domain Name | Description | Business Owner | Platform Owner | Core Entities | Events | APIs | Maturity | Priority |
|-----------|-------------|-------------|----------------|----------------|---------------|--------|------|----------|----------|
| DOCUMENTS | Document Management | Clinical documents, versioning, access control, and retention | Chief Medical Officer | Document Systems Team | 12 | 10 | 10 | Production | High |
| INTEGRATION | Integration & Interoperability | External system integrations, interface engines, and data exchange | Chief Information Officer | Integration Engineering Team | 12 | 10 | 11 | Production | Critical |
| MASTER_DATA | Master Data Management | Patient, provider, and organization master data | Chief Data Officer | MDM Engineering Team | 10 | 8 | 8 | Beta | High |
| DATA_QUALITY | Data Quality & Governance | Data quality rules, lineage tracking, and governance | Chief Data Officer | Data Quality Team | 8 | 8 | 6 | Beta | Medium |
| MIGRATION | Data Migration | Legacy system migration, data transformation, and validation | Chief Information Officer | Migration Engineering Team | 6 | 6 | 4 | Alpha | Medium |

### Infrastructure & Platform Domains

| Domain ID | Domain Name | Description | Business Owner | Platform Owner | Core Entities | Events | APIs | Maturity | Priority |
|-----------|-------------|-------------|----------------|----------------|---------------|--------|------|----------|----------|
| WORKFLOW | Workflow & Orchestration | Clinical workflows, task management, and process automation | Chief Operating Officer | Workflow Systems Team | 12 | 12 | 10 | Beta | High |
| POLICY | Policy & Compliance | Healthcare policies, clinical guidelines, and regulatory compliance | Chief Compliance Officer | Policy Systems Team | 12 | 10 | 10 | Beta | High |
| PUBLIC_HEALTH | Public Health | Disease surveillance, immunization tracking, and population health | Public Health Director | Public Health Systems Team | 12 | 12 | 10 | Beta | Medium |
| QUALITY_SAFETY | Quality & Patient Safety | Quality metrics, safety event reporting, and performance improvement | Chief Quality Officer | Quality Systems Team | 12 | 12 | 11 | Beta | High |
| CONFIGURATION | Platform Configuration | System settings, feature flags, tenant configuration, and deployment | Chief Technology Officer | Platform Engineering Team | 10 | 7 | 9 | Production | Critical |

---

## Domain Maturity Assessment

### Maturity Levels Definition

| Level | Name | Description | Criteria |
|-------|------|-------------|----------|
| 5 | **Production** | Fully operational, battle-tested | All features complete, SLA met, >99.9% uptime, comprehensive monitoring |
| 4 | **Beta** | Feature-complete, limited production use | Core features complete, performance tested, monitoring in place |
| 3 | **Alpha** | Core features implemented | Basic functionality working, unit tests passing, limited integration |
| 2 | **Development** | Active development in progress | Architecture defined, core entities designed, APIs drafted |
| 1 | **Planning** | Requirements and design phase | Requirements gathered, architecture planned, team assigned |
| 0 | **Concept** | Initial concept and exploration | Business case approved, feasibility assessed, roadmap created |

### Maturity Distribution

| Maturity Level | Count | Percentage | Domains |
|----------------|-------|------------|---------|
| **Production (5)** | 12 | 34% | IDENTITY, AUTHZ, AUDIT, PATIENT, ENCOUNTER, LABORATORY, RADIOLOGY, PHARMACY, HOSPITAL, SCHEDULING, FINANCE, INTEGRATION |
| **Beta (4)** | 18 | 52% | EMERGENCY, BLOOD_BANK, CHRONIC_DISEASE, INVENTORY, SUPPLY_CHAIN, REVENUE_CYCLE, INSURANCE, MEDICAL_DEVICES, ANALYTICS, AI_ML, REPORTING, KNOWLEDGE, RESEARCH, PATIENT_ENGAGEMENT, TELEHEALTH, NOTIFICATIONS, DOCUMENTS, WORKFLOW, POLICY, QUALITY_SAFETY |
| **Alpha (3)** | 3 | 9% | SURGERY, MENTAL_HEALTH, REHABILITATION, HOME_CARE, MIGRATION |
| **Development (2)** | 1 | 3% | MESSAGING |
| **Planning (1)** | 0 | 0% | - |
| **Concept (0)** | 1 | 3% | PUBLIC_HEALTH (Advanced features) |

### Maturity Assessment Criteria

#### Production (Level 5)
- [ ] All planned features implemented and tested
- [ ] SLA defined and consistently met
- [ ] Comprehensive monitoring and alerting
- [ ] Documentation complete (API, operational, user)
- [ ] Security audit passed
- [ ] Performance benchmarks established
- [ ] Disaster recovery tested
- [ ] Training materials available
- [ ] Support runbooks in place
- [ ] Capacity planning documented

#### Beta (Level 4)
- [ ] Core features complete (90%+)
- [ ] Performance testing completed
- [ ] Security review passed
- [ ] API documentation available
- [ ] Monitoring in place
- [ ] Limited production deployment
- [ ] User feedback collected
- [ ] Known issues documented

#### Alpha (Level 3)
- [ ] Core features implemented
- [ ] Unit tests passing
- [ ] Basic integration tests
- [ ] API contracts defined
- [ ] Basic documentation
- [ ] Development environment stable

---

## Domain Priority Matrix

### Priority Levels

| Level | Name | Description | SLA Target |
|-------|------|-------------|------------|
| P0 | **Critical** | Must-have for platform operation | 99.99% uptime, <100ms response |
| P1 | **High** | Important for core business functions | 99.95% uptime, <200ms response |
| P2 | **Medium** | Valuable but not immediately critical | 99.9% uptime, <500ms response |
| P3 | **Low** | Nice-to-have, can be delayed | 99.5% uptime, <1s response |

### Priority Distribution

| Priority | Count | Percentage | Domains |
|----------|-------|------------|---------|
| **P0 - Critical** | 8 | 23% | IDENTITY, AUTHZ, AUDIT, PATIENT, ENCOUNTER, LABORATORY, FINANCE, INTEGRATION |
| **P1 - High** | 18 | 52% | RADIOLOGY, PHARMACY, EMERGENCY, BLOOD_BANK, CHRONIC_DISEASE, HOSPITAL, SCHEDULING, INVENTORY, SUPPLY_CHAIN, REVENUE_CYCLE, INSURANCE, MEDICAL_DEVICES, ANALYTICS, AI_ML, REPORTING, PATIENT_ENGAGEMENT, TELEHEALTH, NOTIFICATIONS |
| **P2 - Medium** | 8 | 23% | MENTAL_HEALTH, REHABILITATION, HOME_CARE, DOCUMENTS, RESEARCH, KNOWLEDGE, MESSAGING, DATA_QUALITY |
| **P3 - Low** | 1 | 3% | PUBLIC_HEALTH (Advanced features) |

### Priority Criteria

#### P0 - Critical (Platform Foundation)
- Platform cannot function without this domain
- All other domains depend on it
- Regulatory/compliance requirement
- Patient safety critical
- Revenue critical

#### P1 - High (Core Business)
- Essential for core business operations
- High user adoption expected
- Significant revenue impact
- Regulatory requirement
- Competitive advantage

#### P2 - Medium (Business Value)
- Important for business efficiency
- Enhances user experience
- Moderate revenue impact
- Operational improvement
- Future competitive advantage

#### P3 - Low (Nice-to-Have)
- Enhances platform capability
- Low immediate business impact
- Future roadmap item
- Limited user demand
- Low resource requirement

---

## Domain Ownership Matrix

### Business Ownership

| Business Owner | Domain Count | Domains |
|----------------|--------------|---------|
| **Chief Information Security Officer** | 2 | IDENTITY, AUTHZ |
| **Chief Compliance Officer** | 2 | AUDIT, POLICY |
| **Chief Medical Officer** | 5 | PATIENT, ENCOUNTER, SURGERY, KNOWLEDGE, DOCUMENTS |
| **Laboratory Director** | 1 | LABORATORY |
| **Radiology Director** | 1 | RADIOLOGY |
| **Chief Pharmacy Officer** | 1 | PHARMACY |
| **Emergency Medicine Director** | 1 | EMERGENCY |
| **Blood Bank Director** | 1 | BLOOD_BANK |
| **Behavioral Health Director** | 1 | MENTAL_HEALTH |
| **Rehabilitation Director** | 1 | REHABILITATION |
| **Population Health Director** | 1 | CHRONIC_DISEASE |
| **Home Health Director** | 1 | HOME_CARE |
| **Chief Operating Officer** | 4 | HOSPITAL, SCHEDULING, NOTIFICATIONS, MESSAGING |
| **Supply Chain Director** | 2 | INVENTORY, SUPPLY_CHAIN |
| **Chief Financial Officer** | 3 | FINANCE, REVENUE_CYCLE, INSURANCE |
| **Biomedical Engineering Director** | 1 | MEDICAL_DEVICES |
| **Chief Data Officer** | 4 | ANALYTICS, AI_ML, REPORTING, MASTER_DATA |
| **Research Director** | 1 | RESEARCH |
| **Chief Patient Experience Officer** | 1 | PATIENT_ENGAGEMENT |
| **Chief Medical Officer (Telehealth)** | 1 | TELEHEALTH |
| **Chief Information Officer** | 2 | INTEGRATION, MIGRATION |
| **Chief Technology Officer** | 1 | CONFIGURATION |
| **Public Health Director** | 1 | PUBLIC_HEALTH |
| **Chief Quality Officer** | 1 | QUALITY_SAFETY |

### Technical Ownership

| Platform Owner (Engineering Team) | Domain Count | Domains |
|-----------------------------------|--------------|---------|
| **Security Engineering Team** | 2 | IDENTITY, AUTHZ |
| **Compliance Engineering Team** | 1 | AUDIT |
| **Clinical Engineering Team** | 2 | PATIENT, ENCOUNTER |
| **Lab Systems Team** | 1 | LABORATORY |
| **Imaging Systems Team** | 1 | RADIOLOGY |
| **Pharmacy Systems Team** | 1 | PHARMACY |
| **ED Systems Team** | 1 | EMERGENCY |
| **Blood Systems Team** | 1 | BLOOD_BANK |
| **Surgical Systems Team** | 1 | SURGERY |
| **Mental Health Systems Team** | 1 | MENTAL_HEALTH |
| **Rehab Systems Team** | 1 | REHABILITATION |
| **Chronic Care Team** | 1 | CHRONIC_DISEASE |
| **Home Care Systems Team** | 1 | HOME_CARE |
| **Operations Engineering Team** | 1 | HOSPITAL |
| **Scheduling Systems Team** | 1 | SCHEDULING |
| **Inventory Systems Team** | 1 | INVENTORY |
| **Supply Chain Systems Team** | 1 | SUPPLY_CHAIN |
| **Finance Systems Team** | 1 | FINANCE |
| **Revenue Cycle Team** | 1 | REVENUE_CYCLE |
| **Payer Relations Team** | 1 | INSURANCE |
| **Device Systems Team** | 1 | MEDICAL_DEVICES |
| **Analytics Engineering Team** | 1 | ANALYTICS |
| **AI Engineering Team** | 1 | AI_ML |
| **Reporting Systems Team** | 1 | REPORTING |
| **Knowledge Systems Team** | 1 | KNOWLEDGE |
| **Research Systems Team** | 1 | RESEARCH |
| **Patient Engagement Team** | 1 | PATIENT_ENGAGEMENT |
| **Telehealth Systems Team** | 1 | TELEHEALTH |
| **Notification Systems Team** | 1 | NOTIFICATIONS |
| **Communication Systems Team** | 1 | MESSAGING |
| **Document Systems Team** | 1 | DOCUMENTS |
| **Integration Engineering Team** | 1 | INTEGRATION |
| **MDM Engineering Team** | 1 | MASTER_DATA |
| **Data Quality Team** | 1 | DATA_QUALITY |
| **Migration Engineering Team** | 1 | MIGRATION |
| **Workflow Systems Team** | 1 | WORKFLOW |
| **Policy Systems Team** | 1 | POLICY |
| **Public Health Systems Team** | 1 | PUBLIC_HEALTH |
| **Quality Systems Team** | 1 | QUALITY_SAFETY |
| **Platform Engineering Team** | 1 | CONFIGURATION |

---

## Domain Statistics Summary

### Entity Distribution by Category

| Category | Total Entities | Avg per Domain | Min | Max |
|----------|----------------|----------------|-----|-----|
| Foundation | 24 | 8 | 6 | 10 |
| Clinical Care | 142 | 12 | 8 | 14 |
| Operational Support | 102 | 13 | 10 | 14 |
| Intelligence & Analytics | 60 | 12 | 10 | 12 |
| Engagement | 44 | 11 | 8 | 12 |
| Data & Integration | 50 | 10 | 6 | 12 |
| Platform Services | 34 | 10 | 10 | 12 |

### Event Distribution by Category

| Category | Total Events | Avg per Domain | Min | Max |
|----------|--------------|----------------|-----|-----|
| Foundation | 24 | 8 | 6 | 10 |
| Clinical Care | 150 | 13 | 10 | 14 |
| Operational Support | 100 | 12 | 10 | 13 |
| Intelligence & Analytics | 52 | 10 | 8 | 12 |
| Engagement | 41 | 10 | 8 | 12 |
| Data & Integration | 42 | 8 | 6 | 10 |
| Platform Services | 43 | 11 | 7 | 12 |

### API Distribution by Category

| Category | Total APIs | Avg per Domain | Min | Max |
|----------|------------|----------------|-----|-----|
| Foundation | 30 | 10 | 8 | 12 |
| Clinical Care | 112 | 9 | 6 | 13 |
| Operational Support | 82 | 10 | 8 | 12 |
| Intelligence & Analytics | 52 | 10 | 6 | 11 |
| Engagement | 36 | 9 | 8 | 11 |
| Data & Integration | 39 | 8 | 4 | 11 |
| Platform Services | 29 | 10 | 9 | 10 |

### Domain Dependency Count

| Domain | Dependencies | Dependents | Critical Path |
|--------|--------------|------------|---------------|
| IDENTITY | 0 | 35 | Yes |
| PATIENT | 1 | 15 | Yes |
| ENCOUNTER | 2 | 12 | Yes |
| ORDERS | 3 | 8 | Yes |
| FINANCE | 4 | 10 | Yes |
| INTEGRATION | 2 | 25 | Yes |
| CONFIGURATION | 0 | 35 | Yes |

### Cross-Domain Event Flows

| Source Domain | Target Domain | Event Count | Flow Direction |
|---------------|---------------|-------------|----------------|
| PATIENT | ENCOUNTER | 8 | Patient → Encounter |
| ENCOUNTER | ORDERS | 6 | Encounter → Orders |
| ORDERS | LABORATORY | 5 | Orders → Laboratory |
| ORDERS | RADIOLOGY | 4 | Orders → Radiology |
| ORDERS | PHARMACY | 5 | Orders → Pharmacy |
| FINANCE | REVENUE_CYCLE | 6 | Finance → Revenue Cycle |
| ANALYTICS | ALL DOMAINS | 20+ | All → Analytics |

---

## Appendix: Domain Quick Reference

### Domain ID Naming Convention

- **Format**: UPPER_SNAKE_CASE
- **Max Length**: 20 characters
- **Pattern**: [AREA]_[SUBAREA] or [AREA]
- **Examples**: `PATIENT`, `BLOOD_BANK`, `AI_ML`

### Domain Status Values

| Status | Description |
|--------|-------------|
| Active | Domain is operational and maintained |
| Deprecated | Domain is scheduled for removal |
| Merged | Domain has been merged into another |
| Archived | Domain is no longer actively developed |

### Domain Contact Information

Each domain should maintain:
- **Business Owner**: Executive sponsor
- **Product Owner**: Day-to-day decision maker
- **Technical Lead**: Architecture and design authority
- **Scrum Master/PM**: Delivery management
- **On-Call Contact**: 24/7 operational support

---

**Document Classification:** CANONICAL CATALOG  
**Review Cycle:** Monthly  
**Next Review Date:** 2026-07-25  
**Approved By:** NHDOS Architecture Board