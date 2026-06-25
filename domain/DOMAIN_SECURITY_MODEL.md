# DOMAIN SECURITY MODEL — NATIONAL HEALTHCARE DIGITAL OPERATING SYSTEM

**Document**: Canonical Security Model for All Entities
**Version**: 1.0.0
**Date**: 2026-06-25
**Status**: ACTIVE
**Constitution Reference**: Articles I, V, IX, XII, XVII

---

## 1. OVERVIEW

This document defines the comprehensive security model for every entity in the NHDOS. Security is not an add-on but a fundamental property of every entity, relationship, and operation.

**Security Principles**:
- Zero Trust: Every access request is verified regardless of origin
- Defense in Depth: Multiple security layers protect every entity
- Least Privilege: Users and systems receive minimum required permissions
- Separation of Duties: Critical operations require multiple actors
- Security by Design: Security is built into entity architecture
- Audit Everything: Every access and mutation is logged

---

## 2. CONFIDENTIALITY LEVELS

### 2.1 Level Definitions

| Level | Label | Description | Access Control |
|-------|-------|-------------|----------------|
| 1 | **Public** | Freely available | No restrictions |
| 2 | **Internal** | Organization-wide | Authentication required |
| 3 | **Confidential** | Role-based access | Role + authentication |
| 4 | **Restricted** | Need-to-know basis | Role + authentication + justification |
| 5 | **Top Secret** | Cleared personnel only | Role + authentication + clearance + MFA |

### 2.2 Entity Confidentiality Assignments

| Entity | Default Level | Justification |
|--------|--------------|---------------|
| Repository | Internal | Organizational code asset |
| Module | Internal | Platform component |
| Service | Internal | Operational component |
| API | Internal | Interface contract |
| Event | Internal | System communication |
| Device | Confidential | Medical device information |
| Workflow | Internal | Business process definition |
| Policy | Confidential | Security rules |
| Manifest | Internal | Component declaration |
| Certification | Confidential | Compliance status |
| Dependency | Internal | Component relationships |
| Relationship | Internal | Entity mappings |
| Patient | **Restricted** | PHI (Protected Health Information) |
| Sample | **Restricted** | Linked to patient PHI |
| Test Order | **Restricted** | Clinical decision data |
| Test Result | **Restricted** | Clinical diagnosis data |
| User | Confidential | Personal employee data |
| Role | Internal | Access control definitions |
| Facility | Internal | Organizational structure |
| Credential | Confidential | Professional qualifications |
| Correspondence | Variable | Classification-dependent |
| Inventory Item | Internal | Operational data |
| Attendance Record | Confidential | Employee monitoring data |
| Leave Request | Confidential | Employee personal data |
| Training Record | Confidential | Employee qualification data |
| Audit Event | **Top Secret** | Tamper-evident security log |
| Notification | Internal | System communication |
| Report | Variable | Classification-dependent |
| Protocol | Internal | Technical specification |
| Driver | Internal | Technical component |
| Capability | Internal | Technical capability |
| Schema | Internal | Data structure definition |
| Standard | Public | Healthcare standard reference |
| Configuration | Confidential | System behavior settings |
| Finding | Confidential | Security/quality finding |
| Review | Confidential | Assessment result |
| Decision | Confidential | Governance decision |
| Recommendation | Internal | Improvement suggestion |
| Exception | Confidential | Policy exception |
| Risk Assessment | Confidential | Risk analysis |
| Compliance Standard | Public | Regulatory reference |
| Quality Gate | Internal | Quality criteria |
| Knowledge Node | Internal | Entity relationship data |
| Knowledge Edge | Internal | Entity relationship data |
| Package | Internal | Distributable component |
| Release | Internal | Versioned release |
| Team | Internal | Organizational unit |
| ADR | Internal | Architecture decision |
| Event Instance | Internal | Event occurrence data |
| Sync Queue | Internal | Synchronization data |
| Offline Conflict | Internal | Conflict resolution data |
| Telemetry Event | Internal | Observability data |

---

## 3. INTEGRITY REQUIREMENTS

### 3.1 Integrity Levels

