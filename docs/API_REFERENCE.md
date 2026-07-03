# API Reference

This document provides an overview of Platform-Core's public API modules, key classes, and interfaces.

## Package Structure

```
platform_core/
    runtime/        Runtime engine (container, config, plugins, events, identity, kernel)
    workflow/       Workflow engine (pipeline, steps, context, results)
    governance/     Governance framework (compliance, quality, decisions, risk)
    knowledge/      Knowledge graph (graph store, queries, AI layer)
    discovery/      Discovery engine (scanning, scoring, analysis, reporting)
    doctor/         Health diagnostics (checks, runners, reports)
    scheduler/      Task scheduling (engine, queue, tasks)
    plugins/        Plugin system (plugin base, manager, registry)
    events/         Event system (event bus, events, subscribers)
    services/       Service framework (registry, descriptor, lifetime)
    config/         Configuration (settings, YAML loading)
    contracts/      Contract definitions (base contracts)
    engine/         Base engine abstraction
    cli/            Command-line interface
    api/            API layer
    frontend/       Frontend types and hooks
```

## Runtime Module

### ServiceContainer

Dependency injection container for managing service lifetimes.

```python
from platform_core.runtime.container import ServiceContainer

container = ServiceContainer()

# Register a singleton service (one instance shared across resolvents)
container.register_singleton(IMyService, MyServiceImpl)

# Register a transient service (new instance per resolution)
container.register_transient(IMyService, MyServiceImpl)

# Resolve a service
service = container.resolve(IMyService)

# Check if a service is registered
if container.contains(IMyService):
    service = container.resolve(IMyService)

# Clear all registrations
container.clear()
```

**Methods:**

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `register_singleton` | `interface: type`, `implementation: type \| Callable` | `None` | Register a singleton service |
| `register_transient` | `interface: type`, `implementation: type \| Callable` | `None` | Register a transient service |
| `resolve` | `interface: type` | `Any` | Resolve a service by interface type |
| `contains` | `interface: type` | `bool` | Check if a service is registered |
| `clear` | — | `None` | Remove all registrations |

**Exceptions:**

- `ServiceAlreadyRegisteredError` — Raised when registering a service that already exists
- `ServiceNotRegisteredError` — Raised when resolving an unregistered service

### ConfigurationEngine

Configuration management with schema validation.

```python
from platform_core.runtime.config import ConfigurationEngine

engine = ConfigurationEngine()
config = engine.load("platform.yaml")
```

### PluginManager

Plugin lifecycle management.

```python
from platform_core.plugins.manager import PluginManager
from platform_core.plugins.plugin import Plugin

class MyPlugin(Plugin):
    @property
    def name(self) -> str:
        return "my_plugin"

    def initialize(self) -> None:
        pass

manager = PluginManager()
manager.load(MyPlugin())
```

**Methods:**

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `load` | `plugin: Plugin` | `None` | Initialize and register a plugin |

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `registry` | `PluginRegistry` | Access the plugin registry |

## Workflow Module

### WorkflowEngine

Pipeline-based workflow execution engine.

```python
from platform_core.workflow.engine import WorkflowEngine
from platform_core.workflow.context import WorkflowContext
from platform_core.workflow.step import WorkflowStep
from platform_core.workflow.result import WorkflowResult

class MyStep(WorkflowStep):
    @property
    def name(self) -> str:
        return "my_step"

    def execute(self, context: WorkflowContext) -> WorkflowResult:
        value = context.get("input")
        return WorkflowResult.ok(output=value * 2)

engine = WorkflowEngine()
engine.add_step(MyStep())

context = WorkflowContext(data={"input": 21})
result = engine.run(context)

print(result.success)  # True
print(result.data)     # {"output": 42}
```

