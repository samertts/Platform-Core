# Engineering Rules

## Architecture

Never break architectural boundaries.

Never introduce circular dependencies.

Prefer extension instead of modification.

Keep Runtime isolated.

Keep Governance deterministic.

Registry remains the single source of truth.

## Code Quality

Always format using Black.

Always lint using Ruff.

Run pytest before considering a task complete.

Prefer typed Python.

Avoid duplicated logic.

Avoid unnecessary abstractions.

## Git

Never rewrite history unless explicitly requested.

Keep commits focused.

Generate meaningful commit messages.

## Testing

New features require tests.

Bug fixes require regression tests.

Never remove tests to make builds pass.

## Documentation

Update documentation when behavior changes.

Architecture documents have high priority.

## Performance

Avoid premature optimization.

Optimize only after measurement.

## Security

Never expose secrets.

Validate external input.

Avoid unsafe subprocess usage.

Use secure defaults.