| Level | Name | Requirements | Entities |
|-------|------|--------------|----------|
| 1 | **Standard** | Basic validation, optimistic locking | Configuration, Notification |
| 2 | **Enhanced** | Field validation, version tracking | Repository, Module, Service, API |
| 3 | **Critical** | Hash verification, immutable audit | Patient, Sample, Test Result, Test Order |
| 4 | **Immutable** | Append-only, cryptographic chaining | Audit Event, Event Instance |
| 5 | **Tamper-Proof** | Blockchain-style chaining, digital signatures | Certification, Policy, Finding |

### 3.2 Entity Integrity Requirements

| Entity | Level | Validation | Immutability | Tamper Detection |
|--------|-------|------------|--------------|------------------|
| Patient | Critical | Schema + business rules | Partial (audit trail) | Yes |
| Sample | Critical | Schema + chain of custody | Yes (after analysis) | Yes |
| Test Result | Critical | Schema + reference ranges | Yes (after verification) | Yes |
| Test Order | Critical | Schema + clinical rules | Yes (after completion) | Yes |
| Audit Event | Immutable | Schema validation | Fully immutable | Yes (hash chain) |
| Certification | Tamper-Proof | Schema + criteria validation | Fully immutable | Yes (digital signature) |
| Policy | Tamper-Proof | Schema + rule validation | Version controlled | Yes (digital signature) |
| Finding | Critical | Schema + severity validation | Version controlled | Yes |
| Credential | Critical | Schema + issuer validation | Yes (after issuance) | Yes |
| User | Enhanced | Schema + business rules | Version controlled | Yes |
| Device | Enhanced | Schema + capability validation | Version controlled | No |
| Repository | Enhanced | Schema + manifest validation | Version controlled | No |

### 3.3 Integrity Verification

```python
import hashlib
import json
from datetime import datetime

class IntegrityVerifier:
    def compute_hash(self, entity: dict, exclude_fields: list = None) -> str:
        """Compute SHA-256 hash of entity."""
        exclude = exclude_fields or ["_hash", "_hashChain", "_signature"]
        clean_entity = {k: v for k, v in entity.items() if k not in exclude}
        serialized = json.dumps(clean_entity, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()
    
    def verify_hash(self, entity: dict) -> bool:
        """Verify entity hash integrity."""
        stored_hash = entity.get("_hash")
        if not stored_hash:
            return True  # No hash to verify
        
        computed_hash = self.compute_hash(entity)
        return stored_hash == computed_hash
    
    def verify_hash_chain(self, events: list) -> bool:
        """Verify hash chain for immutable entities."""
        for i in range(1, len(events)):
            current = events[i]
            previous = events[i-1]
            
            # Verify current event references previous hash
            if current.get("_previousHash") != previous.get("_hash"):
                return False
            
            # Verify current event hash
            if not self.verify_hash(current):
                return False
        
        return True
```

### 3.4 Immutable Audit Trail

```python
class ImmutableAuditTrail:
    def __init__(self):
        self.chain = []
    
    def append_event(self, event: dict) -> dict:
        """Append event to immutable chain."""
        previous_hash = self.chain[-1]["_hash"] if self.chain else "0" * 64
        
        event["_previousHash"] = previous_hash
        event["_hash"] = hashlib.sha256(
            json.dumps(event, sort_keys=True, default=str).encode()
        ).hexdigest()
        event["_sequenceNumber"] = len(self.chain)
        event["_timestamp"] = datetime.now(timezone.utc).isoformat()
        
        self.chain.append(event)
        return event
    
    def verify_chain(self) -> bool:
        """Verify entire chain integrity."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current["_previousHash"] != previous["_hash"]:
                return False
            
            expected_hash = hashlib.sha256(
                json.dumps({k: v for k, v in current.items() 
                          if k not in ("_hash",)}, sort_keys=True, default=str).encode()
            ).hexdigest()
            
            if current["_hash"] != expected_hash:
                return False
        
        return True
```

---

## 4. AVAILABILITY REQUIREMENTS

### 4.1 Availability Tiers

| Tier | SLA | Recovery Time | Recovery Point | Entities |
|------|-----|---------------|----------------|----------|
| **Tier 1** | 99.99% | < 1 minute | < 1 minute | Patient, Test Result, Audit Event |
| **Tier 2** | 99.9% | < 5 minutes | < 5 minutes | Sample, Test Order, Device |
| **Tier 3** | 99.5% | < 30 minutes | < 15 minutes | User, Role, Facility |
| **Tier 4** | 99.0% | < 4 hours | < 1 hour | Configuration, Report |
| **Tier 5** | 95.0% | < 24 hours | < 24 hours | Telemetry, Notification |

