# MASTER DATA MODEL

**NHDOS Platform-Core — Master Data Entity Model**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Citizen Master

```json
{
  "entity": "CitizenMaster",
  "domain": "citizen",
  "fields": {
    "id": {"type": "uuid", "primary": true},
    "national_id": {"type": "string", "unique": true, "indexed": true},
    "given_name": {"type": "string", "required": true},
    "family_name": {"type": "string", "required": true},
    "date_of_birth": {"type": "date", "required": true},
    "gender": {"type": "enum", "values": ["male", "female"]},
    "blood_type": {"type": "enum", "values": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]},
    "phone": {"type": "string", "encrypted": true},
    "email": {"type": "string", "encrypted": true},
    "address": {"type": "object", "encrypted": true},
    "governorate_code": {"type": "string", "reference": "location"},
    "district_code": {"type": "string", "reference": "location"},
    "status": {"type": "enum", "values": ["active", "inactive", "deceased", "suspended"]},
    "golden_record_id": {"type": "uuid", "reference": "golden_record"},
    "confidentiality_level": {"type": "integer", "default": 5}
  }
}
```

---

## 2. Patient Master

```json
{
  "entity": "PatientMaster",
  "domain": "healthcare_core",
  "fields": {
    "id": {"type": "uuid", "primary": true},
    "citizen_id": {"type": "uuid", "reference": "citizen_master"},
    "medical_record_number": {"type": "string", "unique": true},
    "facility_id": {"type": "uuid", "reference": "facility_master"},
    "primary_care_provider_id": {"type": "uuid", "reference": "professional_master"},
    "blood_type": {"type": "enum"},
    "allergies": {"type": "array", "items": "string"},
    "chronic_conditions": {"type": "array", "items": "string"},
    "emergency_contact": {"type": "object"},
    "insurance_id": {"type": "uuid", "reference": "insurance_master"},
    "status": {"type": "enum", "values": ["active", "inactive", "deceased"]},
    "golden_record_id": {"type": "uuid", "reference": "golden_record"}
  }
}
```

---

## 3. Professional Master

```json
{
  "entity": "ProfessionalMaster",
  "domain": "human_resources",
  "fields": {
    "id": {"type": "uuid", "primary": true},
    "citizen_id": {"type": "uuid", "reference": "citizen_master"},
    "professional_type": {"type": "enum", "values": ["physician", "nurse", "pharmacist", "technician", "administrator"]},
    "specialty": {"type": "string"},
    "license_number": {"type": "string", "unique": true},
    "license_expiry": {"type": "date"},
    "facility_id": {"type": "uuid", "reference": "facility_master"},
    "department_id": {"type": "uuid", "reference": "department"},
    "status": {"type": "enum", "values": ["active", "inactive", "suspended", "retired"]},
    "golden_record_id": {"type": "uuid", "reference": "golden_record"}
  }
}
```

---

## 4. Organization Master

```json
{
  "entity": "OrganizationMaster",
  "domain": "human_resources",
  "fields": {
    "id": {"type": "uuid", "primary": true},
    "name": {"type": "string", "required": true},
    "organization_type": {"type": "enum", "values": ["ministry", "directorate", "hospital", "clinic", "laboratory", "pharmacy", "insurance"]},
    "parent_organization_id": {"type": "uuid", "reference": "organization_master"},
    "registration_number": {"type": "string", "unique": true},
    "tax_number": {"type": "string"},
    "address": {"type": "object"},
    "phone": {"type": "string"},
    "email": {"type": "string"},
    "status": {"type": "enum", "values": ["active", "inactive", "suspended"]},
    "golden_record_id": {"type": "uuid", "reference": "golden_record"}
  }
}
```

---

## 5. Facility Master

```json
{
  "entity": "FacilityMaster",
  "domain": "human_resources",
  "fields": {
    "id": {"type": "uuid", "primary": true},
    "organization_id": {"type": "uuid", "reference": "organization_master"},
    "name": {"type": "string", "required": true},
    "facility_type": {"type": "enum", "values": ["hospital", "clinic", "laboratory", "pharmacy", "blood_bank", "radiology_center"]},
    "facility_code": {"type": "string", "unique": true},
    "address": {"type": "object"},
    "phone": {"type": "string"},
    "email": {"type": "string"},
    "capacity": {"type": "integer"},
    "beds_count": {"type": "integer"},
    "departments": {"type": "array", "items": "uuid"},
    "status": {"type": "enum", "values": ["active", "inactive", "under_construction"]},
    "golden_record_id": {"type": "uuid", "reference": "golden_record"}
  }
}
```

---

## 6. Laboratory Master

