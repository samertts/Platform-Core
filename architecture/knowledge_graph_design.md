# PLATFORM KNOWLEDGE MODEL

**Document**: Ecosystem Knowledge Graph Design
**Version**: 1.0.0
**Date**: 2026-06-25
**Status**: DESIGN
**Constitution Reference**: Article III — Platform Knowledge

---

## 1. OVERVIEW

The Platform Knowledge Graph is the interconnected map of every entity in the Unified Healthcare Platform ecosystem. It enables Platform-Core to understand, govern, and continuously improve the ecosystem by maintaining complete knowledge of all relationships, dependencies, and interactions.

**Purpose**:
- Enable ecosystem-wide impact analysis
- Support automated governance decisions
- Provide real-time ecosystem health visibility
- Enable intelligent recommendations
- Support certification and compliance

---

## 2. GRAPH ARCHITECTURE

### 2.1 Graph Model

The knowledge graph uses a **property graph model** where:
- **Nodes** represent entities (Repository, Service, API, Event, Device, etc.)
- **Edges** represent relationships (owns, depends-on, publishes, consumes, etc.)
- **Properties** store attributes on both nodes and edges

### 2.2 Storage Technology

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Primary Graph Store | Apache AGE (PostgreSQL extension) | Graph queries on existing PostgreSQL |
| Cache Layer | Redis Graph | Real-time query caching |
| Query Language | Cypher (via Apache AGE) | Graph traversal queries |
| API Layer | GraphQL | Flexible graph querying |

### 2.3 Why Not a Dedicated Graph Database?

Platform-Core uses PostgreSQL with Apache AGE extension rather than a dedicated graph database (Neo4j, TigerGraph) for these reasons:
1. **Operational simplicity** — One database to manage
2. **Transactional consistency** — ACID guarantees across registries and graph
3. **Cost** — No additional licensing
4. **Backup** — Inherits PostgreSQL backup infrastructure
5. **Scalability** — PostgreSQL scales vertically and with read replicas

---

## 3. NODE TYPES

### 3.1 Primary Entity Nodes

| Node Type | Label | Properties |
|-----------|-------|------------|
| Repository | `Repository` | id, name, slug, type, status, maturity, owner |
| Module | `Module` | id, name, slug, status, maturity, version |
| Service | `Service` | id, name, type, status, version, port |
| API | `API` | id, name, type, version, base_path, authentication |
| Event | `Event` | id, name, type, version, category |
| Device | `Device` | id, name, type, manufacturer, model, protocol |
| Driver | `Driver` | id, name, protocol, version |
| Workflow | `Workflow` | id, name, version, status |
| Policy | `Policy` | id, name, type, enforcement, scope |
| Plugin | `Plugin` | id, name, type, version, status |
| Certification | `Certification` | id, level, status, assessed_at, expires_at |
| Standard | `Standard` | id, name, version, level |
| Team | `Team` | id, name, organization |

### 3.2 Supporting Nodes

| Node Type | Label | Properties |
|-----------|-------|------------|
| Schema | `Schema` | id, name, version, format |
| Contract | `Contract` | id, name, type, version |
| Location | `Location` | id, site, building, room |
| Dependency | `Dependency` | id, name, type, version |
| Finding | `Finding` | id, type, severity, status |
| Evidence | `Evidence` | id, type, source, timestamp |
| Metric | `Metric` | id, name, value, unit, timestamp |
| Decision | `Decision` | id, type, rationale, timestamp |

---

## 4. RELATIONSHIP TYPES

### 4.1 Structural Relationships

These define the static structure of the ecosystem.

| Relationship | Source → Target | Description | Properties |
|-------------|----------------|-------------|------------|
| `OWNS` | Repository → Module | Repository contains module | |
| `OWNS` | Repository → Service | Repository contains service | |
| `OWNS` | Repository → API | Repository exposes API | |
| `OWNS` | Repository → Event | Repository publishes event | |
| `PROVIDES` | Module → Service | Module provides service | |
| `EXPOSES` | Module → API | Module exposes API | |
| `EXPOSES` | Service → API | Service exposes API | |
| `PUBLISHES` | Service → Event | Service publishes event | |
| `BELONGS_TO` | Service → Module | Service belongs to module | |
| `BELONGS_TO` | Module → Repository | Module belongs to repository | |

