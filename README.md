# Platform-Core

[![CI](https://github.com/samertts/Platform-Core/actions/workflows/ci.yml/badge.svg)](https://github.com/samertts/Platform-Core/actions/workflows/ci.yml)
[![Security](https://github.com/samertts/Platform-Core/actions/workflows/security.yml/badge.svg)](https://github.com/samertts/Platform-Core/actions/workflows/security.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: Proprietary](https://img.shields.io/badge/license-proprietary-red.svg)](LICENSE)

> Transforming Knowledge into Trusted Systems

Platform-Core is a Knowledge-Driven Engineering Platform designed to transform engineering knowledge into trusted, reusable software systems. It provides a comprehensive runtime, governance framework, and intelligence layer for building enterprise-grade platforms.

## Features

- **Runtime Engine** — Dependency injection, service lifecycle management, and plugin architecture
- **Governance Framework** — AI-assisted decision making, compliance checking, and quality assurance
- **Knowledge Graph** — Graph-based knowledge management with AI-powered querying and visualization
- **Engineering Factory** — Automated code generation, capability scanning, and dependency analysis
- **Workflow Engine** — Pipeline orchestration with context management and result tracking
- **Discovery Engine** — Intelligent analysis, scoring, and reporting of platform components
- **Doctor System** — Health checks, diagnostics, and automated remediation

## Quick Start

### Installation

```bash
pip install platform-core
```

For development:

```bash
git clone https://github.com/samertts/Platform-Core.git
cd Platform-Core
pip install -e ".[dev]"
```

### Basic Usage

```python
from platform_core.runtime.container import ServiceContainer
from platform_core.runtime.config import ConfigurationEngine

# Initialize the container
container = ServiceContainer()

# Register services
container.register_singleton(MyService, MyServiceImpl)

# Resolve services
service = container.resolve(MyService)
```

### Running Tests

```bash
pytest
```

### Quality Checks

```bash
ruff check .           # Linting
ruff format --check .  # Format checking
python -m mypy .       # Type checking
```

## Architecture

Platform-Core follows a layered architecture:

```
┌─────────────────────────────────────────────┐
│                  CLI / API                   │
├─────────────────────────────────────────────┤
│           Frontend (Types, Hooks)            │
├─────────────────────────────────────────────┤
│     Governance │ Knowledge │ Discovery       │
├─────────────────────────────────────────────┤
│  Engine │ Workflow │ Scheduler │ Execution   │
├─────────────────────────────────────────────┤
│        Runtime (Container, Plugins,          │
│        Config, Events, Identity, Kernel)     │
├─────────────────────────────────────────────┤
│              Contracts / Types               │
└─────────────────────────────────────────────┘
```

See [Architecture Guide](docs/ARCHITECTURE.md) for detailed documentation.

## Project Structure

```
platform_core/         Main package
  api/                 API layer
  bootstrap/           Bootstrap generators
  capabilities/        Capability management
  cli/                 Command-line interface
  config/              Configuration management
  contracts/           Contract definitions
  discovery/           Discovery engine
  doctor/              Health diagnostics
  engine/              Core engine
  engineering/         Engineering factory
  events/              Event system
  execution/           Command execution
  frontend/            Frontend types and hooks
  governance/          Governance framework
  host/                Application host
  kernel/              Kernel core
  knowledge/           Knowledge graph
  packages/            Package management
  plugins/             Plugin system
  registry/            Service registry
  runtime/             Runtime engine
  scheduler/           Task scheduling
  security/            Security layer
  services/            Service framework
  workflow/            Workflow engine
runtime/               Runtime implementation
tests/                 Test suite
docs/                  Documentation
```

## Contributing

See [Contributing Guide](CONTRIBUTING.md) for guidelines on how to contribute.

## Security

See [Security Policy](SECURITY.md) for information about reporting vulnerabilities.

## License

Proprietary. See [LICENSE](LICENSE) for details.