### 4.2 Entity Availability Requirements

| Entity | Tier | Offline Available | Backup Frequency | Replication |
|--------|------|-------------------|------------------|-------------|
| Patient | 1 | Yes | Real-time | Multi-region |
| Sample | 1 | Yes | Real-time | Multi-region |
| Test Result | 1 | Yes | Real-time | Multi-region |
| Test Order | 2 | Yes | Every 5 min | Multi-region |
| Device | 2 | Yes | Every 5 min | Regional |
| User | 3 | Yes | Every 15 min | Regional |
| Role | 3 | Yes | Every 15 min | Regional |
| Facility | 3 | Yes | Every 15 min | Regional |
| Credential | 3 | Yes | Every 15 min | Regional |
| Configuration | 4 | Yes | Every hour | Regional |
| Report | 4 | No | Every hour | Single |
| Audit Event | 1 | Yes | Real-time | Multi-region (append-only) |
| Telemetry | 5 | Yes | Every 24 hours | Single |

### 4.3 Failover Strategy

```python
class FailoverManager:
    def __init__(self):
        self.primary_region = None
        self.secondary_regions = []
        self.failover_threshold = 3  # consecutive failures
    
    async def check_health(self, region: str) -> bool:
        """Check region health."""
        try:
            response = await self.health_client.check(region)
            return response.status == "healthy"
        except Exception:
            return False
    
    async def execute_failover(self) -> dict:
        """Execute failover to secondary region."""
        for region in self.secondary_regions:
            if await self.check_health(region):
                # Update routing
                await self.update_routing(region)
                
                # Notify operators
                await self.notify_failover(region)
                
                return {
                    "failoverExecuted": True,
                    "newPrimary": region,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
        
        return {
            "failoverExecuted": False,
            "reason": "No healthy secondary regions available"
        }
```

---

## 5. RBAC ROLES

### 5.1 Role Hierarchy

```
Platform Administrator
├── System Administrator
│   ├── Facility Administrator
│   │   ├── Department Supervisor
│   │   │   ├── Lab Technician
│   │   │   ├── Doctor
│   │   │   ├── Nurse
│   │   │   └── Operator
│   │   └── Quality Manager
│   └── Security Administrator
└── Auditor (read-only across all levels)
```

### 5.2 Role Definitions

| Role | Description | Entity Access | Mutations |
|------|-------------|---------------|-----------|
| **Platform Administrator** | Full system access | All entities | All operations |
| **System Administrator** | System configuration | All except audit | All except audit |
| **Facility Administrator** | Facility management | Facility-scoped | All within scope |
| **Department Supervisor** | Department oversight | Department-scoped | Approve, verify, assign |
| **Quality Manager** | Quality assurance | Quality entities | Quality operations |
| **Security Administrator** | Security management | Security entities | Security operations |
| **Lab Technician** | Laboratory operations | Lab entities | Create, update (lab) |
| **Doctor** | Clinical operations | Clinical entities | Create, update (clinical) |
| **Nursing** | Nursing operations | Patient care entities | Create, update (nursing) |
| **Operator** | Basic operations | Assigned entities | Read, limited create |
| **Auditor** | Audit and compliance | All entities (read) | Read-only |

### 5.3 Entity-Role Permission Matrix

| Entity | Platform Admin | System Admin | Facility Admin | Supervisor | Technician | Doctor | Operator | Auditor |
|--------|---------------|--------------|----------------|------------|------------|--------|----------|---------|
| Patient | CRUD | CRUD | CRUD | CRUD | CRU | CRU | R | R |
| Sample | CRUD | CRUD | CRUD | CRUD | CRUD | R | R | R |
| Test Result | CRUD | CRUD | CRUD | CRUD | CR | CR | R | R |
| Test Order | CRUD | CRUD | CRUD | CRUD | CR | CRUD | R | R |
| User | CRUD | CRUD | CRU | RU | R | R | R | R |
| Role | CRUD | CRUD | RU | R | R | R | R | R |
| Facility | CRUD | CRUD | CRUD | R | R | R | R | R |
| Device | CRUD | CRUD | CRUD | CRUD | CRU | R | R | R |
| Credential | CRUD | CRUD | CRU | RU | R | R | R | R |
| Inventory | CRUD | CRUD | CRUD | CRUD | CRU | R | R | R |
| Audit Event | R | R | R | R | R | R | R | R |
| Policy | CRUD | CRUD | RU | R | R | R | R | R |
| Configuration | CRUD | CRUD | CRU | RU | R | R | R | R |
| Correspondence | CRUD | CRUD | CRUD | CRUD | CRU | CRU | R | R |
| Report | CRUD | CRUD | CRUD | CRU | CR | CR | R | R |