**Methods:**

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_step` | `step: WorkflowStep` | `WorkflowEngine` | Add a step to the pipeline (chainable) |
| `run` | `context: WorkflowContext \| None` | `WorkflowResult` | Execute the workflow pipeline |
| `clear` | — | `None` | Remove all steps from the pipeline |

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `pipeline` | `WorkflowPipeline` | Access the underlying pipeline |

### WorkflowStep

Abstract base class for workflow steps.

```python
from abc import ABC, abstractmethod
from platform_core.workflow.context import WorkflowContext
from platform_core.workflow.result import WorkflowResult

class WorkflowStep(ABC):
    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def execute(self, context: WorkflowContext) -> WorkflowResult:
        raise NotImplementedError
```

### WorkflowContext

Shared mutable context passed between workflow steps.

```python
from platform_core.workflow.context import WorkflowContext

context = WorkflowContext(data={"key": "value"})

# Get a value
value = context.get("key")

# Get with default
value = context.get("missing_key", default="fallback")

# Set a value
context.set("new_key", "new_value")

# Check existence
if context.exists("key"):
    print("Key exists")

# Clear all data
context.clear()
```

**Methods:**

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `get` | `key: str`, `default: Any = None` | `Any` | Get a value from the context |
| `set` | `key: str`, `value: Any` | `None` | Set a value in the context |
| `exists` | `key: str` | `bool` | Check if a key exists |
| `clear` | — | `None` | Clear all context data |

### WorkflowResult

Immutable result of a workflow execution.

```python
from platform_core.workflow.result import WorkflowResult
from platform_core.workflow.status import WorkflowStatus

# Successful result
result = WorkflowResult.ok(output="data")
assert result.success is True
assert result.data == {"output": "data"}

# Error result
result = WorkflowResult.error("Something went wrong")
assert result.failed is True
assert result.message == "Something went wrong"
```

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `success` | `bool` | True if status is COMPLETED |
| `failed` | `bool` | True if status is FAILED |

**Class Methods:**

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `ok` | `**data: Any` | `WorkflowResult` | Create a successful result |
| `error` | `message: str`, `**data: Any` | `WorkflowResult` | Create an error result |

## Events Module

### EventBus

Publish-subscribe event system for inter-module communication.

```python
from platform_core.events.event_bus import EventBus
from platform_core.events.event import Event

bus = EventBus()

# Subscribe to an event
def handler(event: Event) -> None:
    print(f"Received: {event.name}")

bus.subscribe("my.event", handler)

# Publish an event
bus.publish(Event(name="my.event", payload={"key": "value"}))

# Unsubscribe
bus.unsubscribe("my.event", handler)
```

**Methods:**

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `subscribe` | `event_name: str`, `callback: Subscriber` | `None` | Register a subscriber for an event |
| `unsubscribe` | `event_name: str`, `callback: Subscriber` | `None` | Remove a subscriber |
| `publish` | `event: Event` | `None` | Publish an event to all subscribers |

### Event

Immutable event data object.

```python
from platform_core.events.event import Event
from datetime import datetime

event = Event(
    name="service.started",
    payload={"service": "auth", "port": 8080}
)

print(event.id)         # Auto-generated UUID
print(event.name)       # "service.started"
print(event.payload)    # {"service": "auth", "port": 8080}
print(event.created_at) # datetime object
```

## Governance Module

### GovernanceEngine

Main orchestrator for governance operations.

```python
from platform_core.governance.engine import GovernanceEngine

engine = GovernanceEngine()

# Run a full review
results = engine.run_full_review(
    repository="my-repo",
    evidence={"coverage_percent": 85.0, "security_passed": True}
)

# Approve a release
decision = engine.approve_release(
    repository="my-repo",
    version="1.0.0",
    approved_by="admin",
    evidence={"coverage_percent": 85.0}
)

# Reject a release
decision = engine.reject_release(
    repository="my-repo",
    version="1.0.0",
    rejected_by="admin",
    rationale="Coverage too low"
)

# Get repository status
status = engine.get_repository_status("my-repo")

