# Installation Guide

This guide covers installing Platform-Core from PyPI, from source, and setting up a development environment.

## Requirements

- **Python**: 3.11 or later (3.12 recommended)
- **pip**: 21.0 or later
- **Operating System**: Linux, macOS, or Windows

## Install from PyPI

```bash
pip install platform-core
```

This installs Platform-Core with only the required dependencies (pydantic).

### With Optional Dependencies

```bash
# With YAML support
pip install platform-core[yaml]
```

## Install from Source

```bash
# Clone the repository
git clone https://github.com/samertts/Platform-Core.git
cd Platform-Core

# Install in the current environment
pip install .
```

### From a Specific Branch or Tag

```bash
# Install from a specific branch
pip install git+https://github.com/samertts/Platform-Core.git@main

# Install from a specific tag
pip install git+https://github.com/samertts/Platform-Core.git@v1.0.0
```

## Development Installation

For contributing or modifying Platform-Core:

```bash
# Clone the repository
git clone https://github.com/samertts/Platform-Core.git
cd Platform-Core

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install in editable mode with all dev dependencies
pip install -e ".[dev]"

# Install optional YAML support
pip install -e ".[yaml]"
```

### What Gets Installed

The development installation includes:

**Core dependencies:**
- `pydantic>=2.0.0` — Data validation and settings management

**Dev dependencies (`[dev]`):**
- `pytest>=8.0` — Testing framework
- `pytest-asyncio>=1.0` — Async test support
- `pytest-cov>=7.0` — Coverage reporting
- `coverage[toml]>=7.0` — Code coverage
- `ruff>=0.12` — Linting and formatting
- `mypy>=1.16` — Static type checking
- `build>=1.2` — Package building
- `twine>=6.0` — Package publishing
- `types-PyYAML` — Type stubs for PyYAML

**Optional dependencies (`[yaml]`):**
- `pyyaml>=6.0` — YAML file parsing

## Virtual Environment

Platform-Core should always be installed in a virtual environment to avoid dependency conflicts.

### Creating a Virtual Environment

```bash
# Using venv (standard library)
python -m venv .venv

# Using virtualenv (faster, optional)
virtualenv .venv
```

### Activating the Virtual Environment

```bash
# Linux/macOS
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### Deactivating

```bash
deactivate
```

## Docker

Docker support is planned for a future release. The Docker image will include:

- Python 3.12 runtime
- Platform-Core pre-installed
- Health check endpoints
- Configuration volume mounts

## Verifying the Installation

```bash
# Check Python version
python --version

# Verify platform-core is installed
pip show platform-core

# Run a quick test
python -c "from platform_core.runtime.container import ServiceContainer; print('OK')"
```

## Upgrading

```bash
# Upgrade to the latest version
pip install --upgrade platform-core

# Upgrade from source
cd Platform-Core
git pull
pip install -e ".[dev]"
```

## Uninstalling

```bash
pip uninstall platform-core
```

## Troubleshooting

### Common Issues

#### `pip install` fails with permission error

Use a virtual environment or add `--user`:

```bash
pip install --user platform-core
```

#### `pydantic` version conflict

Platform-Core requires `pydantic>=2.0.0`. If you have an older version:

```bash
pip install --upgrade pydantic
```

#### `mypy` reports import errors

Install type stubs:

```bash
pip install types-PyYAML
```

#### YAML loading fails

Install the optional YAML dependency:

```bash
pip install platform-core[yaml]
```

#### `pytest` not found

Install dev dependencies:

```bash
pip install -e ".[dev]"
```

#### Import errors after installation

Ensure you're using the correct Python version and virtual environment:

```bash
python --version  # Should be 3.11+
which python      # Should point to your virtual environment
```

### Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/samertts/Platform-Core/issues) for known problems
2. Search for existing solutions in the issue tracker
3. Open a new issue with:
   - Python version (`python --version`)
   - pip version (`pip --version`)
   - Operating system
   - Full error traceback
   - Steps to reproduce