**Legend**: C=Create, R=Read, U=Update, D=Delete

### 5.4 Permission Definition

```python
class Permission:
    def __init__(self, entity: str, action: str, scope: str = "own"):
        self.entity = entity
        self.action = action  # create, read, update, delete, approve, verify, export
        self.scope = scope    # own, department, facility, global
    
    def matches(self, required_permission: 'Permission') -> bool:
        """Check if this permission matches the required permission."""
        if self.entity != required_permission.entity and self.entity != "*":
            return False
        
        if self.action != required_permission.action and self.action != "*":
            return False
        
        scope_hierarchy = {"own": 0, "department": 1, "facility": 2, "global": 3}
        if scope_hierarchy.get(self.scope, 0) < scope_hierarchy.get(required_permission.scope, 0):
            return False
        
        return True

class RBACEngine:
    def __init__(self):
        self.role_permissions = {}
        self.user_roles = {}
    
    def check_permission(self, user_id: str, entity: str, action: str, scope: str = "own") -> bool:
        """Check if user has required permission."""
        user_roles = self.user_roles.get(user_id, [])
        
        for role_name in user_roles:
            permissions = self.role_permissions.get(role_name, [])
            required = Permission(entity, action, scope)
            
            for perm in permissions:
                if perm.matches(required):
                    return True
        
        return False
```

---

## 6. ABAC POLICIES

### 6.1 Attribute-Based Access Control Overview

ABAC extends RBAC by evaluating attributes of:

| Attribute Category | Examples |
|-------------------|----------|
| **Subject** | Role, department, clearance, shift, location |
| **Resource** | Entity type, classification, owner, facility |
| **Action** | Create, read, update, delete, approve, export |
| **Environment** | Time, location, network, device, risk level |

### 6.2 ABAC Policy Definitions

#### 6.2.1 Time-Based Policies

```json
{
  "policyId": "ABAC-TIME-001",
  "name": "Shift-Based Access",
  "description": "Technicians can only modify results during their shift",
  "effect": "permit",
  "subject": {
    "role": "lab_technician",
    "department": "laboratory"
  },
  "resource": {
    "entity": "test_result",
    "action": "update"
  },
  "conditions": [
    {
      "attribute": "subject.currentShift",
      "operator": "equals",
      "value": "current"
    },
    {
      "attribute": "resource.status",
      "operator": "not_equals",
      "value": "verified"
    }
  ]
}
```

#### 6.2.2 Location-Based Policies

```json
{
  "policyId": "ABAC-LOC-001",
  "name": "Facility-Bound Access",
  "description": "Users can only access data for their assigned facility",
  "effect": "deny",
  "subject": {
    "role": "*"
  },
  "resource": {
    "entity": "*"
  },
  "conditions": [
    {
      "attribute": "resource.facilityId",
      "operator": "not_equals",
      "value": "subject.assignedFacility"
    }
  ]
}
```

#### 6.2.3 Risk-Based Policies

```json
{
  "policyId": "ABAC-RISK-001",
  "name": "High-Risk Operation Control",
  "description": "Critical operations require elevated clearance during high-risk periods",
  "effect": "permit",
  "subject": {
    "clearanceLevel": ">=4"
  },
  "resource": {
    "entity": ["patient", "test_result"],
    "action": "delete"
  },
  "conditions": [
    {
      "attribute": "environment.riskLevel",
      "operator": "equals",
      "value": "high"
    }
  ]
}
```

#### 6.2.4 Device-Based Policies

```json
{
  "policyId": "ABAC-DEV-001",
  "name": "Managed Device Only",
  "description": "Sensitive data can only be accessed from managed devices",
  "effect": "deny",
  "subject": {
    "role": "*"
  },
  "resource": {
    "classification": ">=restricted"
  },
  "conditions": [
    {
      "attribute": "environment.deviceType",
      "operator": "not_in",
      "value": ["managed_desktop", "managed_laptop", "managed_tablet"]
    }
  ]
}
```

