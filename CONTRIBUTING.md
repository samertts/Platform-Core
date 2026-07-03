# Contributing to Platform-Core

Thank you for your interest in contributing to Platform-Core! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Commit Message Convention](#commit-message-convention)
- [Review Process](#review-process)
- [Release Process](#release-process)
- [License](#license)
- [Getting Help](#getting-help)

## Code of Conduct

This project adheres to the [Contributor Covenant v2.1](CODE_OF_CONDUCT.md). By participating, you agree to uphold its standards. Report unacceptable behavior to platform@healthcare.org.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment (see below)
4. Create a feature branch
5. Make your changes
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.11 or later
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/samertts/Platform-Core.git
cd Platform-Core

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install the package in development mode
pip install -e ".[dev,yaml]"

# Verify installation
python -c "import platform_core; print(platform_core.__version__)"
```

### Pre-commit Checks

Run these before every commit:

```bash
# Linting
ruff check .

# Type checking
mypy platform_core/

# Unit tests
pytest tests/ -v
```

## How to Contribute

### Reporting Bugs

1. Search [existing issues](https://github.com/samertts/Platform-Core/issues) first
2. Open a new issue using the **Bug Report** template
3. Include:
   - Python version and OS
   - Steps to reproduce
   - Expected vs actual behavior
   - Relevant logs or tracebacks

### Suggesting Features

1. Open an issue using the **Feature Request** template
2. Describe the problem your feature would solve
3. Outline the proposed solution
4. Note any alternatives you considered

### Code Contributions

1. Pick an issue labeled `good first issue` or `help wanted`
2. Comment on the issue to claim it
3. Follow the development setup above
4. Implement changes following the guidelines below
5. Submit a pull request

## Pull Request Process

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make your changes** in focused, atomic commits

3. **Ensure all checks pass**:
   ```bash
   ruff check .
   mypy platform_core/
   pytest tests/ -v --cov=platform_core
   ```

4. **Update documentation** if your change affects the public API or adds new features

5. **Update the changelog** under the `[Unreleased]` section in `CHANGELOG.md`

6. **Push and create a pull request** against `main`

7. **Fill out the PR template** completely, linking the relevant issue

8. **Respond to review feedback** promptly and push additional commits as needed

9. A maintainer will merge your PR once approved and all checks pass

## Code Style Guidelines

This project uses **ruff** for linting and **mypy** for static type analysis.

### Ruff Configuration

- Line length: 100 characters
- Target: Python 3.11
- Enabled rules: `E`, `F`, `I`, `N`, `W`, `UP`

```bash
# Check
ruff check .

# Auto-fix
ruff check --fix .
```

### mypy Configuration

- Strict mode enabled
- `warn_return_any = true`
- `warn_unused_configs = true`

```bash
mypy platform_core/
```

### General Style

- Use type annotations on all function signatures and variables
- Prefer `pathlib.Path` over `os.path`
- Use dataclasses or Pydantic models for structured data
- Keep functions focused and under 50 lines where possible
- Use descriptive variable and function names
- No `# type: ignore` without a linked issue comment

## Testing Requirements

- All new features must include tests
- All bug fixes must include a regression test
- Maintain or improve code coverage (target: 80%+)
- Use `pytest` with `pytest-asyncio` for async tests
- Name test files `test_<module>.py` in the `tests/` directory

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=platform_core --cov-report=term-missing

# Run a specific test file
pytest tests/test_config.py -v
```

## Commit Message Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only changes |
| `style` | Code style changes (formatting, no logic change) |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or updating tests |
| `chore` | Build process or auxiliary tool changes |
| `ci` | CI/CD configuration changes |

### Examples

```
feat(runtime): add service dependency resolution ordering
fix(config): handle missing YAML key gracefully
docs: update API reference for governance module
test: add unit tests for discovery engine scoring
chore: update pyproject.toml dependencies
ci: add matrix testing for Python 3.12
```

### Rules

- Use the imperative mood in the description ("add feature" not "added feature")
- Do not capitalize the first letter of the description
- Do not end the description with a period
- Keep the subject line under 72 characters
- Reference issues in the footer: `Closes #123`

## Review Process

1. All PRs require at least one approving review from a maintainer
2. CI checks must pass (linting, type checking, tests, security scanning)
3. Reviewers will check for:
   - Code correctness and edge cases
   - Type safety and annotation completeness
   - Test coverage for new logic
   - Documentation updates
   - Adherence to style guidelines
4. Address all review comments before merging
5. Squash and merge is the default merge strategy

## Release Process

1. Update `CHANGELOG.md` with all changes since the last release
2. Update the version in `pyproject.toml`
3. Create a release tag: `git tag v<version>`
4. Push the tag: `git push origin v<version>`
5. A GitHub Action will build and publish the release
6. Update the `Unreleased` section in the changelog for the next cycle

## License

By contributing to Platform-Core, you agree that your contributions will be licensed under the same [proprietary license](LICENSE) that covers the project. See [docs/LICENSE_POLICY.md](docs/LICENSE_POLICY.md) for details.

## Getting Help

- **Issues**: Open a [GitHub Issue](https://github.com/samertts/Platform-Core/issues)
- **Discussions**: Use [GitHub Discussions](https://github.com/samertts/Platform-Core/discussions) for questions
- **Email**: platform@healthcare.org

Thank you for contributing to Platform-Core!
