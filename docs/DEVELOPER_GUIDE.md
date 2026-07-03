# Developer Guide

This guide covers the development workflow, coding standards, testing practices, and common patterns for contributing to Platform-Core.

## Development Environment Setup

### Prerequisites

- Python 3.11 or later (3.12 recommended)
- Git
- pip

### Setting Up a Development Environment

```bash
# Clone the repository
git clone https://github.com/samertts/Platform-Core.git
cd Platform-Core

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install the package in development mode with all dev dependencies
pip install -e ".[dev]"

# Install the optional YAML dependency
pip install -e ".[yaml]"
```

### Verifying the Setup

```bash
# Run the test suite
pytest

# Run linting
ruff check .

# Run type checking
mypy .
```

## Code Style

Platform-Core enforces strict code quality standards.

### Formatting and Linting

The project uses **ruff** for both linting and formatting:

```bash
# Check for linting errors
ruff check .

# Auto-fix linting errors
ruff check --fix .

# Check formatting
ruff format --check .

# Apply formatting
ruff format .
```

Ruff configuration is in `pyproject.toml`:

- Line length: 100 characters
- Target: Python 3.11
- Enabled rules: `E`, `F`, `I`, `N`, `W`, `UP`

### Type Checking

The project uses **mypy** in strict mode:

```bash
mypy .
```

All code must pass mypy strict mode. Key requirements:

- All functions must have return type annotations
- All function parameters must have type annotations
- Use `from __future__ import annotations` for forward references
- Prefer `X | None` over `Optional[X]`
- Use `collections.abc.Callable` instead of `typing.Callable`

### Import Sorting

Imports are sorted by ruff using isort-compatible rules:

```python
# Standard library imports first
from __future__ import annotations

import threading
from datetime import UTC, datetime
from typing import Any

# Third-party imports second
import yaml
from pydantic import BaseModel

# Local imports last
from platform_core.events.event import Event
from platform_core.workflow.context import WorkflowContext
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=platform_core --cov-report=term-missing

# Run a specific test file
pytest tests/test_workflow.py

# Run a specific test
pytest tests/test_workflow.py::test_workflow_execution

# Run tests matching a pattern
pytest -k "test_workflow"
```

### Test Configuration

Test configuration is in `pyproject.toml`:

- Test path: `tests/`
- Async mode: `auto` (pytest-asyncio)
- Coverage source: `platform_core`
- Branch coverage enabled

### Writing Tests

#### Basic Test

```python
def test_service_container_register_singleton() -> None:
    container = ServiceContainer()
    container.register_singleton(MyInterface, MyImplementation)
    assert container.contains(MyInterface)
```

#### Async Test

```python
import pytest

@pytest.mark.asyncio
async def test_async_workflow() -> None:
    engine = WorkflowEngine()
    result = engine.run(WorkflowContext(data={"key": "value"}))
    assert result.success
```

#### Test with Fixtures

```python
import pytest

@pytest.fixture
def container() -> ServiceContainer:
    c = ServiceContainer()
    c.register_singleton(IMyService, MyServiceImpl)
    return c

def test_resolve_service(container: ServiceContainer) -> None:
    service = container.resolve(IMyService)
    assert service is not None
```

#### Test with Mocks

```python
from unittest.mock import Mock, patch

def test_governance_with_mock() -> None:
    mock_compliance = Mock()
    mock_compliance.validate_all_standards.return_value = []

    engine = GovernanceEngine()
    engine.compliance = mock_compliance

    result = engine.run_full_review("my-repo")
    mock_compliance.validate_all_standards.assert_called_once()
```

### Test Organization

Tests mirror the source structure:

```
tests/
    test_workflow.py          → platform_core/workflow/
    test_events.py            → platform_core/events/
    test_runtime.py           → platform_core/runtime/
    test_governance.py        → platform_core/governance/
```

## Adding a New Module

1. Create the module directory under `platform_core/`:

```bash
mkdir -p platform_core/my_module
```

2. Create `__init__.py`:

```python
"""My module description."""
```

3. Create the main module file:

```python
from __future__ import annotations

from typing import Any


class MyModule:
    """Module for handling my domain logic."""

    def __init__(self) -> None:
        self._state: dict[str, Any] = {}

    def process(self, input_data: str) -> str:
        """Process input data and return result."""
        return f"processed: {input_data}"
```

4. Create a test file:

```python
from platform_core.my_module import MyModule


def test_my_module_process() -> None:
    module = MyModule()
    result = module.process("hello")
    assert result == "processed: hello"
```

5. Add any new dependencies to `pyproject.toml` under `[project.dependencies]`.

## Adding a New Service

1. Define the service interface (if applicable):

```python
# platform_core/my_module/interfaces.py
from abc import ABC, abstractmethod


class IMyService(ABC):
    @abstractmethod
    def do_work(self) -> str:
        raise NotImplementedError
```

2. Implement the service:

```python
# platform_core/my_module/service.py
from platform_core.my_module.interfaces import IMyService


class MyService(IMyService):
    def do_work(self) -> str:
        return "work completed"
```