### 6.3 ABAC Policy Engine

```python
class ABACEngine:
    def __init__(self):
        self.policies = []
    
    def evaluate(self, subject: dict, resource: dict, action: str, environment: dict) -> dict:
        """Evaluate ABAC policies for access decision."""
        applicable_policies = self.get_applicable_policies(subject, resource, action)
        
        decisions = []
        for policy in applicable_policies:
            if self.evaluate_conditions(policy, subject, resource, environment):
                decisions.append({
                    "policyId": policy["policyId"],
                    "effect": policy["effect"]
                })
        
        # Deny overrides permit
        if any(d["effect"] == "deny" for d in decisions):
            return {"decision": "deny", "policies": decisions}
        
        if any(d["effect"] == "permit" for d in decisions):
            return {"decision": "permit", "policies": decisions}
        
        return {"decision": "deny", "policies": [], "reason": "No applicable policy"}
    
    def evaluate_conditions(self, policy: dict, subject: dict, resource: dict, environment: dict) -> bool:
        """Evaluate all conditions in a policy."""
        for condition in policy.get("conditions", []):
            if not self.evaluate_condition(condition, subject, resource, environment):
                return False
        return True
    
    def evaluate_condition(self, condition: dict, subject: dict, resource: dict, environment: dict) -> bool:
        """Evaluate a single condition."""
        attribute_path = condition["attribute"]
        operator = condition["operator"]
        expected_value = condition["value"]
        
        # Resolve attribute value
        actual_value = self.resolve_attribute(attribute_path, subject, resource, environment)
        
        # Evaluate operator
        return self.evaluate_operator(actual_value, operator, expected_value)
```

---

## 7. ENCRYPTION REQUIREMENTS

### 7.1 Encryption at Rest

| Entity Classification | Encryption Required | Algorithm | Key Management |
|----------------------|---------------------|-----------|----------------|
| Public | No | N/A | N/A |
| Internal | Recommended | AES-256-GCM | Platform KMS |
| Confidential | Required | AES-256-GCM | Platform KMS |
| Restricted | Required | AES-256-GCM | HSM-backed KMS |
| Top Secret | Required | AES-256-GCM | HSM + dual control |

### 7.2 Encryption in Transit

| Connection Type | Encryption Required | Protocol | Minimum Version |
|----------------|---------------------|----------|-----------------|
| Client → Server | Required | TLS | 1.3 |
| Server → Server | Required | mTLS | 1.3 |
| Server → Database | Required | TLS | 1.3 |
| Server → Cache | Required | TLS | 1.2 |
| Server → External API | Required | TLS | 1.3 |
| Offline Sync | Required | mTLS | 1.3 |

### 7.3 Field-Level Encryption

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class FieldEncryption:
    def __init__(self, master_key: bytes):
        self.master_key = master_key
    
    def encrypt_field(self, field_name: str, value: str, context: dict) -> dict:
        """Encrypt a specific field with associated data."""
        # Generate unique key for this field
        key = self.derive_key(field_name, context)
        
        # Generate nonce
        nonce = os.urandom(12)
        
        # Create AESGCM instance
        aesgcm = AESGCM(key)
        
        # Encrypt with associated data
        associated_data = json.dumps(context).encode()
        ciphertext = aesgcm.encrypt(nonce, value.encode(), associated_data)
        
        return {
            "ciphertext": ciphertext.hex(),
            "nonce": nonce.hex(),
            "keyVersion": context.get("keyVersion", 1)
        }
    
    def decrypt_field(self, field_name: str, encrypted_data: dict, context: dict) -> str:
        """Decrypt a specific field."""
        key = self.derive_key(field_name, context)
        
        nonce = bytes.fromhex(encrypted_data["nonce"])
        ciphertext = bytes.fromhex(encrypted_data["ciphertext"])
        
        aesgcm = AESGCM(key)
        associated_data = json.dumps(context).encode()
        
        plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data)
        return plaintext.decode()
```

### 7.4 Encryption Key Hierarchy

```
Root Key (HSM)
├── Master Key (KMS)
│   ├── Data Encryption Key (DEK)
│   │   ├── Patient DEK
│   │   ├── Test Result DEK
│   │   └── Audit DEK
│   └── Key Encryption Key (KEK)
│       ├── Facility KEK
│       └── Department KEK
└── Signing Key (HSM)
    ├── Certificate Signing Key
    └── Document Signing Key