# Get governance dashboard
dashboard = engine.get_governance_dashboard()
```

**Methods:**

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `run_full_review` | `repository: str`, `evidence: dict \| None` | `dict[str, Any]` | Execute a comprehensive governance review |
| `approve_release` | `repository: str`, `version: str`, `approved_by: str`, `evidence: dict \| None` | `dict[str, Any]` | Approve a release after quality gates |
| `reject_release` | `repository: str`, `version: str`, `rejected_by: str`, `rationale: str` | `dict[str, Any]` | Reject a release with rationale |
| `get_repository_status` | `repository: str` | `dict[str, Any]` | Get full status for a repository |
| `get_governance_dashboard` | — | `dict[str, Any]` | Get governance metrics overview |

**Components:**

| Component | Type | Description |
|-----------|------|-------------|
| `findings` | `FindingManager` | Manages findings and issues |
| `reviews` | `ReviewManager` | Manages governance reviews |
| `decisions` | `DecisionEngine` | Tracks approval/rejection decisions |
| `recommendations` | `RecommendationEngine` | Generates improvement recommendations |
| `risk` | `RiskEngine` | Assesses risk across categories |
| `compliance` | `ComplianceEngine` | Validates against standards |
| `quality_gates` | `QualityGateEngine` | Evaluates release readiness |
| `constitution` | `ConstitutionEnforcer` | Enforces constitutional rules |
| `registry` | `GovernanceRegistry` | Stores governance events |
| `ai_assistant` | `AIGovernanceAssistant` | AI-powered governance support |

## Knowledge Module

### GraphStore

Thread-safe in-memory graph storage with adjacency lists.

```python
from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.types import Node, Edge, NodeType, RelationshipType

store = GraphStore(max_nodes=10000, max_edges=50000)

# Add nodes
node_a = Node(id="a", node_type=NodeType.CONCEPT, label="Service A")
node_b = Node(id="b", node_type=NodeType.CONCEPT, label="Service B")
store.add_node(node_a)
store.add_node(node_b)

# Add edges
edge = Edge(
    id="e1",
    source_id="a",
    target_id="b",
    relationship_type=RelationshipType.DEPENDS_ON
)
store.add_edge(edge)

# Query
node = store.get_node("a")
neighbors = store.get_neighbors("a")
outgoing = store.get_outgoing_edges("a")
incoming = store.get_incoming_edges("a")

# Statistics
print(f"Nodes: {store.node_count()}, Edges: {store.edge_count()}")

# Snapshot
snapshot = store.snapshot()
```

**Methods:**

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_node` | `node: Node` | `Node` | Add a node to the graph |
| `get_node` | `node_id: str` | `Node` | Get a node by ID |
| `get_node_optional` | `node_id: str` | `Node \| None` | Get a node or None |
| `update_node` | `node: Node` | `Node` | Update an existing node |
| `delete_node` | `node_id: str` | `bool` | Delete a node and its edges |
| `add_edge` | `edge: Edge` | `Edge` | Add an edge to the graph |
| `get_edge` | `edge_id: str` | `Edge` | Get an edge by ID |
| `update_edge` | `edge: Edge` | `Edge` | Update an existing edge |
| `delete_edge` | `edge_id: str` | `bool` | Delete an edge |
| `get_outgoing_edges` | `node_id: str` | `list[Edge]` | Get all outgoing edges from a node |
| `get_incoming_edges` | `node_id: str` | `list[Edge]` | Get all incoming edges to a node |
| `get_neighbors` | `node_id: str` | `list[Node]` | Get all neighbor nodes |
| `get_all_nodes` | — | `list[Node]` | Get all nodes |
| `get_all_edges` | — | `list[Edge]` | Get all edges |
| `get_nodes_by_type` | `node_type: Any` | `list[Node]` | Filter nodes by type |
| `get_edges_by_type` | `rel_type: Any` | `list[Edge]` | Filter edges by type |
| `node_count` | — | `int` | Get node count |
| `edge_count` | — | `int` | Get edge count |
| `snapshot` | — | `dict[str, Any]` | Get a full graph snapshot |
| `clear` | — | `None` | Remove all nodes and edges |

