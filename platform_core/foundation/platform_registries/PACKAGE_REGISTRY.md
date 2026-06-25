# PACKAGE REGISTRY

**NHDOS Platform-Core — Package Registry**
**Version:** 1.0.0 | **Date:** 2026-06-25

---

## 1. Executive Summary

The NHDOS Package Registry manages internal software packages, libraries, and artifacts across all platform services. It provides versioning, dependency management, security scanning, and distribution for internal packages.

---

## 2. Architecture Overview

### 2.1 Package Registry Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Package Registry                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Package   │  │  Security   │  │  Package    │     │
│  │   Store     │──▶│  Scanner    │──▶│  Server     │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │              │
│         └────────┬───────┴────────┬───────┘              │
│                  │                │                       │
│         ┌────────▼────────┐ ┌────▼────────────┐         │
│         │  Package Store  │ │  Proxy Cache    │         │
│         │  (S3/NFS)       │ │  (Nginx)        │         │
│         └─────────────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Package Types

### 3.1 Supported Package Formats

| Format | Package Manager | Use Case |
|--------|-----------------|----------|
| Python | pip/poetry | Python packages |
| npm | npm/yarn | JavaScript packages |
| Maven | Maven/Gradle | Java packages |
| Go | Go Modules | Go packages |
| NuGet | NuGet | .NET packages |
| Docker | Docker | Container images |

### 3.2 Package Definition

```json
{
  "package_id": "nhdos-patient-sdk",
  "name": "NHDOS Patient SDK",
  "version": "1.2.3",
  "description": "Python SDK for Patient Service API",
  "author": "NHDOS Platform Team",
  "license": "Apache-2.0",
  "type": "python",
  "repository": "https://packages.nhdos.iq/python/nhdos-patient-sdk",
  "dependencies": {
    "requests": ">=2.28.0",
    "pydantic": ">=2.0.0",
    "nhdos-auth": ">=1.0.0"
  },
  "metadata": {
    "python_requires": ">=3.8",
    "platform": "linux",
    "classifiers": [
      "Programming Language :: Python :: 3.8",
      "Topic :: Healthcare"
    ]
  }
}
```

---

## 4. Package Management

### 4.1 Publishing Process

```
1. Developer builds package
2. Run local tests
3. Package with metadata
4. Upload to registry
5. Security scan
6. Virus scan
7. Availability check
8. Publish to repository
```

### 4.2 Publishing Implementation

```python
class PackagePublisher:
    def publish(self, package_path: str, metadata: PackageMetadata) -> Package:
        # 1. Validate package
        self.validate_package(package_path)
        
        # 2. Security scan
        scan_result = self.security_scan(package_path)
        if scan_result.has_critical:
            raise SecurityError("Critical vulnerabilities found")
        
        # 3. Virus scan
        virus_result = self.virus_scan(package_path)
        if virus_result.infected:
            raise SecurityError("Virus detected")
        
        # 4. Upload to storage
        storage_url = self.upload_to_storage(package_path)
        
        # 5. Register in database
        package = self.register_package(metadata, storage_url)
        
        return package
```

---

## 5. Dependency Management

### 5.1 Dependency Resolution

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Exact | `==1.2.3` | Production builds |
| Compatible | `>=1.2.0,<2.0.0` | Stable dependencies |
| Range | `>=1.2.0` | Flexible dependencies |
| Latest | `*` | Development |

### 5.2 Dependency Graph

```python
class DependencyResolver:
    def resolve(self, package_id: str, version: str) -> DependencyGraph:
        # 1. Get package dependencies
        package = self.get_package(package_id, version)
        
        # 2. Resolve dependencies recursively
        graph = DependencyGraph()
        self.resolve_dependencies(package, graph)
        
        # 3. Check for conflicts
        conflicts = graph.get_conflicts()
        if conflicts:
            raise DependencyConflict(conflicts)
        
        return graph
```

---

## 6. APIs

### 6.1 Package Registry API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/packages` | GET | List packages |
| `/api/v1/packages` | POST | Publish package |
| `/api/v1/packages/{name}` | GET | Get package details |
| `/api/v1/packages/{name}/versions` | GET | List versions |
| `/api/v1/packages/{name}/versions/{version}` | GET | Get version details |
| `/api/v1/packages/{name}/download` | GET | Download package |
| `/api/v1/packages/{name}/delete` | DELETE | Delete package |

### 6.2 Package Client

```python
# pip configuration
[global]
index-url = https://packages.nhdos.iq/python/simple/
trusted-host = packages.nhdos.iq

# npm configuration
registry=https://packages.nhdos.iq/npm/
//packages.nhdos.iq/npm/:_authToken=${NPM_TOKEN}

# maven configuration
<repository>
    <id>nhdos</id>
    <url>https://packages.nhdos.iq/maven/</url>
</repository>
```

---

*Generated as part of NHDOS Platform-Core Phase 17.1 Architecture Freeze*