```

### 7.5 Key Rotation

| Key Type | Rotation Frequency | Process |
|----------|-------------------|---------|
| DEK | Every 90 days | Automatic, re-encrypt data |
| KEK | Every 180 days | Automatic, re-wrap DEKs |
| Master | Every 365 days | Manual, dual control |
| Root | Every 3650 days | Manual, dual control, ceremony |

---

## 8. DIGITAL SIGNATURE REQUIREMENTS

### 8.1 Signing Requirements by Entity

| Entity | Signing Required | Algorithm | Use Case |
|--------|-----------------|-----------|----------|
| Patient Record | Recommended | Ed25519 | Clinical sign-off |
| Test Result | Required | Ed25519 | Result verification |
| Test Order | Recommended | Ed25519 | Order authentication |
| Certification | Required | Ed25519 | Compliance attestation |
| Policy | Required | Ed25519 | Policy authenticity |
| Finding | Required | Ed25519 | Finding attestation |
| Correspondence | Required | Ed25519 | Official document |
| Report | Recommended | Ed25519 | Report authenticity |
| Manifest | Required | Ed25519 | Component integrity |
| Package | Required | Ed25519 | Package integrity |
| Credential | Required | Ed25519 | Credential authenticity |

### 8.2 Digital Signature Process

```python
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import hashlib

class DigitalSignature:
    def __init__(self, private_key: ed25519.Ed25519PrivateKey):
        self.private_key = private_key
        self.public_key = private_key.public_key()
    
    def sign_entity(self, entity: dict) -> dict:
        """Sign an entity."""
        # Create canonical representation
        canonical = self.canonicalize(entity)
        
        # Compute hash
        entity_hash = hashlib.sha256(canonical.encode()).digest()
        
        # Sign hash
        signature = self.private_key.sign(entity_hash)
        
        return {
            "signature": signature.hex(),
            "algorithm": "Ed25519",
            "publicKey": self.public_key.public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode(),
            "signedAt": datetime.now(timezone.utc).isoformat()
        }
    
    def verify_signature(self, entity: dict, signature_data: dict) -> bool:
        """Verify entity signature."""
        # Reconstruct public key
        public_key = serialization.load_pem_public_key(
            signature_data["publicKey"].encode()
        )
        
        # Create canonical representation
        canonical = self.canonicalize(entity)
        
        # Compute hash
        entity_hash = hashlib.sha256(canonical.encode()).digest()
        
        # Verify signature
        try:
            public_key.verify(
                bytes.fromhex(signature_data["signature"]),
                entity_hash
            )
            return True
        except Exception:
            return False
```

### 8.3 Signature Verification Chain

```
Signed Entity
├── Verify Entity Hash
├── Verify Signature Algorithm
├── Verify Public Key in Trust Store
├── Verify Signing Authority
└── Verify Timestamp
    └── All checks pass → Signature VALID
```

### 8.4 Trust Store

```python
class TrustStore:
    def __init__(self):
        self.trusted_keys = {}
        self.key_metadata = {}
    
    def register_key(self, key_id: str, public_key: str, metadata: dict):
        """Register a trusted public key."""
        self.trusted_keys[key_id] = public_key
        self.key_metadata[key_id] = {
            "registeredAt": datetime.now(timezone.utc).isoformat(),
            "expiresAt": metadata.get("expiresAt"),
            "owner": metadata.get("owner"),
            "algorithm": metadata.get("algorithm", "Ed25519"),
            "status": "active"
        }
    
    def verify_key(self, key_id: str) -> bool:
        """Verify if a key is trusted and valid."""
        if key_id not in self.trusted_keys:
            return False
        
        metadata = self.key_metadata[key_id]
        
        # Check status
        if metadata["status"] != "active":
            return False
        
        # Check expiration
        if metadata.get("expiresAt"):
            expiry = datetime.fromisoformat(metadata["expiresAt"])
            if datetime.now(timezone.utc) > expiry:
                return False
        
        return True