### 4.2 Dependency Relationships

These define how entities depend on each other.

| Relationship | Source → Target | Description | Properties |
|-------------|----------------|-------------|------------|
| `DEPENDS_ON` | Repository → Repository | Repository depends on another | version, critical |
| `DEPENDS_ON` | Service → Service | Service depends on another | version, critical |
| `DEPENDS_ON` | Module → Module | Module depends on another | version, critical |
| `DEPENDS_ON` | Repository → External | External dependency | type, version |
| `REQUIRES` | Service → API | Service requires specific API | version |
| `REQUIRES` | Module → Service | Module requires service | version, critical |

### 4.3 Communication Relationships

These define how entities communicate.

| Relationship | Source → Target | Description | Properties |
|-------------|----------------|-------------|------------|
| `CONSUMES` | Service → Event | Service consumes event | frequency |
| `CONSUMES` | Workflow → Event | Workflow triggered by event | |
| `TRIGGERS` | Event → Workflow | Event triggers workflow | |
| `CALLS` | Service → Service | Service calls another | protocol, frequency |
| `CALLS` | API → API | API depends on another | version |

### 4.4 Device Relationships

These define device ecosystem connections.

| Relationship | Source → Target | Description | Properties |
|-------------|----------------|-------------|------------|
| `USES_DRIVER` | Device → Driver | Device uses specific driver | |
| `IMPLEMENTS` | Driver → Protocol | Driver implements protocol | version |
| `COMMUNICATES_VIA` | Device → Protocol | Device uses protocol | version |
| `HAS_CAPABILITY` | Device → Capability | Device has capability | parameters |
| `LOCATED_AT` | Device → Location | Device at location | |
| `ADAPTS` | Adapter → Protocol | Adapter handles protocol | |

### 4.5 Governance Relationships

These define governance and compliance connections.

| Relationship | Source → Target | Description | Properties |
|-------------|----------------|-------------|------------|
| `CERTIFIES` | Certification → Module | Module certified | level, scope |
| `GOVERNS` | Policy → Service | Policy governs service | |
| `GOVERNS` | Policy → API | Policy governs API | |
| `VIOLATES` | Finding → Policy | Finding violates policy | severity |
| `HAS_EVIDENCE` | Certification → Evidence | Certification has evidence | type |
| `OWNED_BY` | Repository → Team | Repository owned by team | |
| `OWNED_BY` | Service → Team | Service owned by team | |

### 4.6 Evolution Relationships

These define versioning and evolution connections.

| Relationship | Source → Target | Description | Properties |
|-------------|----------------|-------------|------------|
| `VERSION_OF` | API → API | API version of another | |
| `VERSION_OF` | Event → Event | Event version of another | |
| `EXTENDS` | Service → Service | Service extends another | |
| `SUPERSEDES` | API → API | API replaces another | |
| `SUPERSEDES` | Event → Event | Event replaces another | |
| `MIGRATES_TO` | Repository → Repository | Repository migration | |

---

## 5. GRAPH QUERIES

### 5.1 Impact Analysis

**Query**: "If I change Event X, which services and repositories are affected?"

```cypher
MATCH (e:Event {name: $event_name})
      <-[:CONSUMES]-(s:Service)
      <-[:PROVIDES]-(m:Module)
      <-[:OWNS]-(r:Repository)
RETURN DISTINCT r.name, m.name, s.name
```

### 5.2 Dependency Chain

**Query**: "What is the full dependency chain of Repository X?"

```cypher
MATCH path = (r:Repository {name: $repo_name})
             -[:DEPENDS_ON*1..5]->(dep:Repository)
RETURN path
```

### 5.3 Service Health

**Query**: "Show me all services that depend on Service X and their health status."