```json
{
  "entity": "LaboratoryMaster",
  "domain": "laboratory",
  "fields": {
    "id": {"type": "uuid", "primary": true},
    "facility_id": {"type": "uuid", "reference": "facility_master"},
    "name": {"type": "string", "required": true},
    "laboratory_type": {"type": "enum", "values": ["clinical", "pathology", "microbiology", "blood_bank", "radiology"]},
    "accreditation": {"type": "object"},
    "capacity": {"type": "integer"},
    "equipment": {"type": "array", "items": "uuid"},
    "status": {"type": "enum", "values": ["active", "inactive", "suspended"]},
    "golden_record_id": {"type": "uuid", "reference": "golden_record"}
  }
}
```

---

## 7. Medical Device Master

```json
{
  "entity": "MedicalDeviceMaster",
  "domain": "medical_devices",
  "fields": {
    "id": {"type": "uuid", "primary": true},
    "device_type": {"type": "string", "required": true},
    "manufacturer": {"type": "string", "required": true},
    "model": {"type": "string", "required": true},
    "serial_number": {"type": "string", "unique": true},
    "facility_id": {"type": "uuid", "reference": "facility_master"},
    "department_id": {"type": "uuid", "reference": "department"},
    "location": {"type": "string"},
    "calibration_due": {"type": "date"},
    "maintenance_due": {"type": "date"},
    "status": {"type": "enum", "values": ["active", "inactive", "maintenance", "decommissioned"]},
    "golden_record_id": {"type": "uuid", "reference": "golden_record"}
  }
}
```

---

## 8. Medication Master

```json
{
  "entity": "MedicationMaster",
  "domain": "pharmacy",
  "fields": {
    "id": {"type": "uuid", "primary": true},
    "name": {"type": "string", "required": true},
    "generic_name": {"type": "string"},
    "manufacturer": {"type": "string", "required": true},
    "ndc_code": {"type": "string", "unique": true},
    "atc_code": {"type": "string", "reference": "terminology"},
    "dosage_form": {"type": "enum", "values": ["tablet", "capsule", "liquid", "injection", "inhaler", "cream", "suppository"]},
    "strength": {"type": "string"},
    "controlled_substance": {"type": "boolean", "default": false},
    "storage_conditions": {"type": "string"},
    "expiry_date": {"type": "date"},
    "status": {"type": "enum", "values": ["active", "inactive", "recalled", "expired"]},
    "golden_record_id": {"type": "uuid", "reference": "golden_record"}
  }
}
```

---

## 9. Reference Organization Master

```json
{
  "entity": "ReferenceOrganizationMaster",
  "domain": "human_resources",
  "fields": {
    "id": {"type": "uuid", "primary": true},
    "name": {"type": "string", "required": true},
    "organization_type": {"type": "string"},
    "parent_id": {"type": "uuid", "reference": "reference_organization_master"},
    "code": {"type": "string", "unique": true},
    "level": {"type": "integer"},
    "path": {"type": "string"},
    "status": {"type": "enum", "values": ["active", "inactive"]},
    "golden_record_id": {"type": "uuid", "reference": "golden_record"}
  }
}
```

---

## 10. Location Master

```json
{
  "entity": "LocationMaster",
  "domain": "geography",
  "fields": {
    "id": {"type": "uuid", "primary": true},
    "name": {"type": "string", "required": true},
    "location_type": {"type": "enum", "values": ["country", "governorate", "district", "city", "village"]},
    "parent_id": {"type": "uuid", "reference": "location_master"},
    "code": {"type": "string", "unique": true},
    "iso_code": {"type": "string"},
    "latitude": {"type": "decimal"},
    "longitude": {"type": "decimal"},
    "population": {"type": "integer"},
    "status": {"type": "enum", "values": ["active", "inactive"]}
  }
}
```

---

## 11. Insurance Master

```json
{
  "entity": "InsuranceMaster",
  "domain": "financial",
  "fields": {
    "id": {"type": "uuid", "primary": true},
    "provider_name": {"type": "string", "required": true},
    "provider_type": {"type": "enum", "values": ["government", "private", "mixed"]},
    "license_number": {"type": "string", "unique": true},
    "coverage_types": {"type": "array", "items": "string"},
    "contact": {"type": "object"},
    "status": {"type": "enum", "values": ["active", "inactive", "suspended"]},
    "golden_record_id": {"type": "uuid", "reference": "golden_record"}
  }
}
```

---

## 12. Golden Record

```json
{
  "entity": "GoldenRecord",
  "domain": "master_data",
  "fields": {
    "id": {"type": "uuid", "primary": true},
    "domain": {"type": "string", "required": true},
    "entity_type": {"type": "string", "required": true},
    "source_records": {"type": "array", "items": "uuid"},
    "resolved_data": {"type": "object"},
    "confidence_score": {"type": "decimal"},
    "resolution_method": {"type": "enum", "values": ["deterministic", "probabilistic", "fuzzy", "manual"]},
    "created_at": {"type": "datetime"},
    "updated_at": {"type": "datetime"},
    "status": {"type": "enum", "values": ["active", "merged", "deleted"]}
  }
}
```

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
