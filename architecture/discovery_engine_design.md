# DISCOVERY ENGINE DESIGN

**Document**: Repository Discovery Engine Architecture
**Version**: 1.0.0
**Date**: 2026-06-25
**Status**: DESIGN
**Constitution Reference**: Articles III, IV, X

---

## 1. OVERVIEW

The Discovery Engine is responsible for automatically discovering, analyzing, and scoring repositories in the platform ecosystem. It populates the Knowledge Graph and provides the foundation for governance, certification, and operational intelligence.

**Design Principles**:
- Non-invasive: Never modifies repository contents
- Comprehensive: Detects all aspects of repository structure
- Continuous: Runs on schedule and on-demand
- Transparent: All findings are auditable
- Extensible: New analyzers can be added via plugins

---

## 2. ENGINE ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                  DISCOVERY ENGINE                        │
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │  Scheduler   │───→│   Scanner   │───→│  Analyzer   │ │
│  │             │    │             │    │             │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│         │                  │                  │         │
│         ▼                  ▼                  ▼         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │  Trigger     │    │  Collector  │    │  Scorer     │ │
│  │  Engine      │    │             │    │             │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│         │                  │                  │         │
│         └──────────────────┼──────────────────┘         │
│                            ▼                            │
│                    ┌─────────────┐                      │
│                    │   Reporter  │                      │
│                    └─────────────┘                      │
│                            │                            │
│                            ▼                            │
│              ┌─────────────────────────┐                │
│              │    Knowledge Graph      │                │
│              │    Registry Service     │                │
│              │    Notification Service │                │
│              └─────────────────────────┘                │
└─────────────────────────────────────────────────────────┘
```

---

## 3. COMPONENTS

### 3.1 Scheduler

Controls when and how often discovery runs.

| Schedule Type | Frequency | Purpose |
|--------------|-----------|---------|
| Full Scan | Daily (02:00 UTC) | Complete ecosystem scan |
| Incremental | Every 4 hours | Changed repositories only |
| On-Demand | Manual trigger | Specific repository or event-driven |
| Post-Deploy | On deployment | Newly deployed repositories |
| Health Check | Every 5 minutes | Service health only |

**Configuration**:
```yaml
scheduler:
  full_scan:
    cron: "0 2 * * *"
    timezone: UTC
  incremental:
    interval: 4h
  health_check:
    interval: 5m
  on_deploy:
    enabled: true
    delay: 30s
```

### 3.2 Scanner

Discovers repository structure by analyzing the repository source.

**Scanning Capabilities**:

| Scanner | What It Detects | How |
|---------|----------------|-----|
| **Repository Scanner** | Repository metadata | Git remote, README, LICENSE |
| **Language Scanner** | Programming languages | File extensions, shebangs |
| **Framework Scanner** | Frameworks and libraries | Dependency files, imports |
| **Structure Scanner** | Directory structure | File system analysis |
| **Manifest Scanner** | Platform manifest | `platform-manifest.yaml` |
| **Docker Scanner** | Container configuration | `Dockerfile`, `docker-compose.yml` |
| **CI Scanner** | CI/CD pipelines | `.github/workflows`, `.gitlab-ci.yml` |
| **Documentation Scanner** | Documentation | `README.md`, `docs/`, `*.md` |
| **Test Scanner** | Test configuration | `pytest.ini`, `jest.config`, `*_test.go` |
| **Coverage Scanner** | Test coverage | `.coverage`, `coverage.xml` |
| **Dependency Scanner** | Dependencies | `requirements.txt`, `package.json`, `go.mod` |
| **Security Scanner** | Security configuration | `.env.example`, `SECURITY.md` |

### 3.3 Analyzers

Process raw scan data into structured knowledge.

#### 3.3.1 Language Analyzer

Detects programming languages and their distribution.

**Detection Method**:
```
For each file in repository:
  1. Get file extension
  2. Map extension to language (using language map)
  3. Count files per language
  4. Calculate lines of code per language
  5. Determine primary language (by LOC)
