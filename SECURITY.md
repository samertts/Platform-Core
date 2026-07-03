# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within Platform-Core, please send an email to platform@healthcare.org. All security vulnerabilities will be promptly addressed.

### What to include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 5 business days
- **Fix or mitigation**: Within 30 days for critical vulnerabilities

## Security Measures

### Automated Scanning

- **Bandit**: Static analysis for common security issues in Python code
- **pip-audit**: Dependency vulnerability scanning
- **GitHub CodeQL**: Semantic code analysis
- **Dependabot**: Automated dependency updates

### Best Practices

- All pull requests require review before merge
- Secrets are never committed to the repository
- Dependencies are pinned in lockfiles
- Security scans run on every CI pipeline
- Branch protection rules enforce quality gates

## Scope

This security policy applies to the Platform-Core package distributed via PyPI and the source code in this repository.