```cypher
MATCH (s:Service {name: $service_name})
      <-[:DEPENDS_ON]-(consumer:Service)
RETURN consumer.name, consumer.status, consumer.health_score
```

### 5.4 Certification Status

**Query**: "Show me all modules and their certification status."

```cypher
MATCH (m:Module)
      OPTIONAL MATCH (c:Certification)-[:CERTIFIES]->(m)
RETURN m.name, m.maturity, c.level, c.status, c.expires_at
```

### 5.5 Ecosystem Overview

**Query**: "Show me the complete ecosystem map."

```cypher
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, type(r), m
```

### 5.6 Orphan Detection

**Query**: "Find services that are not referenced by any API or event."

```cypher
MATCH (s:Service)
WHERE NOT (s)-[:EXPOSES]->(:API)
  AND NOT (s)-[:PUBLISHES]->(:Event)
  AND NOT (s)-[:CONSUMES]->(:Event)
RETURN s.name, s.status
```

### 5.7 Circular Dependency Detection

**Query**: "Find circular dependencies between repositories."

```cypher
MATCH path = (r:Repository)-[:DEPENDS_ON*2..10]->(r)
RETURN DISTINCT [node IN nodes(path) | node.name] AS cycle
```

### 5.8 Coverage Analysis

**Query**: "Which healthcare domains are covered by the platform?"

```cypher
MATCH (r:Repository)-[:OWNS]->(m:Module)
OPTIONAL MATCH (m)-[:PROVIDES]->(s:Service)
OPTIONAL MATCH (m)-[:EXPOSES]->(a:API)
RETURN r.name AS repository,
       m.name AS module,
       count(DISTINCT s) AS services,
       count(DISTINCT a) AS apis
```

---

## 6. GRAPH MAINTENANCE

### 6.1 Automatic Updates

The knowledge graph is automatically updated when:

| Trigger | Action |
|---------|--------|
| Manifest submitted | Add/update Repository, Module, Service, API, Event nodes |
| Manifest updated | Update all dependent nodes |
| Service deployed | Update Service status and health |
| Event published | Update Event metrics |
| Certification completed | Add/update Certification node |
| Policy created | Add/update Policy node |

### 6.2 Scheduled Maintenance

| Task | Frequency | Description |
|------|-----------|-------------|
| Orphan detection | Daily | Find unreferenced entities |
| Circular dependency scan | Weekly | Detect dependency cycles |
| Stale knowledge removal | Monthly | Remove outdated entries |
| Health score recalculation | Hourly | Update all health scores |
| Graph integrity check | Daily | Verify referential integrity |

### 6.3 Knowledge Freshness

| Knowledge Type | Maximum Staleness | Refresh Method |
|---------------|-------------------|----------------|
| Repository metadata | 24 hours | Manifest re-validation |
| Service status | 5 minutes | Health check polling |
| API metrics | 1 minute | Metrics collection |
| Event metrics | 1 minute | Metrics collection |
| Device status | 30 seconds | Device heartbeat |
| Certification status | 24 hours | Certification engine |
| Policy status | 1 hour | Policy engine |

---

## 7. GRAPH API

### 7.1 REST API

```
GET    /knowledge/graph                         # Full graph (paginated)
GET    /knowledge/graph/{node_type}              # All nodes of type
GET    /knowledge/graph/{node_type}/{id}         # Single node with relationships
GET    /knowledge/graph/{node_type}/{id}/neighbors  # Neighbors
POST   /knowledge/graph/query                    # Custom Cypher query
GET    /knowledge/graph/impact/{entity_type}/{id}   # Impact analysis
GET    /knowledge/graph/dependencies/{id}        # Dependency chain
GET    /knowledge/graph/health                   # Ecosystem health overview
```

### 7.2 GraphQL API

```graphql
type Query {
  repositories(status: String): [Repository]
  services(name: String, status: String): [Service]
  apis(type: String, status: String): [API]
  events(type: String, status: String): [Event]
  impactAnalysis(entityType: String!, id: ID!): ImpactResult
  dependencyChain(id: ID!, depth: Int): [Dependency]
  ecosystemHealth: HealthOverview
}
```