3. Register with the container:

```python
from platform_core.runtime.container import ServiceContainer
from platform_core.my_module.interfaces import IMyService
from platform_core.my_module.service import MyService

container = ServiceContainer()
container.register_singleton(IMyService, MyService)
```

## Adding a New Test

1. Create a test file in `tests/` following the naming convention `test_<module_name>.py`.

2. Write test functions prefixed with `test_`:

```python
from platform_core.my_module import MyModule


def test_my_feature_basic() -> None:
    module = MyModule()
    assert module.process("input") == "processed: input"


def test_my_feature_edge_case() -> None:
    module = MyModule()
    assert module.process("") == "processed: "
```

3. Run the test to verify:

```bash
pytest tests/test_my_module.py -v
```

## Quality Checks

Run all quality checks before committing:

```bash
# Linting
ruff check .

# Formatting
ruff format --check .

# Type checking
mypy .

# Tests with coverage
pytest --cov=platform_core --cov-report=term-missing
```

## Git Workflow

### Branch Naming

- `feature/<description>` — New features
- `fix/<description>` — Bug fixes
- `docs/<description>` — Documentation changes
- `refactor/<description>` — Code refactoring

### Commit Messages

Use conventional commit format:

```
<type>: <description>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

Examples:

```
feat: add async workflow execution support

Implement async step execution in WorkflowEngine with
proper context propagation and error handling.

Closes #123
```

```
fix: resolve thread safety issue in GraphStore

Add missing lock acquisition in get_neighbors method
to prevent race conditions during concurrent reads.
```

### Pull Request Process

1. Create a feature branch from `main`
2. Make changes and write tests
3. Run all quality checks
4. Push and create a pull request
5. Fill in the PR template
6. Request review

## Debugging Tips

### Using pytest for Debugging

```bash
# Drop into debugger on failure
pytest --pdb

# Show print output
pytest -s

# Verbose output
pytest -vv
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

def my_function() -> None:
    logger.debug("Entering my_function")
    # ... logic ...
    logger.info("Function completed")
```

### Inspecting the Container

```python
container = ServiceContainer()
container.register_singleton(IMyService, MyService)

# Check if a service is registered
assert container.contains(IMyService)

# Resolve and inspect
service = container.resolve(IMyService)
print(type(service))
```

### Inspecting the Knowledge Graph

```python
from platform_core.knowledge.graph import GraphStore
from platform_core.knowledge.types import Node, Edge, NodeType, RelationshipType

store = GraphStore()
store.add_node(Node(id="n1", node_type=NodeType.CONCEPT, label="A"))
store.add_node(Node(id="n2", node_type=NodeType.CONCEPT, label="B"))
store.add_edge(Edge(id="e1", source_id="n1", target_id="n2", relationship_type=RelationshipType.DEPENDS_ON))

# Get snapshot
snapshot = store.snapshot()
print(f"Nodes: {snapshot['node_count']}, Edges: {snapshot['edge_count']}")
```

## Common Patterns in the Codebase

### Engine Pattern

Engines follow a four-phase lifecycle:

```python
class MyEngine(BaseEngine):
    def validate(self, context: EngineContext) -> None:
        """Validate input before execution."""

    def prepare(self, context: EngineContext) -> None:
        """Set up resources for execution."""

    def execute(self, context: EngineContext) -> EngineResult:
        """Perform the main work."""

    def finalize(self, context: EngineContext) -> None:
        """Clean up resources after execution."""
```

### Workflow Step Pattern

Steps are composable units of work:

```python
class ValidateInput(WorkflowStep):
    @property
    def name(self) -> str:
        return "validate_input"

    def execute(self, context: WorkflowContext) -> WorkflowResult:
        input_data = context.get("input")
        if not input_data:
            return WorkflowResult.error("No input provided")
        return WorkflowResult.ok(validated=True)
```

### Event-Driven Communication

Modules communicate through events:

```python
# Publisher
from platform_core.events.event import Event

bus.publish(Event(
    name="repository.scanned",
    payload={"repository": "my-repo", "score": 0.85}
))

# Subscriber
def on_repository_scanned(event: Event) -> None:
    repo = event.payload["repository"]
    score = event.payload["score"]
    logger.info(f"Repository {repo} scored {score}")

bus.subscribe("repository.scanned", on_repository_scanned)
```

### Configuration-Driven Behavior

Use settings for runtime configuration:

```python
from platform_core.config.settings import settings

# Access configuration
workspace = settings.workspace
log_level = settings.log_level
sandbox_mode = settings.sandbox
```

## IDE Setup

### VS Code

Recommended extensions:

- Python (ms-python)
- Pylance
- Ruff
- mypy

Recommended `settings.json`:

```json
{
    "python.linting.enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "none",
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": true,
            "source.organizeImports.ruff": true
        }
    },
    "mypy-type-checker.args": ["--strict"]
}
```

### PyCharm

1. Set Python interpreter to the virtual environment
2. Enable mypy integration
3. Configure ruff as the external tool
