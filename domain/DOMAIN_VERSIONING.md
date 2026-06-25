# DOMAIN VERSIONING — NATIONAL HEALTHCARE DIGITAL OPERATING SYSTEM

**Document**: Canonical Versioning Model
**Version**: 1.0.0
**Date**: 2026-06-25
**Status**: ACTIVE
**Constitution Reference**: Articles IV, VII, XII, XVI

---

## 1. OVERVIEW

This document defines the comprehensive versioning model for all entities, APIs, events, and schemas in the NHDOS. Consistent versioning ensures backward compatibility, smooth migrations, and predictable evolution of the platform.

**Core Principles**:
- All versioned artifacts follow Semantic Versioning 2.0.0
- Breaking changes require major version bumps
- Backward compatibility is maintained within major versions
- Deprecation periods provide migration time
- Version history is maintained for traceability

---

## 2. VERSIONING STRATEGY

### 2.1 Semantic Versioning (SemVer 2.0.0)

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

MAJOR: Breaking changes (incompatible API changes)
MINOR: New features (backward compatible)
PATCH: Bug fixes (backward compatible)
PRERELEASE: alpha.1, beta.1, rc.1
BUILD: build metadata
```

### 2.2 Version Bump Rules

| Change Type | Version Bump | Example | Rationale |
|-------------|-------------|---------|-----------|
| Removing field | MAJOR | 1.0.0 → 2.0.0 | Breaking change |
| Renaming field | MAJOR | 1.0.0 → 2.0.0 | Breaking change |
| Changing field type | MAJOR | 1.0.0 → 2.0.0 | Breaking change |
| Adding required field | MAJOR | 1.0.0 → 2.0.0 | Breaking change |
| Removing endpoint | MAJOR | 1.0.0 → 2.0.0 | Breaking change |
| Changing response structure | MAJOR | 1.0.0 → 2.0.0 | Breaking change |
| Adding optional field | MINOR | 1.0.0 → 1.1.0 | Backward compatible |
| Adding new endpoint | MINOR | 1.0.0 → 1.1.0 | Backward compatible |
| Adding new enum value | MINOR | 1.0.0 → 1.1.0 | Backward compatible |
| Increasing rate limit | MINOR | 1.0.0 → 1.1.0 | Backward compatible |
| Fixing bug | PATCH | 1.0.0 → 1.0.1 | Backward compatible |
| Documentation update | PATCH | 1.0.0 → 1.0.1 | No code change |
| Dependency update | PATCH | 1.0.0 → 1.0.1 | No API change |

---

## 3. ENTITY VERSIONING

### 3.1 Entity Version Field

Every versioned entity includes:

```json
{
  "id": "entity-uuid",
  "version": "2.1.0",
  "versionMetadata": {
    "majorVersion": 2,
    "minorVersion": 1,
    "patchVersion": 0,
    "lastVersionedAt": "2026-06-25T10:00:00Z",
    "lastVersionedBy": "user-uuid",
    "changelog": [
      {"type": "added", "description": "New field 'department'"},
      {"type": "changed", "description': "Improved validation rules"}
    ]
  }
}
```

### 3.2 Entity Version Tracking

```python
class EntityVersionManager:
    def __init__(self):
        self.version_history = {}
    
    def increment_version(self, entity: dict, change_type: str, 
                          description: str) -> dict:
        """Increment entity version based on change type."""
        current_version = entity.get("version", "1.0.0")
        major, minor, patch = self.parse_version(current_version)
        
        if change_type == "breaking":
            major += 1
            minor = 0
            patch = 0
        elif change_type == "feature":
            minor += 1
            patch = 0
        elif change_type == "fix":
            patch += 1
        else:
            raise ValueError(f"Unknown change type: {change_type}")
        
        new_version = f"{major}.{minor}.{patch}"
        
        # Update entity
        entity["version"] = new_version
        entity["versionMetadata"] = {
            "majorVersion": major,
            "minorVersion": minor,
            "patchVersion": patch,
            "lastVersionedAt": datetime.now(timezone.utc).isoformat(),
            "changelog": [{"type": change_type, "description": description}]
        }
        
        # Track history
        self.track_version(entity["id"], new_version, change_type, description)
        
        return entity
    
    def parse_version(self, version: str) -> tuple:
        """Parse semantic version string."""
        parts = version.split(".")
        return int(parts[0]), int(parts[1]), int(parts[2])
    
    def track_version(self, entity_id: str, version: str, 
                      change_type: str, description: str):
        """Track version history."""
        if entity_id not in self.version_history:
            self.version_history[entity_id] = []
        
        self.version_history[entity_id].append({
            "version": version,
            "changeType": change_type,
            "description": description,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
```

### 3.3 Entity-Specific Versioning

#### 3.3.1 Patient Entity Versioning

| Change | Type | Version Bump | Example |
|--------|------|-------------|---------|
| Remove field | Breaking | MAJOR | Remove `maidenName` |
| Rename field | Breaking | MAJOR | `name` → `fullName` |
| Change field type | Breaking | MAJOR | `age` (int) → `dateOfBirth` (date) |
| Add required field | Breaking | MAJOR | Add `nationalId` |
| Add optional field | Feature | MINOR | Add `email` |
| Add enum value | Feature | MINOR | Add `gender: other` |
| Fix validation | Fix | PATCH | Fix date format |

#### 3.3.2 Sample Entity Versioning

| Change | Type | Version Bump | Example |
|--------|------|-------------|---------|
| Remove field | Breaking | MAJOR | Remove `collectionSite` |
| Change status values | Breaking | MAJOR | Rename `pending` → `awaiting` |
| Add optional field | Feature | MINOR | Add `specialInstructions` |
| Fix calculation | Fix | PATCH | Fix volume calculation |

#### 3.3.3 Test Result Entity Versioning

| Change | Type | Version Bump | Example |
|--------|------|-------------|---------|
| Remove analyte | Breaking | MAJOR | Remove `hemoglobin` |
| Change result structure | Breaking | MAJOR | Restructure `results` array |
| Add optional analyte | Feature | MINOR | Add `CRP` |
| Fix reference range | Fix | PATCH | Correct WBC range |

---

## 4. BACKWARD COMPATIBILITY RULES

### 4.1 Compatibility Matrix

| Change | Backward Compatible | Forward Compatible | Migration Required |
|--------|--------------------|--------------------|-------------------|
| Add optional field | Yes | No | No |
| Add required field | No | No | Yes |
| Remove optional field | No | Yes | Recommended |
| Remove required field | No | No | Yes |
| Rename field | No | No | Yes |
| Change field type | No | No | Yes |
| Add enum value | Yes | No | Recommended |
| Remove enum value | No | No | Yes |
| Add endpoint | Yes | No | No |
| Remove endpoint | No | No | Yes |
| Change response structure | No | No | Yes |

### 4.2 Backward Compatibility Rules

```python
class BackwardCompatibilityChecker:
    def check_compatibility(self, old_schema: dict, new_schema: dict) -> dict:
        """Check if new schema is backward compatible."""
        issues = []
        
        # Check for removed fields
        old_fields = set(old_schema.get("properties", {}).keys())
        new_fields = set(new_schema.get("properties", {}).keys())
        
        removed_fields = old_fields - new_fields
        for field in removed_fields:
            issues.append({
                "type": "removed_field",
                "field": field,
                "severity": "breaking",
                "migration": "Required"
            })
        
        # Check for type changes
        for field in old_fields & new_fields:
            old_type = old_schema["properties"][field].get("type")
            new_type = new_schema["properties"][field].get("type")
            
            if old_type != new_type:
                issues.append({
                    "type": "type_changed",
                    "field": field,
                    "oldType": old_type,
                    "newType": new_type,
                    "severity": "breaking",
                    "migration": "Required"
                })
        
        # Check for new required fields
        old_required = set(old_schema.get("required", []))
        new_required = set(new_schema.get("required", []))
        
        new_required_fields = new_required - old_required
        for field in new_required_fields:
            issues.append({
                "type": "new_required_field",
                "field": field,
                "severity": "breaking",
                "migration": "Required"
            })
        
        # Check for removed enum values
        for field in old_fields & new_fields:
            old_enum = set(old_schema["properties"][field].get("enum", []))
            new_enum = set(new_schema["properties"][field].get("enum", []))
            
            removed_enum = old_enum - new_enum
            if removed_enum:
                issues.append({
                    "type": "removed_enum_value",
                    "field": field,
                    "values": list(removed_enum),
                    "severity": "breaking",
                    "migration": "Required"
                })
        
        is_compatible = len([i for i in issues if i["severity"] == "breaking"]) == 0
        
        return {
            "compatible": is_compatible,
            "issues": issues,
            "requiresMigration": not is_compatible
        }
```

### 4.3 Forward Compatibility Rules

```python
class ForwardCompatibilityChecker:
    def check_forward_compatibility(self, old_schema: dict, new_schema: dict) -> dict:
        """Check if old clients can handle new schema."""
        issues = []
        
        old_fields = set(old_schema.get("properties", {}).keys())
        new_fields = set(new_schema.get("properties", {}).keys())
        
        # New fields should be optional
        new_required = set(new_schema.get("required", []))
        new_required_fields = new_required - old_fields
        
        for field in new_required_fields:
            issues.append({
                "type": "new_required_field",
                "field": field,
                "severity": "breaking",
                "impact": "Old clients cannot process new responses"
            })
        
        is_compatible = len(issues) == 0
        
        return {
            "compatible": is_compatible,
            "issues": issues
        }
```

---

## 5. MIGRATION RULES

### 5.1 Migration Strategy

```
Version N (Current) → Version N+1 (New)
       │                      │
       │    ┌─────────────────┤
       │    │                 │
       ▼    ▼                 ▼
   ┌─────────────┐    ┌─────────────┐
   │  Deprecation │    │  Migration  │
   │   Period     │    │   Period    │
   │ (12 months)  │    │ (6 months)  │
   └─────────────┘    └─────────────┘
```

### 5.2 Migration Types

| Migration Type | Description | Complexity | Downtime |
|---------------|-------------|------------|----------|
| Non-breaking | Add optional fields | Low | None |
| Breaking (additive) | Add required fields with defaults | Medium | None |
| Breaking (structural) | Restructure entity | High | Minimal |
| Breaking (removal) | Remove deprecated fields | Medium | None |
| Data migration | Transform existing data | High | Minimal |

### 5.3 Migration Process

```python
class EntityMigrationManager:
    def __init__(self):
        self.migrations = {}
    
    def register_migration(self, entity_type: str, from_version: str, 
                           to_version: str, migration_fn: callable):
        """Register a migration function."""
        key = f"{entity_type}:{from_version}:{to_version}"
        self.migrations[key] = migration_fn
    
    def migrate(self, entity: dict, target_version: str) -> dict:
        """Migrate entity to target version."""
        current_version = entity.get("version", "1.0.0")
        
        if current_version == target_version:
            return entity
        
        # Get migration path
        migration_path = self.get_migration_path(
            entity["type"], current_version, target_version
        )
        
        migrated_entity = entity.copy()
        for step in migration_path:
            migration_key = f"{entity['type']}:{step['from']}:{step['to']}"
            migration_fn = self.migrations.get(migration_key)
            
            if migration_fn:
                migrated_entity = migration_fn(migrated_entity)
                migrated_entity["version"] = step["to"]
            else:
                raise MigrationError(f"No migration found: {migration_key}")
        
        return migrated_entity
    
    def get_migration_path(self, entity_type: str, from_version: str, 
                           to_version: str) -> list:
        """Get migration path between versions."""
        # Implementation would use graph traversal to find shortest path
        return [
            {"from": from_version, "to": to_version}
        ]
```

### 5.4 Migration Example

```python
# Migration from Patient v1.0.0 to v2.0.0
def migrate_patient_v1_to_v2(patient: dict) -> dict:
    """Migrate patient from v1.0.0 to v2.0.0."""
    
    # v1.0.0 → v2.0.0 changes:
    # - Renamed field: name → fullName (MAJOR)
    # - Added required field: nationalId (MAJOR)
    # - Added optional field: email (MINOR)
    
    migrated = patient.copy()
    
    # Handle renamed field
    if "name" in migrated:
        migrated["fullName"] = migrated.pop("name")
    
    # Add default for new required field (if not present)
    if "nationalId" not in migrated:
        migrated["nationalId"] = f"PENDING-{migrated['id'][:8]}"
    
    # Add default for new optional field
    if "email" not in migrated:
        migrated["email"] = None
    
    # Update version
    migrated["version"] = "2.0.0"
    migrated["versionMetadata"] = {
        "migratedFrom": "1.0.0",
        "migratedAt": datetime.now(timezone.utc).isoformat(),
        "migrationVersion": "patient-v1-to-v2"
    }
    
    return migrated
```

---

## 6. SCHEMA EVOLUTION

### 6.1 Schema Versioning

```python
class SchemaVersionManager:
    def __init__(self):
        self.schemas = {}
        self.schema_history = {}
    
    def register_schema(self, entity_type: str, version: str, schema: dict):
        """Register a schema version."""
        key = f"{entity_type}:{version}"
        self.schemas[key] = schema
        
        if entity_type not in self.schema_history:
            self.schema_history[entity_type] = []
        
        self.schema_history[entity_type].append({
            "version": version,
            "registeredAt": datetime.now(timezone.utc).isoformat(),
            "schema": schema
        })
    
    def get_compatible_schemas(self, entity_type: str, version: str) -> list:
        """Get all schema versions compatible with the given version."""
        major_version = int(version.split(".")[0])
        compatible = []
        
        for v in self.schema_history.get(entity_type, []):
            v_major = int(v["version"].split(".")[0])
            if v_major == major_version:
                compatible.append(v["version"])
        
        return compatible
    
    def validate_against_schema(self, entity: dict, schema_version: str = None) -> dict:
        """Validate entity against schema."""
        entity_type = entity.get("type", entity.get("entityType"))
        version = schema_version or entity.get("version", "1.0.0")
        
        key = f"{entity_type}:{version}"
        schema = self.schemas.get(key)
        
        if not schema:
            return {"valid": False, "error": f"Schema not found: {key}"}
        
        # Validate against schema
        errors = self.validate_json_schema(entity, schema)
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "schemaVersion": version
        }
```

### 6.2 Schema Evolution Rules

| Evolution | Strategy | Example |
|-----------|----------|---------|
| Add optional property | Add to schema with default | Add `email: string \| null` |
| Add required property | Add with migration | Add `nationalId: string` |
| Remove property | Deprecate first | Mark as deprecated, remove in next major |
| Change property type | New version | `age: number` → `dateOfBirth: string` |
| Restructure | New version | Flatten nested object |
| Rename property | New version | `name` → `fullName` |

### 6.3 Schema Compatibility Validation

```python
class SchemaCompatibilityValidator:
    def validate_backward_compatibility(self, old_schema: dict, new_schema: dict) -> dict:
        """Validate backward compatibility of schema changes."""
        issues = []
        
        old_props = old_schema.get("properties", {})
        new_props = new_schema.get("properties", {})
        
        # Check for removed properties
        for prop in old_props:
            if prop not in new_props:
                issues.append({
                    "type": "removed_property",
                    "property": prop,
                    "severity": "breaking"
                })
        
        # Check for type changes
        for prop in old_props:
            if prop in new_props:
                old_type = old_props[prop].get("type")
                new_type = new_props[prop].get("type")
                if old_type != new_type:
                    issues.append({
                        "type": "type_changed",
                        "property": prop,
                        "oldType": old_type,
                        "newType": new_type,
                        "severity": "breaking"
                    })
        
        # Check for new required properties
        old_required = set(old_schema.get("required", []))
        new_required = set(new_schema.get("required", []))
        for prop in new_required - old_required:
            issues.append({
                "type": "new_required_property",
                "property": prop,
                "severity": "breaking"
            })
        
        return {
            "compatible": len([i for i in issues if i["severity"] == "breaking"]) == 0,
            "issues": issues
        }
```

---

## 7. API VERSIONING

### 7.1 API Version Lifecycle

```
v1 (current) → v2 (developing) → v1 (deprecated) → v1 (removed)
                    │                    │
                    │    12-month window │
                    └────────────────────┘
```

### 7.2 API Versioning Strategy

| Strategy | Convention | Example |
|----------|-----------|---------|
| URL Path | `/api/v{N}/` | `/api/v1/patients` |
| Header | `Accept: application/vnd.nhdos.v1+json` | — |
| Query Parameter | `?version=v1` | `?version=v1` |

**Preferred**: URL path versioning for simplicity and cacheability.

### 7.3 API Version Header

```json
{
  "X-API-Version": "v1",
  "X-API-Deprecated": false,
  "X-API-Sunset": null,
  "X-API-Documentation": "https://api.nhdos.gov/docs/v1"
}
```

### 7.4 API Deprecation Headers

```json
{
  "Deprecation": "true",
  "Sunset": "Sat, 25 Jun 2027 00:00:00 GMT",
  "Link": "<https://api.nhdos.gov/docs/v2>; rel=\"successor-version\""
}
```

### 7.5 API Version Migration

```python
class APIVersionManager:
    def __init__(self):
        self.versions = {}
        self.deprecated_versions = {}
    
    def register_version(self, version: str, status: str = "current"):
        """Register API version."""
        self.versions[version] = {
            "status": status,
            "registeredAt": datetime.now(timezone.utc).isoformat(),
            "sunsetDate": None
        }
    
    def deprecate_version(self, version: str, sunset_date: str):
        """Deprecate API version."""
        if version in self.versions:
            self.versions[version]["status"] = "deprecated"
            self.versions[version]["sunsetDate"] = sunset_date
            
            self.deprecated_versions[version] = self.versions[version]
    
    def remove_version(self, version: str):
        """Remove deprecated API version."""
        if version in self.deprecated_versions:
            del self.versions[version]
            del self.deprecated_versions[version]
    
    def get_version_info(self, version: str) -> dict:
        """Get version information."""
        return self.versions.get(version, {"status": "unknown"})
    
    def is_version_supported(self, version: str) -> bool:
        """Check if version is supported."""
        version_info = self.versions.get(version)
        return version_info is not None and version_info["status"] != "removed"
```

### 7.6 Multi-Version Support

```python
class MultiVersionAPIRouter:
    def __init__(self):
        self.routers = {}
    
    def add_version(self, version: str, router):
        """Add router for API version."""
        self.routers[version] = router
    
    def get_handler(self, version: str, path: str):
        """Get handler for specific version."""
        router = self.routers.get(version)
        if router:
            return router.get_handler(path)
        return None
    
    def redirect_to_latest(self, request) -> str:
        """Redirect request to latest version."""
        latest_version = self.get_latest_version()
        return f"/api/{latest_version}{request.path}"
    
    def get_latest_version(self) -> str:
        """Get latest API version."""
        supported = [v for v, info in self.versions.items() 
                    if info["status"] == "current"]
        return max(supported) if supported else "v1"
```

---

## 8. EVENT VERSIONING

### 8.1 Event Schema Versioning

```json
{
  "event": {
    "type": "patient.admitted",
    "version": "2.0.0",
    "schema": {
      "$ref": "schemas/patient-admitted-v2.0.0.json"
    }
  }
}
```

### 8.2 Event Versioning Rules

| Change | Version Bump | Backward Compatible |
|--------|-------------|---------------------|
| Add optional field | MINOR | Yes |
| Add required field | MAJOR | No |
| Remove field | MAJOR | No |
| Rename field | MAJOR | No |
| Change field type | MAJOR | No |
| Change event name | MAJOR | No |

### 8.3 Event Schema Evolution

```python
class EventSchemaVersionManager:
    def __init__(self):
        self.event_schemas = {}
        self.schema_compatibility = {}
    
    def register_event_schema(self, event_type: str, version: str, schema: dict):
        """Register event schema."""
        key = f"{event_type}:{version}"
        self.event_schemas[key] = schema
        
        # Check compatibility with previous version
        prev_version = self.get_previous_version(event_type, version)
        if prev_version:
            compatibility = self.check_event_compatibility(
                event_type, prev_version, version
            )
            self.schema_compatibility[key] = compatibility
    
    def check_event_compatibility(self, event_type: str, 
                                   old_version: str, new_version: str) -> dict:
        """Check event schema compatibility."""
        old_schema = self.event_schemas.get(f"{event_type}:{old_version}")
        new_schema = self.event_schemas.get(f"{event_type}:{new_version}")
        
        if not old_schema or not new_schema:
            return {"compatible": True, "reason": "No previous schema"}
        
        # Check for breaking changes
        issues = []
        
        old_props = old_schema.get("properties", {})
        new_props = new_schema.get("properties", {})
        
        # Removed fields
        for prop in old_props:
            if prop not in new_props:
                issues.append(f"Removed field: {prop}")
        
        # Type changes
        for prop in old_props:
            if prop in new_props:
                if old_props[prop].get("type") != new_props[prop].get("type"):
                    issues.append(f"Type changed: {prop}")
        
        return {
            "compatible": len(issues) == 0,
            "issues": issues
        }
```

### 8.4 Event Consumer Versioning

```python
class EventConsumerVersionManager:
    def __init__(self):
        self.consumer_versions = {}
    
    def register_consumer(self, consumer_id: str, event_type: str, 
                          min_version: str, max_version: str):
        """Register event consumer with version constraints."""
        self.consumer_versions[consumer_id] = {
            "eventType": event_type,
            "minVersion": min_version,
            "maxVersion": max_version,
            "registeredAt": datetime.now(timezone.utc).isoformat()
        }
    
    def can_consume(self, consumer_id: str, event_type: str, 
                    event_version: str) -> bool:
        """Check if consumer can handle event version."""
        consumer = self.consumer_versions.get(consumer_id)
        if not consumer:
            return False
        
        if consumer["eventType"] != event_type:
            return False
        
        return (consumer["minVersion"] <= event_version <= consumer["maxVersion"])
    
    def get_compatible_consumers(self, event_type: str, 
                                  event_version: str) -> list:
        """Get all consumers compatible with event version."""
        compatible = []
        
        for consumer_id, consumer in self.consumer_versions.items():
            if self.can_consume(consumer_id, event_type, event_version):
                compatible.append(consumer_id)
        
        return compatible
```

---

## 9. SDK VERSIONING

### 9.1 SDK Version Strategy

| SDK | Versioning | Compatibility |
|-----|-----------|---------------|
| Python SDK | SemVer | Compatible with API v{N} |
| TypeScript SDK | SemVer | Compatible with API v{N} |
| CLI | SemVer | Compatible with Platform-Core v{N} |

### 9.2 SDK Compatibility Matrix

| SDK Version | API Version | Platform-Core Version | Status |
|-------------|-------------|----------------------|--------|
| 1.x.x | v1 | 2.x.x | Current |
| 2.x.x | v2 | 3.x.x | Developing |
| 0.x.x | v1 | 1.x.x | Deprecated |

### 9.3 SDK Version Negotiation

```python
class SDKVersionNegotiator:
    def __init__(self):
        self.supported_versions = {}
    
    def register_sdk_version(self, sdk_type: str, sdk_version: str, 
                              api_version: str, platform_version: str):
        """Register SDK version compatibility."""
        key = f"{sdk_type}:{sdk_version}"
        self.supported_versions[key] = {
            "apiVersion": api_version,
            "platformVersion": platform_version,
            "registeredAt": datetime.now(timezone.utc).isoformat()
        }
    
    def negotiate_version(self, sdk_type: str, client_version: str, 
                          server_versions: dict) -> dict:
        """Negotiate compatible version."""
        # Find compatible SDK version
        compatible_sdk = None
        for key, info in self.supported_versions.items():
            if key.startswith(f"{sdk_type}:"):
                sdk_version = key.split(":")[1]
                if self.is_version_compatible(sdk_version, client_version):
                    compatible_sdk = info
                    break
        
        if not compatible_sdk:
            return {"compatible": False, "reason": "No compatible SDK version"}
        
        # Find compatible server version
        compatible_api = compatible_sdk["apiVersion"]
        if compatible_api in server_versions.get("apiVersions", []):
            return {
                "compatible": True,
                "sdkVersion": client_version,
                "apiVersion": compatible_api,
                "platformVersion": compatible_sdk["platformVersion"]
            }
        
        return {"compatible": False, "reason": "No compatible server version"}
```

---

## 10. VERSION CONTROL WORKFLOW

### 10.1 Version Branching Strategy

```
main (production)
├── develop (integration)
│   ├── feature/v2-new-feature
│   ├── feature/v2-another-feature
│   └── bugfix/v1-bug-fix
├── release/v2.0.0
└── hotfix/v1.0.1
```

### 10.2 Version Release Process

```
1. Feature Development
   └── Create feature branch
   └── Implement changes
   └── Add tests
   └── Update documentation
   └── Create PR

2. Integration
   └── Merge to develop
   └── Run integration tests
   └── Update version number

3. Release Candidate
   └── Create release branch
   └── Run full test suite
   └── Security scan
   └── Performance test

4. Release
   └── Merge to main
   └── Tag release
   └── Update changelog
   └── Deploy to production

5. Deprecation
   └── Mark old version as deprecated
   └── Add deprecation headers
   └── Notify consumers
   └── Monitor usage
```

### 10.3 Version Release Checklist

```python
class VersionReleaseChecklist:
    def __init__(self):
        self.checklist = []
    
    def generate_checklist(self, version: str, change_type: str) -> list:
        """Generate release checklist."""
        checklist = [
            {"item": "Update version number", "required": True},
            {"item": "Update CHANGELOG.md", "required": True},
            {"item": "Run full test suite", "required": True},
            {"item": "Run security scan", "required": True},
            {"item": "Update API documentation", "required": True},
            {"item": "Update SDK compatibility matrix", "required": True},
            {"item": "Notify consumers of deprecation", "required": change_type == "breaking"},
            {"item": "Update migration guide", "required": change_type == "breaking"},
            {"item": "Performance benchmark", "required": True},
            {"item": "Load test", "required": version.startswith("2.")},
            {"item": "Security audit", "required": version.startswith("2.")},
            {"item": "Compliance review", "required": True},
        ]
        
        return checklist
    
    def verify_checklist(self, checklist: list) -> dict:
        """Verify checklist completion."""
        required_items = [item for item in checklist if item["required"]]
        completed_items = [item for item in checklist if item.get("completed")]
        
        return {
            "total": len(checklist),
            "required": len(required_items),
            "completed": len(completed_items),
            "allRequiredComplete": all(
                item.get("completed") for item in required_items
            ),
            "missing": [
                item for item in required_items 
                if not item.get("completed")
            ]
        }
```

---

## 11. VERSION MONITORING

### 11.1 Version Usage Metrics

```python
class VersionMetricsCollector:
    def __init__(self):
        self.metrics = {}
    
    def record_request(self, api_version: str, endpoint: str, 
                       status_code: int, response_time: float):
        """Record API request metrics."""
        key = f"{api_version}:{endpoint}"
        
        if key not in self.metrics:
            self.metrics[key] = {
                "totalRequests": 0,
                "successfulRequests": 0,
                "failedRequests": 0,
                "averageResponseTime": 0,
                "lastUpdated": None
            }
        
        metrics = self.metrics[key]
        metrics["totalRequests"] += 1
        
        if 200 <= status_code < 400:
            metrics["successfulRequests"] += 1
        else:
            metrics["failedRequests"] += 1
        
        # Update average response time
        total = metrics["totalRequests"]
        metrics["averageResponseTime"] = (
            (metrics["averageResponseTime"] * (total - 1) + response_time) / total
        )
        
        metrics["lastUpdated"] = datetime.now(timezone.utc).isoformat()
    
    def get_version_usage_report(self) -> dict:
        """Get version usage report."""
        report = {}
        
        for key, metrics in self.metrics.items():
            api_version = key.split(":")[0]
            
            if api_version not in report:
                report[api_version] = {
                    "totalRequests": 0,
                    "totalEndpoints": 0,
                    "averageResponseTime": 0
                }
            
            report[api_version]["totalRequests"] += metrics["totalRequests"]
            report[api_version]["totalEndpoints"] += 1
        
        return report
```

### 11.2 Deprecation Monitoring

```python
class DeprecationMonitor:
    def __init__(self):
        self.deprecation_warnings = {}
    
    def track_deprecated_usage(self, version: str, endpoint: str, 
                                client_info: dict):
        """Track usage of deprecated API versions."""
        key = f"{version}:{endpoint}"
        
        if key not in self.deprecation_warnings:
            self.deprecation_warnings[key] = {
                "totalCalls": 0,
                "uniqueClients": set(),
                "firstSeen": datetime.now(timezone.utc).isoformat(),
                "lastSeen": None
            }
        
        warnings = self.deprecation_warnings[key]
        warnings["totalCalls"] += 1
        warnings["uniqueClients"].add(client_info.get("userAgent", "unknown"))
        warnings["lastSeen"] = datetime.now(timezone.utc).isoformat()
    
    def get_deprecation_report(self) -> dict:
        """Get deprecation usage report."""
        report = []
        
        for key, warnings in self.deprecation_warnings.items():
            version, endpoint = key.split(":")
            report.append({
                "version": version,
                "endpoint": endpoint,
                "totalCalls": warnings["totalCalls"],
                "uniqueClients": len(warnings["uniqueClients"]),
                "firstSeen": warnings["firstSeen"],
                "lastSeen": warnings["lastSeen"]
            })
        
        return {"deprecatedEndpoints": report}
```

---

*Document generated as part of NHDOS Canonical Domain Model*
*Versioning model defined for all entities*
*Constitution Reference: Articles IV, VII, XII, XVI*
*Last Updated: 2026-06-25*
