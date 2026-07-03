# Branch Protection Strategy

## Protected Branches

### `main`

| Rule | Setting |
|------|---------|
| Require pull request before merging | Yes |
| Required approving reviews | 1 |
| Dismiss stale reviews on new pushes | Yes |
| Require review from code owners | Yes |
| Require status checks before merging | Yes |
| Required status checks | `Quality (3.11)`, `Build`, `Bandit`, `CodeQL` |
| Require branches to be up to date | Yes |
| Require conversation resolution | Yes |
| Require signed commits | No (optional) |
| Require linear history | Yes (squash merge) |
| Allow force pushes | **No** |
| Allow deletions | **No** |
| Do not allow bypassing above settings | Yes |

### `develop`

| Rule | Setting |
|------|---------|
| Require pull request before merging | Yes |
| Required approving reviews | 1 |
| Require status checks before merging | Yes |
| Required status checks | `Quality (3.11)` |
| Allow force pushes | Yes (for maintainers) |
| Allow deletions | No |

## Merge Strategy

- **Squash Merge**: Default for all pull requests
  - Automatically squashes all commits into a single commit
  - Requires a conventional commit message format
  - Example: `feat: add knowledge graph visualization`

- **Merge Commit**: Disabled by default
  - Only used for release merges when merging `develop` into `main`

- **Rebase**: Disabled

## Required Status Checks

### CI Pipeline (`Quality`)
- Ruff Lint
- Ruff Format Check
- Mypy (Python 3.11)
- Pytest with coverage

### Security Pipeline
- Bandit static analysis
- pip-audit dependency scanning
- CodeQL analysis

### Build Pipeline
- Package build
- Package verification (twine check)

## Release Process

1. All changes merge to `develop` first
2. When ready for release, create a release branch: `release/v1.x.x`
3. Release branch goes through final validation
4. Merge release branch to `main` via squash merge
5. Tag the merge commit on `main` with version: `v1.x.x`
6. Tag triggers the Release workflow
7. GitHub Release is created with auto-generated release notes
8. Package is published to PyPI

## Version Strategy

- **Semantic Versioning**: `MAJOR.MINOR.PATCH[-STAGE]`
- Version is maintained in three places:
  - `pyproject.toml` (authoritative)
  - `platform_core/version.py` (programmatic access)
  - `VERSION` file (simple text reference)
- All three must be updated together during release

## Hotfix Process

1. Create branch `hotfix/description` from `main`
2. Apply the fix with tests
3. Create PR targeting `main`
4. After merge, tag with patch version
5. Backport fix to `develop` if applicable