### 7.3 Real-time Updates

The knowledge graph supports WebSocket subscriptions for real-time updates:

```graphql
subscription {
  entityChanged(entityType: "Service") {
    id
    name
    status
    healthScore
  }
}
```

---

## 8. GRAPH ANALYTICS

### 8.1 Ecosystem Metrics

| Metric | Calculation | Purpose |
|--------|-------------|---------|
| **Ecosystem Health Score** | Average of all entity health scores | Overall platform health |
| **Dependency Depth** | Longest dependency chain | Architecture complexity |
| **Coupling Score** | Average dependencies per entity | Inter-entity coupling |
| **Coverage Score** | Domains covered / Total domains | Feature completeness |
| **Maturity Distribution** | Count by maturity level | Ecosystem maturity |
| **Certification Coverage** | Certified modules / Total modules | Compliance status |

### 8.2 Trend Analysis

Track these metrics over time:
- Dependency graph growth
- New entity creation rate
- Entity retirement rate
- Health score trends
- Certification pass rate
- Policy violation trends

### 8.3 Anomaly Detection

- Sudden increase in dependencies
- Health score degradation
- New circular dependencies
- Certification expiration approaching
- Policy violations increasing

---

## 9. GRAPH SECURITY

### 9.1 Access Control

| Operation | Platform Architect | Team Lead | Developer | Viewer |
|-----------|-------------------|-----------|-----------|--------|
| Read graph | Yes | Yes | Yes | Yes |
| Query graph | Yes | Yes | Yes | Yes |
| Modify graph | Yes | Yes | No | No |
| Delete nodes | Yes | No | No | No |
| Execute custom queries | Yes | Yes | No | No |

### 9.2 Data Sensitivity

| Data Type | Sensitivity | Access Level |
|-----------|-------------|--------------|
| Repository metadata | Internal | All users |
| Service health | Internal | All users |
| API metrics | Internal | All users |
| Certification details | Confidential | Team leads+ |
| Policy rules | Confidential | Platform architects |
| Findings | Confidential | Team leads+ |
| Security metrics | Restricted | Platform architects |

---

## 10. INTEGRATION WITH PLATFORM-CORE

### 10.1 Governance Engine Integration

The Governance Engine queries the knowledge graph to:
- Assess impact of proposed changes
- Verify compliance with policies
- Check certification status
- Evaluate architectural fitness

### 10.2 Certification Engine Integration

The Certification Engine uses the knowledge graph to:
- Verify all required services exist
- Check dependency health
- Validate API contracts
- Assess ecosystem readiness

### 10.3 Discovery Engine Integration

The Discovery Engine populates the knowledge graph with:
- Repository structure
- Service topology
- API contracts
- Event schemas
- Dependency relationships

### 10.4 Operational Intelligence Integration

Operational Intelligence reads from the knowledge graph to:
- Calculate health scores
- Identify bottlenecks
- Detect anomalies
- Generate recommendations

---

## 11. GRAPH SCALABILITY

### 11.1 Estimated Graph Size

| Entity Type | Initial (Year 1) | Growth (Year 3) | National (Year 5) |
|-------------|-------------------|------------------|--------------------|
| Repositories | 10 | 50 | 200 |
| Services | 30 | 200 | 1,000 |
| APIs | 50 | 400 | 2,000 |
| Events | 100 | 800 | 4,000 |
| Devices | 20 | 200 | 2,000 |
| Relationships | 500 | 5,000 | 50,000 |

### 11.2 Performance Targets

| Query Type | Target Latency |
|-----------|----------------|
| Single node lookup | < 10ms |
| 1-hop neighbor query | < 50ms |
| 3-hop impact analysis | < 500ms |
| Full ecosystem overview | < 2s |
| Custom Cypher query | < 5s |

---

*Document generated as part of Platform-Core V2.0 Bootstrap Program — Phase 5*
*Constitution Reference: Article III — Platform Knowledge*