**Exceptions:**

- `NodeNotFoundError` — Raised when a node is not found
- `EdgeNotFoundError` — Raised when an edge is not found
- `GraphConstraintError` — Raised when graph limits are exceeded

## Discovery Module

### DiscoveryEngine

Orchestrates scanning, analysis, scoring, and reporting.

```python
from platform_core.discovery.engine import DiscoveryEngine
from platform_core.discovery.types import ScanType

engine = DiscoveryEngine()

# Discover a single repository
result = engine.discover(
    repository_path="/path/to/repo",
    repository_name="my-repo",
    scan_type=ScanType.FULL
)

# Discover multiple repositories
results = engine.discover_multiple(
    paths=["/path/to/repo1", "/path/to/repo2"]
)

# Get results
result = engine.get_result("my-repo")
all_results = engine.get_all_results()

# Generate reports
ecosystem_report = engine.get_ecosystem_report()
repo_report = engine.get_repository_report("my-repo")
health_summary = engine.get_health_summary("my-repo")

# Get statistics
stats = engine.get_statistics()
```

**Methods:**

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `discover` | `repository_path: str`, `repository_name: str`, `scan_type: ScanType` | `DiscoveryResult` | Scan and analyze a repository |
| `discover_multiple` | `paths: list[str]`, `scan_type: ScanType` | `list[DiscoveryResult]` | Scan multiple repositories |
| `get_result` | `repository: str` | `DiscoveryResult \| None` | Get scan result for a repository |
| `get_all_results` | — | `list[DiscoveryResult]` | Get all scan results |
| `get_ecosystem_report` | — | `EcosystemReport` | Generate ecosystem-wide report |
| `get_repository_report` | `repository: str` | `RepositoryReport \| None` | Generate repository-specific report |
| `get_health_summary` | `repository: str` | `str` | Get formatted health summary |
| `clear_results` | — | `None` | Clear all stored results |
| `get_statistics` | — | `dict[str, Any]` | Get scan statistics |

## Doctor Module

### DoctorEngine

Health checks and diagnostic engine.

```python
from platform_core.doctor.engine import DoctorEngine
from platform_core.doctor.check_registry import CheckRegistry
from platform_core.engine.context import EngineContext

registry = CheckRegistry()
engine = DoctorEngine(registry)

context = EngineContext()
result = engine.execute(context)

print(result.status)   # EngineStatus.COMPLETED
print(result.payload)  # Health check report
print(result.metrics)  # {"checks": 10, "score": 0.95}
```

## Scheduler Module

### SchedulerEngine

Task queue management and execution.

```python
from platform_core.scheduler.engine import SchedulerEngine

engine = SchedulerEngine()

# Enqueue tasks
from platform_core.scheduler.task import Task
task = Task(action=lambda: print("executed"))
engine.queue.enqueue(task)

# Run all queued tasks
engine.run()
```

## Services Module

### ServiceRegistry

Immutable registry for service descriptors.

```python
from platform_core.services.registry import ServiceRegistry
from platform_core.services.descriptor import ServiceDescriptor

registry = ServiceRegistry()

# Register a service
descriptor = ServiceDescriptor(
    key="my_service",
    implementation=MyServiceImpl,
    lifetime="singleton"
)
registry.register(descriptor)

# Check existence
if registry.exists("my_service"):
    desc = registry.get("my_service")

# Get all services
all_services = registry.all()

# Unregister
registry.unregister("my_service")
```

**Methods:**

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `register` | `descriptor: ServiceDescriptor` | `None` | Register a service descriptor |
| `unregister` | `key: str` | `None` | Remove a service registration |
| `clear` | — | `None` | Remove all registrations |
| `exists` | `key: str` | `bool` | Check if a service is registered |
| `get` | `key: str` | `ServiceDescriptor` | Get a service descriptor by key |
| `all` | — | `tuple[ServiceDescriptor, ...]` | Get all registered descriptors |
