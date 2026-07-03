# Deployment Guide

This guide covers configuring, deploying, and operating Platform-Core in production environments.

## Configuration

### Configuration File

Platform-Core uses a YAML configuration file (`platform.yaml` by default) for runtime settings.

```yaml
# platform.yaml
workspace: /opt/platform-core
config_file: platform.yaml
log_level: INFO
sandbox: true
```

### Configuration Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `workspace` | `Path` | `Path.cwd()` | Root directory for platform operations |
| `config_file` | `Path` | `Path("platform.yaml")` | Path to the configuration file |
| `log_level` | `str` | `"INFO"` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `sandbox` | `bool` | `true` | Enable sandbox mode for isolated execution |

### Configuration Sources

Settings are resolved in the following order:

1. Environment variables
2. Configuration file (`platform.yaml`)
3. Default values

## Environment Variables

Platform-Core can be configured via environment variables using pydantic-settings naming conventions:

| Environment Variable | Setting | Description |
|---------------------|---------|-------------|
| `WORKSPACE` | `workspace` | Root workspace directory |
| `CONFIG_FILE` | `config_file` | Path to configuration file |
| `LOG_LEVEL` | `log_level` | Logging verbosity level |
| `SANDBOX` | `sandbox` | Enable/disable sandbox mode |

Example:

```bash
export WORKSPACE=/opt/platform-core
export LOG_LEVEL=DEBUG
export SANDBOX=false
```

## Logging Setup

### Configuration

Platform-Core uses Python's standard `logging` module. Configure logging in your application:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("platform_core")
```

### Log Levels

| Level | Usage |
|-------|-------|
| `DEBUG` | Detailed diagnostic information |
| `INFO` | General operational messages |
| `WARNING` | Unexpected conditions that don't prevent operation |
| `ERROR` | Failures that prevent specific operations |
| `CRITICAL` | System-level failures requiring immediate attention |

### Production Logging

For production, configure structured logging:

```python
import json
import logging

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())

logging.root.handlers.clear()
logging.root.addHandler(handler)
logging.root.setLevel(logging.INFO)
```

## Health Monitoring

### Doctor System

Platform-Core includes a built-in health check system via the `DoctorEngine`:

```python
from platform_core.doctor.engine import DoctorEngine
from platform_core.doctor.check_registry import CheckRegistry
from platform_core.engine.context import EngineContext

# Create check registry
registry = CheckRegistry()

# Register health checks
from platform_core.doctor.check import Check, CheckResult, CheckStatus

registry.register(Check(
    name="disk_space",
    description="Check available disk space",
    check_fn=lambda: CheckResult(
        status=CheckStatus.PASS,
        message="Disk space OK"
    ),
))

# Run health checks
engine = DoctorEngine(registry)
context = EngineContext()
result = engine.execute(context)

# result.payload contains the health report
# result.metrics contains {"checks": N, "score": 0.0-1.0}
```

### Discovery Health Scores

Use the Discovery Engine to monitor component health:

```python
from platform_core.discovery.engine import DiscoveryEngine

engine = DiscoveryEngine()

# Scan and score a component
result = engine.discover(
    repository_path="/opt/platform-core",
    repository_name="platform-core"
)

# Get health summary
summary = engine.get_health_summary("platform-core")

# Get ecosystem-wide statistics
stats = engine.get_statistics()
# {"total_scanned": 5, "average_score": 0.85, "best_score": 0.95, "worst_score": 0.72}
```

### Governance Dashboard

Monitor governance metrics:

```python
from platform_core.governance.engine import GovernanceEngine

engine = GovernanceEngine()
dashboard = engine.get_governance_dashboard()

# dashboard contains:
# {"total_findings": 12, "total_reviews": 8, "critical_findings": 2, ...}
```

## Production Checklist

### Pre-Deployment

- [ ] All tests pass: `pytest`
- [ ] No linting errors: `ruff check .`
- [ ] Code is formatted: `ruff format --check .`
- [ ] Type checking passes: `mypy .`
- [ ] Coverage meets threshold: `pytest --cov=platform_core`
- [ ] Configuration file is properly set
- [ ] Environment variables are configured
- [ ] Logging level is appropriate (not DEBUG in production)
- [ ] Disk space and system resources are sufficient

### Runtime Configuration

- [ ] `workspace` points to the correct directory
- [ ] `sandbox` mode is configured appropriately
  - `true` for isolated execution (recommended for multi-tenant)
  - `false` for direct system access (single-tenant only)
- [ ] Log rotation is configured at the OS level
- [ ] Monitoring endpoints are accessible

### Security

- [ ] No secrets in configuration files (use environment variables)
- [ ] File permissions are restrictive on config files
- [ ] Network access is limited to required endpoints
- [ ] Audit logging is enabled for governance operations

### Monitoring

- [ ] Health checks are configured and accessible
- [ ] Alerting is set up for critical findings
- [ ] Governance dashboard is monitored
- [ ] Discovery scores are tracked over time

## Scaling Considerations

### Single Instance

For single-instance deployments:

```python
from platform_core.runtime.container import ServiceContainer
from platform_core.governance.engine import GovernanceEngine
from platform_core.knowledge.graph import GraphStore

container = ServiceContainer()
governance = GovernanceEngine()
graph = GraphStore(max_nodes=100000, max_edges=500000)
```

### Thread Safety

The following components are thread-safe:

- `GraphStore` — Uses `threading.RLock` for all operations
- `GovernanceEngine` — Uses `threading.RLock` for state mutations
- `DiscoveryEngine` — Uses `threading.RLock` for result caching

The following components are not thread-safe:

- `ServiceContainer` — Designed for initialization phase only
- `WorkflowEngine` — Single-threaded pipeline execution

### Resource Limits

Configure resource limits based on your workload:

```python
from platform_core.knowledge.graph import GraphStore

# Adjust based on available memory
graph = GraphStore(
    max_nodes=100000,   # ~100MB for 100K nodes
    max_edges=500000    # ~200MB for 500K edges
)
```

## Backup and Recovery

### Knowledge Graph Backup

```python
import json
from platform_core.knowledge.graph import GraphStore

# Export snapshot
snapshot = graph.snapshot()
with open("graph_backup.json", "w") as f:
    json.dump(snapshot, f)
```

### Governance State Backup

Governance state is stored in memory by default. For persistence, implement a custom `GovernanceRegistry` backend that writes to disk or a database.

## Troubleshooting

### High Memory Usage

- Reduce `max_nodes` and `max_edges` in `GraphStore`
- Clear discovery results periodically: `engine.clear_results()`
- Use `graph.clear()` when knowledge graph is no longer needed

### Slow Performance

- Enable DEBUG logging to identify bottlenecks
- Check if sandbox mode is adding overhead
- Profile workflow execution with `cProfile`

### Thread Deadlocks

- Ensure `GraphStore` operations don't nest (uses reentrant lock)
- Avoid calling governance operations from multiple threads simultaneously
- Use `threading.RLock` if implementing custom concurrent components