```

---

## 9. AUTHENTICATION REQUIREMENTS

### 9.1 Authentication Methods

| Method | Security Level | Use Case | MFA Required |
|--------|---------------|----------|--------------|
| Username/Password | Standard | General access | Recommended |
| JWT Token | Standard | API access | Recommended |
| API Key | Standard | Service-to-service | No |
| Certificate (mTLS) | High | Server-to-server | No |
| Hardware Token | High | Administrative access | Yes |
| Biometric | High | Physical access | No |
| Smart Card | High | Government access | Yes |

### 9.2 Authentication by Entity Access

| Entity Classification | Authentication Required | MFA Required |
|----------------------|------------------------|--------------|
| Public | None | No |
| Internal | Username/Password | No |
| Confidential | Username/Password + JWT | Recommended |
| Restricted | Username/Password + JWT | Required |
| Top Secret | Certificate + Hardware Token | Required |

### 9.3 Token Structure

```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "key-id"
  },
  "payload": {
    "sub": "user-uuid",
    "iss": "nhdos-auth",
    "aud": "nhdos-api",
    "exp": 1719312000,
    "iat": 1719308400,
    "jti": "token-uuid",
    "roles": ["lab_technician"],
    "permissions": ["patient:read", "sample:create", "test_result:create"],
    "facility": "facility-uuid",
    "department": "laboratory",
    "clearanceLevel": 3,
    "mfa": true,
    "sessionId": "session-uuid"
  }
}
```

### 9.4 Token Lifecycle

```
Issue → Active → Refresh → Active → ... → Expire → Revoke
                      ↓
                      └── Compromise → Revoke
```

| Action | Trigger | Duration |
|--------|---------|----------|
| Issue | Successful authentication | 15 minutes |
| Refresh | Within 5 minutes of expiry | 24 hours |
| Expire | After 15 minutes without refresh | N/A |
| Revoke | Security event, logout | Immediate |

---

## 10. AUTHORIZATION REQUIREMENTS

### 10.1 Authorization Check Flow

```
Request → Authenticate → Extract Identity → Check RBAC → Check ABAC → Allow/Deny
```

### 10.2 Entity-Specific Authorization Rules

#### 10.2.1 Patient Entity

```yaml
patient:
  create:
    required_roles: [doctor, nurse, lab_technician, registration]
    required_facility: true
    conditions:
      - field: "medicalRecordNumber"
        validation: "unique_per_facility"
  
  read:
    required_roles: [doctor, nurse, lab_technician, registration, auditor]
    scope: facility
    conditions:
      - field: "relationship"
        operator: "in"
        value: ["treating", "consulting", "emergency"]
  
  update:
    required_roles: [doctor, nurse, registration]
    scope: facility
    conditions:
      - field: "status"
        operator: "not_equals"
        value: "deceased"
  
  delete:
    required_roles: [platform_administrator]
    conditions:
      - field: "hasClinicalData"
        operator: "equals"
        value: false
```

#### 10.2.2 Test Result Entity

```yaml
test_result:
  create:
    required_roles: [lab_technician, lab_supervisor]
    required_facility: true
    conditions:
      - field: "testOrder"
        operator: "exists"
        value: true
  
  read:
    required_roles: [lab_technician, lab_supervisor, doctor, nurse]
    scope: facility
  
  update:
    required_roles: [lab_technician, lab_supervisor]
    conditions:
      - field: "status"
        operator: "equals"
        value: "preliminary"
  
  verify:
    required_roles: [lab_supervisor, lab_director]
    conditions:
      - field: "status"
        operator: "equals"
        value: "preliminary"
  
  delete:
    required_roles: [platform_administrator]
    conditions:
      - field: "isIntegrated"
        operator: "equals"
        value: false
```

#### 10.2.3 Audit Event Entity

```yaml
audit_event:
  create:
    required_roles: [system]
    immutable: true
  
  read:
    required_roles: [auditor, security_administrator, platform_administrator]
    scope: global
    conditions:
      - field: "clearanceLevel"
        operator: "gte"
        value: 4
  
  update:
    required_roles: []
    denied: true
  
  delete:
    required_roles: []
    denied: true