```

**Supported Languages**:
| Language | Extensions | Confidence |
|----------|-----------|------------|
| Python | `.py` | High |
| TypeScript | `.ts`, `.tsx` | High |
| JavaScript | `.js`, `.jsx` | High |
| Go | `.go` | High |
| Rust | `.rs` | High |
| Java | `.java` | High |
| C# | `.cs` | High |
| Shell | `.sh`, `.bash` | Medium |
| YAML | `.yaml`, `.yml` | Low (config) |
| JSON | `.json` | Low (config) |

#### 3.3.2 Framework Analyzer

Detects frameworks and libraries.

**Detection Method**:
```
For each dependency file:
  1. Parse dependency declarations
  2. Match against known framework signatures
  3. Detect framework version
  4. Identify framework category (web, test, build, etc.)
```

**Known Frameworks**:
| Framework | Detection Signal | Category |
|-----------|-----------------|----------|
| FastAPI | `fastapi` in dependencies | Web |
| Django | `django` in dependencies | Web |
| Flask | `flask` in dependencies | Web |
| Express | `express` in dependencies | Web |
| Next.js | `next` in dependencies | Web |
| React | `react` in dependencies | Frontend |
| Vue | `vue` in dependencies | Frontend |
| pytest | `pytest` in dependencies | Test |
| Jest | `jest` in dependencies | Test |
| SQLAlchemy | `sqlalchemy` in dependencies | ORM |

#### 3.3.3 Architecture Analyzer

Detects architectural patterns.

**Detection Method**:
```
Analyze directory structure:
  If has "src/" and "tests/": Standard layout
  If has "cmd/": Go CLI pattern
  If has "services/": Microservices pattern
  If has "modules/": Modular pattern
  If has "plugins/": Plugin-based pattern

Analyze file patterns:
  If has "main.py" or "app.py": Python application
  If has "index.ts": TypeScript application
  If has "Dockerfile": Containerized
  If has "docker-compose.yml": Multi-service
```

**Architecture Patterns**:
| Pattern | Detection Criteria |
|---------|-------------------|
| Monolith | Single entry point, no service separation |
| Microservices | Multiple services, independent deployment |
| Modular Monolith | Single deployment, clear module boundaries |
| Serverless | Lambda/Function handlers, no server |
| CLI | Command-line interface, no HTTP server |

#### 3.3.4 Documentation Analyzer

Assesses documentation quality.

**Metrics**:
| Metric | Weight | Calculation |
|--------|--------|-------------|
| README exists | 20% | Boolean |
| README quality | 15% | Length, sections, code examples |
| API docs exist | 20% | OpenAPI/Swagger file |
| Code comments | 10% | Comment density |
| CHANGELOG exists | 10% | Boolean |
| CONTRIBUTING exists | 10% | Boolean |
| Architecture docs | 15% | `docs/` or `architecture/` exists |

#### 3.3.5 Test Analyzer

Assesses test coverage and quality.

**Metrics**:
| Metric | Weight | Calculation |
|--------|--------|-------------|
| Test files exist | 20% | `*_test.*`, `test_*.*`, `*.test.*` |
| Test framework detected | 15% | pytest, jest, go test |
| Test configuration | 15% | Config files exist |
| Test coverage report | 25% | Coverage files exist |
| Test-to-code ratio | 25% | Test LOC / Source LOC |

#### 3.3.6 CI/CD Analyzer

Detects continuous integration and deployment pipelines.

**Detection**:
| CI System | Detection File |
|-----------|---------------|
| GitHub Actions | `.github/workflows/*.yml` |
| GitLab CI | `.gitlab-ci.yml` |
| Jenkins | `Jenkinsfile` |
| CircleCI | `.circleci/config.yml` |
| Travis CI | `.travis.yml` |
| Azure DevOps | `azure-pipelines.yml` |

**Analysis**:
- Pipeline stages (build, test, deploy)
- Trigger conditions (push, PR, schedule)
- Deployment targets
- Security scanning integration

#### 3.3.7 Docker Analyzer

Detects container configuration.

**Analysis**:
- Base image detection
- Port mappings
- Volume mounts
- Multi-stage build detection
- Image size estimation
- Security best practices

#### 3.3.8 Dependency Analyzer

Analyzes dependency health and security.

**Analysis**:
- Total dependency count
- Direct vs transitive dependencies
- Outdated dependencies
- Known vulnerabilities (via advisory databases)
- License compatibility
- Dependency age and maintenance status

#### 3.3.9 Security Analyzer

Detects security configuration and potential issues.

**Checks**:
| Check | Severity | Description |
|-------|----------|-------------|
| Hardcoded secrets | Critical | API keys, passwords in code |
| .env committed | Critical | Environment files in repo |
| No .gitignore | Warning | Missing gitignore |
| No SECURITY.md | Info | Missing security policy |
| Debug mode | Warning | Debug flags enabled |
| Verbose errors | Warning | Stack traces exposed |

### 3.4 Scorer

Calculates repository health scores based on analyzer outputs.

#### 3.4.1 Health Score Formula

```
Health Score = Σ (Category Score × Category Weight)

Where:
  Category Score = Σ (Metric Score × Metric Weight) / Σ Metric Weight
  Score Range = 0.0 - 1.0 (0 = worst, 1 = best)
```

#### 3.4.2 Category Weights

| Category | Weight | Rationale |
|----------|--------|-----------|
| Documentation | 15% | Essential for maintainability |
| Testing | 20% | Critical for quality |
| Security | 25% | Critical for healthcare |
| Architecture | 15% | Important for scalability |
| Dependencies | 10% | Important for stability |
| CI/CD | 10% | Important for delivery |
| Code Quality | 5% | Supporting metric |

#### 3.4.3 Score Thresholds

| Score Range | Rating | Action |
|------------|--------|--------|
| 0.9 - 1.0 | Excellent | No action needed |
| 0.7 - 0.89 | Good | Minor improvements recommended |
| 0.5 - 0.69 | Fair | Improvements required |
| 0.3 - 0.49 | Poor | Significant improvements required |
| 0.0 - 0.29 | Critical | Immediate action required |

### 3.5 Reporter

Generates discovery reports and notifications.

**Report Types**:
| Report | Frequency | Audience |
|--------|-----------|----------|
| Full Ecosystem Report | Daily | Platform Architects |
| Repository Health Report | Weekly | Team Leads |
| Security Findings | On detection | Security Team |
| Certification Readiness | On-demand | Module Owners |
| Trend Analysis | Monthly | Platform Architects |

---

## 4. DISCOVERY WORKFLOW

```
┌──────────────┐
│  Trigger      │
│  (Schedule/   │
│   Event)      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Identify     │
│  Target       │──── Full Scan: All repositories
│  Repositories │──── Incremental: Changed only
└──────┬───────┘──── On-Demand: Specific repo
       │
       ▼
┌──────────────┐
│  Scan         │
│  Repository   │──── File system analysis
│  Structure    │──── Dependency parsing
└──────┬─────────────── Metadata extraction
       │
       ▼
┌──────────────┐
│  Run          │
│  Analyzers    │──── Language detection
│  in           │──── Framework detection
│  Parallel     │──── Architecture analysis
└──────┬─────────────── Documentation analysis
       │                Test analysis
       │                Security analysis
       │
       ▼
┌──────────────┐
│  Calculate    │
│  Health       │──── Category scores
│  Score        │──── Overall score
└──────┬─────────────── Trend comparison
       │
       ▼
┌──────────────┐
│  Update       │
│  Knowledge    │──── Add/update nodes
│  Graph        │──── Add/update relationships
└──────┬─────────────── Update metrics
       │
       ▼
┌──────────────┐
│  Update       │
│  Registries   │──── Repository Registry
│               │──── Service Registry
└──────┬─────────────── API Registry
       │
       ▼
┌──────────────┐
│  Generate     │
│  Reports      │──── Health reports
│  & Notify     │──── Finding alerts
└──────────────┘──── Trend updates
```

---

## 5. DISCOVERY OUTPUT SCHEMA

### 5.1 Discovery Result

```yaml
discovery_result:
  id: UUIDv4
  repository: String             # Repository name
  scan_type: Enum                # full, incremental, on-demand
  scan_id: UUIDv4
  started_at: Timestamp
  completed_at: Timestamp
  duration_seconds: Integer
  status: Enum                   # success, partial, failed
  
  metadata:
    language:
      primary: String
      distribution:
        - language: String
          percentage: Float
          loc: Integer
    framework:
      name: String
      version: String
    architecture:
      pattern: String
      confidence: Float
  
  documentation:
    score: Float
    findings:
      - type: String
        severity: String
        message: String
  
  testing:
    score: Float
    test_framework: String
    test_files: Integer
    coverage_available: Boolean
    coverage_percent: Float
  
  security:
    score: Float
    findings:
      - type: String
        severity: String
        file: String
        line: Integer
        message: String
  
  dependencies:
    score: Float
    total: Integer
    direct: Integer
    transitive: Integer
    outdated: Integer
    vulnerable: Integer
  
  ci_cd:
    score: Float
    system: String
    stages: List[String]
    deployment_configured: Boolean
  
  docker:
    detected: Boolean
    base_image: String
    ports: List[Integer]
    multi_stage: Boolean
  
  health_score:
    overall: Float
    documentation: Float
    testing: Float
    security: Float
    architecture: Float
    dependencies: Float
    ci_cd: Float
  
  findings:
    - id: UUIDv4
      category: String
      type: String
      severity: Enum            # critical, high, medium, low, info
      message: String
      file: String
      line: Integer
      recommendation: String
  
  manifest:
    present: Boolean
    valid: Boolean
    validation_errors: List[String]
```

---

## 6. SCANNER CONFIGURATION

### 6.1 Repository Selection

```yaml
discovery:
  repositories:
    include:
      - "*"                      # All repositories
    exclude:
      - ".git"
      - "node_modules"
      - "__pycache__"
      - ".venv"
      - "venv"
      - "dist"
      - "build"
      - ".next"
      - ".nuxt"
    max_file_size: 1048576       # 1MB
    max_files: 10000
    follow_symlinks: false
```

### 6.2 Analyzer Configuration

```yaml
analyzers:
  language:
    enabled: true
    min_confidence: 0.7
  
  framework:
    enabled: true
    known_frameworks:
      - name: fastapi
        signals: ["fastapi"]
        category: web
      - name: django
        signals: ["django"]
        category: web
  
  architecture:
    enabled: true
    patterns:
      - name: microservices
        signals: ["services/", "docker-compose.yml"]
      - name: modular_monolith
        signals: ["modules/", "src/"]
  
  documentation:
    enabled: true
    required_files:
      - README.md
    recommended_files:
      - CHANGELOG.md
      - CONTRIBUTING.md
      - LICENSE
  
  testing:
    enabled: true
    test_patterns:
      - "test_*.py"
      - "*_test.py"
      - "*.test.ts"
      - "*.test.js"
      - "*_test.go"
  
  security:
    enabled: true
    secret_patterns:
      - pattern: "password\\s*=\\s*['\"]"
        severity: critical
      - pattern: "api_key\\s*=\\s*['\"]"
        severity: critical
      - pattern: "secret\\s*=\\s*['\"]"
        severity: critical
  
  dependencies:
    enabled: true
    advisory_database: "https://github.com/advisories"
  
  ci_cd:
    enabled: true
  
  docker:
    enabled: true
```

---

## 7. INCREMENTAL DISCOVERY

### 7.1 Change Detection

Incremental discovery only scans repositories that have changed since the last full scan.

**Change Detection Methods**:
| Method | Description | Reliability |
|--------|-------------|-------------|
| Git commit timestamp | Check if new commits exist | High |
| Git file diff | Check which files changed | High |
| Manifest hash | Check if manifest changed | High |
| Webhook trigger | Repository notifies of changes | High |

### 7.2 Incremental Scope

When changes are detected:
1. Full scan of changed files
2. Re-analysis of affected analyzers only
3. Health score recalculation
4. Knowledge graph update for changed entities

---

## 8. PLUGIN ARCHITECTURE

### 8.1 Custom Analyzers

The Discovery Engine supports custom analyzers via plugins.

```python
# Example custom analyzer interface
class DiscoveryAnalyzer:
    name: str
    description: str
    version: str
    
    def can_analyze(self, repository: Repository) -> bool:
        """Check if this analyzer can handle the repository."""
        pass
    
    def analyze(self, repository: Repository, scan_result: ScanResult) -> AnalysisResult:
        """Perform analysis and return results."""
        pass
    
    def get_score(self, analysis: AnalysisResult) -> float:
        """Calculate score from analysis results."""
        pass
```

### 8.2 Built-in vs Plugin Analyzers

| Type | Examples | Maintenance |
|------|----------|-------------|
| Built-in | Language, Framework, Architecture | Platform-Core team |
| Plugin | Language-specific (Go, Rust) | Community |
| Plugin | Domain-specific (HL7, FHIR) | Healthcare team |
| Plugin | Custom scoring | Organization-specific |

---

## 9. PERFORMANCE SPECIFICATIONS

### 9.1 Scan Performance

| Repository Size | Full Scan Time | Incremental Scan Time |
|----------------|---------------|----------------------|
| Small (< 100 files) | < 30 seconds | < 5 seconds |
| Medium (100-1000 files) | < 2 minutes | < 15 seconds |
| Large (1000-10000 files) | < 10 minutes | < 1 minute |
| Very Large (> 10000 files) | < 30 minutes | < 5 minutes |

### 9.2 Resource Limits

| Resource | Limit |
|----------|-------|
| Max concurrent scans | 5 |
| Max memory per scan | 512 MB |
| Max CPU per scan | 1 core |
| Max scan duration | 60 minutes |

---

## 10. ERROR HANDLING

| Error Type | Handling |
|-----------|----------|
| Repository inaccessible | Log error, skip repository, alert team |
| File permission denied | Log warning, skip file, continue |
| Dependency parse failure | Log error, partial analysis |
| Timeout | Log error, partial results |
| Disk full | Log critical, pause scanning |

---

## 11. REPORTING

### 11.1 Ecosystem Health Report

```yaml
ecosystem_health_report:
  generated_at: Timestamp
  total_repositories: Integer
  scanned_repositories: Integer
  
  health_distribution:
    excellent: Integer
    good: Integer
    fair: Integer
    poor: Integer
    critical: Integer
  
  average_health_score: Float
  
  top_repositories:
    - name: String
      score: Float
  
  bottom_repositories:
    - name: String
      score: Float
      issues: List[String]
  
  findings_summary:
    critical: Integer
    high: Integer
    medium: Integer
    low: Integer
    info: Integer
  
  trends:
    health_score_change: Float
    new_repositories: Integer
    deprecated_repositories: Integer
```

### 11.2 Repository Health Report

```yaml
repository_health_report:
  repository: String
  generated_at: Timestamp
  health_score: Float
  rating: String
  
  category_scores:
    documentation: Float
    testing: Float
    security: Float
    architecture: Float
    dependencies: Float
    ci_cd: Float
  
  findings:
    - category: String
      severity: String
      message: String
      recommendation: String
  
  recommendations:
    - priority: Integer
      category: String
      message: String
      estimated_effort: String
  
  comparison:
    previous_score: Float
    score_change: Float
    rank: Integer
    percentile: Integer
```

---

*Document generated as part of Platform-Core V2.0 Bootstrap Program — Phase 6*
*Constitution Reference: Articles III, IV, X*