```

---

## 11. DATA CLASSIFICATION HANDLING

### 11.1 Classification Requirements

| Level | Storage | Access Logging | Export | Print | Screen Display |
|-------|---------|---------------|--------|-------|----------------|
| Public | Any | Optional | Allowed | Allowed | Allowed |
| Internal | Encrypted | Recommended | Controlled | Controlled | Allowed |
| Confidential | Encrypted | Required | Restricted | Restricted | Controlled |
| Restricted | Encrypted + HSM | Required | Denied | Restricted | Restricted |
| Top Secret | Encrypted + HSM | Required | Denied | Denied | Restricted |

### 11.2 Classification Labels

```json
{
  "classification": "restricted",
  "classificationMetadata": {
    "classifiedBy": "user-uuid",
    "classifiedAt": "2026-06-25T10:00:00Z",
    "reviewDate": "2027-06-25T00:00:00Z",
    "reason": "Contains PHI",
    "applicableRegulations": ["HIPAA", "GDPR"]
  }
}
```

### 11.3 Classification Inheritance

When entities are related, classification follows the highest level:

```
Patient (Restricted)
├── Sample (Restricted - inherits from Patient)
├── Test Order (Restricted - inherits from Patient)
└── Test Result (Restricted - inherits from Patient)
```

---

## 12. SECURITY AUDIT REQUIREMENTS

### 12.1 Audit Events by Entity

| Entity | Events to Audit |
|--------|-----------------|
| Patient | All access, all mutations, all exports |
| Sample | All access, all mutations, all status changes |
| Test Result | All access, all mutations, all verifications |
| Test Order | All access, all mutations, all cancellations |
| User | All access, all mutations, all role changes |
| Credential | All access, all mutations, all issuances |
| Configuration | All access, all mutations |
| Audit Event | All access (meta-audit) |
| Policy | All access, all mutations |
| Finding | All access, all mutations |

### 12.2 Audit Log Structure

```json
{
  "eventId": "uuid",
  "timestamp": "2026-06-25T10:00:00Z",
  "actor": {
    "userId": "uuid",
    "username": "ahmed.rashid",
    "roles": ["lab_technician"],
    "facility": "facility-uuid",
    "ipAddress": "10.0.0.1",
    "userAgent": "Mozilla/5.0...",
    "sessionId": "session-uuid"
  },
  "action": {
    "type": "read",
    "entity": "patient",
    "entityId": "patient-uuid",
    "fields": ["firstName", "lastName", "dateOfBirth"]
  },
  "result": {
    "status": "success",
    "duration": "15ms"
  },
  "context": {
    "correlationId": "corr-uuid",
    "requestId": "req-uuid",
    "facility": "facility-uuid",
    "department": "laboratory"
  },
  "metadata": {
    "classification": "restricted",
    "sensitivity": "high"
  }
}
```

---

## 13. SECURITY POLICIES

### 13.1 Password Policy

| Requirement | Value |
|-------------|-------|
| Minimum Length | 12 characters |
| Complexity | Upper, lower, digit, special |
| History | Last 12 passwords |
| Max Age | 90 days |
| Lockout Threshold | 5 failed attempts |
| Lockout Duration | 30 minutes |

### 13.2 Session Policy

| Requirement | Value |
|-------------|-------|
| Max Session Duration | 8 hours |
| Idle Timeout | 30 minutes |
| Concurrent Sessions | 3 per user |
| Session Binding | IP + User Agent |

### 13.3 API Security Policy

| Requirement | Value |
|-------------|-------|
| Rate Limiting | 1000 requests/minute |
| Request Size Limit | 10MB |
| Timeout | 30 seconds |
| CORS | Whitelist only |
| Content Security | Enabled |

---

## 14. COMPLIANCE REQUIREMENTS

### 14.1 Regulatory Compliance

| Regulation | Applicability | Key Requirements |
|------------|---------------|------------------|
| HIPAA | US Healthcare | PHI protection, audit trail |
| GDPR | EU Data | Consent, right to deletion |
| NIST 800-53 | US Government | Security controls |
| ISO 27001 | International | Information security |
| HL7 FHIR | Healthcare Data | Data exchange security |
| Local Regulations | Iraq | Government compliance |

### 14.2 Compliance Controls by Entity

| Entity | HIPAA | GDPR | NIST | ISO 27001 |
|--------|-------|------|------|-----------|
| Patient | Required | Required | Required | Required |
| Sample | Required | Recommended | Required | Required |
| Test Result | Required | Recommended | Required | Required |
| User | Required | Required | Required | Required |
| Audit Event | Required | N/A | Required | Required |

---

*Document generated as part of NHDOS Canonical Domain Model*
*Security model defined for all entities*
*Constitution Reference: Articles I, V, IX, XII, XVII*
*Last Updated: 2026-06-25*
