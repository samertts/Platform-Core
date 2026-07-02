"""Analyzers - Process raw scan data into structured knowledge."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from platform_core.discovery.types import (AnalysisResult, ArchitectureInfo,
                                           CIInfo, DependencyInfo, DockerInfo,
                                           DocumentationInfo, Finding,
                                           FindingCategory, FindingSeverity,
                                           FrameworkInfo, LanguageInfo,
                                           SecurityInfo, TestingInfo)


class BaseAnalyzer:
    name: str = "base"
    description: str = ""
    enabled: bool = True

    def analyze(self, root_path: str, files: list[dict[str, Any]]) -> dict[str, Any]:
        raise NotImplementedError


class LanguageAnalyzer(BaseAnalyzer):
    name = "language"
    description = "Detects programming languages and their distribution"

    EXTENSION_MAP: dict[str, str] = {
        ".py": "Python",
        ".pyx": "Python",
        ".pyi": "Python",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".mjs": "JavaScript",
        ".go": "Go",
        ".rs": "Rust",
        ".java": "Java",
        ".cs": "C#",
        ".cpp": "C++",
        ".cc": "C++",
        ".cxx": "C++",
        ".c": "C",
        ".h": "C",
        ".rb": "Ruby",
        ".php": "PHP",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".kts": "Kotlin",
        ".scala": "Scala",
        ".sh": "Shell",
        ".bash": "Shell",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".json": "JSON",
        ".toml": "TOML",
        ".xml": "XML",
        ".html": "HTML",
        ".htm": "HTML",
        ".css": "CSS",
        ".scss": "SCSS",
        ".less": "LESS",
        ".md": "Markdown",
        ".sql": "SQL",
        ".r": "R",
        ".R": "R",
        ".lua": "Lua",
        ".dart": "Dart",
        ".ex": "Elixir",
        ".exs": "Elixir",
        ".erl": "Erlang",
        ".hs": "Haskell",
        ".ml": "OCaml",
        ".vue": "Vue",
        ".svelte": "Svelte",
    }

    CONFIG_EXTENSIONS = {
        ".yaml",
        ".yml",
        ".json",
        ".toml",
        ".xml",
        ".ini",
        ".cfg",
        ".conf",
    }

    def analyze(self, root_path: str, files: list[dict[str, Any]]) -> dict[str, Any]:
        lang_counts: dict[str, int] = {}
        config_count = 0

        for f in files:
            ext = f.get("extension", "")
            if ext in self.CONFIG_EXTENSIONS:
                config_count += 1
                continue
            lang = self.EXTENSION_MAP.get(ext)
            if lang:
                lang_counts[lang] = lang_counts.get(lang, 0) + 1

        total = sum(lang_counts.values()) or 1
        distribution = []
        for lang, count in sorted(lang_counts.items(), key=lambda x: -x[1]):
            distribution.append(
                {
                    "language": lang,
                    "files": count,
                    "percentage": round(count / total * 100, 1),
                }
            )

        primary = distribution[0]["language"] if distribution else "Unknown"

        return {
            "primary": primary,
            "distribution": distribution,
            "total_files": len(files),
            "total_source_files": total,
        }


class FrameworkAnalyzer(BaseAnalyzer):
    name = "framework"
    description = "Detects frameworks and libraries"

    KNOWN_FRAMEWORKS: list[dict[str, Any]] = [
        {
            "name": "FastAPI",
            "signals": ["fastapi"],
            "category": "web",
            "file": "requirements.txt",
        },
        {
            "name": "Django",
            "signals": ["django"],
            "category": "web",
            "file": "requirements.txt",
        },
        {
            "name": "Flask",
            "signals": ["flask"],
            "category": "web",
            "file": "requirements.txt",
        },
        {
            "name": "Express",
            "signals": ["express"],
            "category": "web",
            "file": "package.json",
        },
        {
            "name": "Next.js",
            "signals": ["next"],
            "category": "web",
            "file": "package.json",
        },
        {
            "name": "React",
            "signals": ["react"],
            "category": "frontend",
            "file": "package.json",
        },
        {
            "name": "Vue",
            "signals": ["vue"],
            "category": "frontend",
            "file": "package.json",
        },
        {
            "name": "Angular",
            "signals": ["@angular/core"],
            "category": "frontend",
            "file": "package.json",
        },
        {
            "name": "Svelte",
            "signals": ["svelte"],
            "category": "frontend",
            "file": "package.json",
        },
        {
            "name": "pytest",
            "signals": ["pytest"],
            "category": "test",
            "file": "requirements.txt",
        },
        {
            "name": "Jest",
            "signals": ["jest"],
            "category": "test",
            "file": "package.json",
        },
        {
            "name": "SQLAlchemy",
            "signals": ["sqlalchemy"],
            "category": "orm",
            "file": "requirements.txt",
        },
        {
            "name": "Pydantic",
            "signals": ["pydantic"],
            "category": "validation",
            "file": "requirements.txt",
        },
        {
            "name": "Celery",
            "signals": ["celery"],
            "category": "task_queue",
            "file": "requirements.txt",
        },
        {
            "name": "Redis",
            "signals": ["redis"],
            "category": "cache",
            "file": "requirements.txt",
        },
        {
            "name": "TensorFlow",
            "signals": ["tensorflow"],
            "category": "ml",
            "file": "requirements.txt",
        },
        {
            "name": "PyTorch",
            "signals": ["torch"],
            "category": "ml",
            "file": "requirements.txt",
        },
    ]

    def analyze(self, root_path: str, files: list[dict[str, Any]]) -> dict[str, Any]:
        root = Path(root_path)
        detected: list[dict[str, Any]] = []

        dep_content = self._read_dependency_files(root, files)

        for fw in self.KNOWN_FRAMEWORKS:
            for dep_file, content in dep_content.items():
                if fw["file"] in dep_file:
                    for signal in fw["signals"]:
                        if signal.lower() in content.lower():
                            detected.append(
                                {
                                    "name": fw["name"],
                                    "category": fw["category"],
                                    "file": dep_file,
                                    "confidence": 0.9,
                                }
                            )
                            break

        return {
            "detected": detected,
            "primary": detected[0]["name"] if detected else "",
            "count": len(detected),
        }

    def _read_dependency_files(
        self, root: Path, files: list[dict[str, Any]]
    ) -> dict[str, str]:
        dep_files = [
            "requirements.txt",
            "setup.py",
            "setup.cfg",
            "pyproject.toml",
            "package.json",
            "go.mod",
            "Cargo.toml",
            "pom.xml",
            "build.gradle",
            "Gemfile",
            "composer.json",
        ]
        result: dict[str, str] = {}
        for f in files:
            if f["name"] in dep_files:
                filepath = root / f["path"]
                try:
                    result[f["path"]] = filepath.read_text(
                        encoding="utf-8", errors="ignore"
                    )
                except (OSError, PermissionError):
                    pass
        return result


class ArchitectureAnalyzer(BaseAnalyzer):
    name = "architecture"
    description = "Detects architectural patterns"

    PATTERNS: list[dict[str, Any]] = [
        {
            "name": "microservices",
            "signals": ["services/", "docker-compose.yml"],
            "min_matches": 1,
        },
        {"name": "modular_monolith", "signals": ["modules/", "src/"], "min_matches": 1},
        {"name": "monolith", "signals": ["main.py", "app.py"], "min_matches": 1},
        {"name": "cli", "signals": ["cmd/", "cli.py", "click"], "min_matches": 1},
        {
            "name": "serverless",
            "signals": ["handler.py", "lambda", "serverless.yml"],
            "min_matches": 1,
        },
        {"name": "plugin_based", "signals": ["plugins/", "hooks/"], "min_matches": 1},
        {
            "name": "layered",
            "signals": ["models/", "views/", "controllers/"],
            "min_matches": 2,
        },
    ]

    def analyze(self, root_path: str, files: list[dict[str, Any]]) -> dict[str, Any]:
        root = Path(root_path)
        dir_names = self._get_directory_names(root)
        file_names = {f["name"] for f in files}
        all_names = dir_names | file_names

        best_pattern = "unknown"
        best_confidence = 0.0
        features: list[str] = []

        for pattern in self.PATTERNS:
            matches = sum(
                1 for s in pattern["signals"] if any(s in n for n in all_names)
            )
            if matches >= pattern["min_matches"]:
                confidence = min(matches / len(pattern["signals"]), 1.0)
                if confidence > best_confidence:
                    best_pattern = pattern["name"]
                    best_confidence = confidence
                    features = [
                        s for s in pattern["signals"] if any(s in n for n in all_names)
                    ]

        return {
            "pattern": best_pattern,
            "confidence": round(best_confidence, 2),
            "features": features,
        }

    def _get_directory_names(self, root: Path) -> set[str]:
        names: set[str] = set()
        try:
            for item in root.iterdir():
                if item.is_dir() and not item.name.startswith("."):
                    names.add(item.name + "/")
        except PermissionError:
            pass
        return names


class DocumentationAnalyzer(BaseAnalyzer):
    name = "documentation"
    description = "Assesses documentation quality"

    REQUIRED_FILES = ["README.md", "README.rst", "README"]
    RECOMMENDED_FILES = ["CHANGELOG.md", "CONTRIBUTING.md", "LICENSE", "LICENSE.md"]
    API_DOC_FILES = ["openapi.json", "openapi.yaml", "swagger.json", "swagger.yaml"]
    ARCH_DOC_DIRS = ["docs", "documentation", "architecture", "doc"]

    def analyze(self, root_path: str, files: list[dict[str, Any]]) -> dict[str, Any]:
        file_names = {f["name"] for f in files}
        dir_names = {f["path"].split("/")[0] + "/" for f in files if "/" in f["path"]}

        has_readme = any(r in file_names for r in self.REQUIRED_FILES)
        has_changelog = "CHANGELOG.md" in file_names
        has_contributing = "CONTRIBUTING.md" in file_names
        has_license = any(
            l in file_names for l in ["LICENSE", "LICENSE.md", "LICENSE.txt"]
        )
        has_api_docs = any(d in file_names for d in self.API_DOC_FILES)
        has_arch_docs = any(d.rstrip("/") in dir_names for d in self.ARCH_DOC_DIRS)

        score = 0.0
        if has_readme:
            score += 0.25
        if has_changelog:
            score += 0.15
        if has_contributing:
            score += 0.10
        if has_license:
            score += 0.15
        if has_api_docs:
            score += 0.20
        if has_arch_docs:
            score += 0.15

        findings: list[dict[str, Any]] = []
        if not has_readme:
            findings.append(
                {
                    "type": "missing_readme",
                    "severity": "high",
                    "message": "No README file found",
                }
            )
        if not has_license:
            findings.append(
                {
                    "type": "missing_license",
                    "severity": "medium",
                    "message": "No LICENSE file found",
                }
            )
        if not has_changelog:
            findings.append(
                {
                    "type": "missing_changelog",
                    "severity": "low",
                    "message": "No CHANGELOG.md found",
                }
            )

        return {
            "score": round(score, 2),
            "has_readme": has_readme,
            "has_changelog": has_changelog,
            "has_contributing": has_contributing,
            "has_license": has_license,
            "has_api_docs": has_api_docs,
            "has_architecture_docs": has_arch_docs,
            "findings": findings,
        }


class TestingAnalyzer(BaseAnalyzer):
    name = "testing"
    description = "Assesses test coverage and quality"

    TEST_PATTERNS = [
        "test_*.py",
        "*_test.py",
        "*.test.ts",
        "*.test.js",
        "*.test.tsx",
        "*.test.jsx",
        "*_test.go",
        "*_test.rs",
        "*.spec.ts",
        "*.spec.js",
    ]
    TEST_CONFIG_FILES = [
        "pytest.ini",
        "setup.cfg",
        "pyproject.toml",
        "jest.config.js",
        "jest.config.ts",
        ".jest.config",
        "vitest.config.ts",
        "vitest.config.js",
    ]
    COVERAGE_FILES = [".coverage", "coverage.xml", "htmlcov", "coverage.json"]

    def analyze(self, root_path: str, files: list[dict[str, Any]]) -> dict[str, Any]:
        test_files = [f for f in files if self._is_test_file(f["name"])]
        has_test_config = any(f["name"] in self.TEST_CONFIG_FILES for f in files)
        has_coverage = any(
            any(c in f["path"] for c in self.COVERAGE_FILES) for f in files
        )

        test_framework = self._detect_framework(files)
        test_count = len(test_files)
        total_source = len(files) - test_count
        ratio = test_count / max(total_source, 1)

        score = 0.0
        if test_count > 0:
            score += 0.30
        if test_framework:
            score += 0.20
        if has_test_config:
            score += 0.15
        if has_coverage:
            score += 0.20
        if ratio >= 0.1:
            score += 0.15

        findings: list[dict[str, Any]] = []
        if test_count == 0:
            findings.append(
                {
                    "type": "no_tests",
                    "severity": "high",
                    "message": "No test files found",
                }
            )
        if not has_test_config:
            findings.append(
                {
                    "type": "no_test_config",
                    "severity": "low",
                    "message": "No test configuration found",
                }
            )

        return {
            "score": round(min(score, 1.0), 2),
            "test_framework": test_framework,
            "test_files": test_count,
            "has_test_config": has_test_config,
            "coverage_available": has_coverage,
            "test_to_code_ratio": round(ratio, 2),
            "findings": findings,
        }

    def _is_test_file(self, name: str) -> bool:
        test_prefixes = ("test_", "tests_", "spec_")
        test_suffixes = (
            "_test.py",
            "_test.ts",
            "_test.js",
            "_test.go",
            "_test.rs",
            ".test.ts",
            ".test.js",
            ".test.tsx",
            ".test.jsx",
            ".spec.ts",
            ".spec.js",
        )
        return name.startswith(test_prefixes) or name.endswith(test_suffixes)

    def _detect_framework(self, files: list[dict[str, Any]]) -> str:
        file_names = {f["name"] for f in files}
        if "pytest.ini" in file_names or "conftest.py" in file_names:
            return "pytest"
        if "jest.config.js" in file_names or "jest.config.ts" in file_names:
            return "jest"
        if "vitest.config.ts" in file_names:
            return "vitest"
        return ""


class SecurityAnalyzer(BaseAnalyzer):
    name = "security"
    description = "Detects security configuration and potential issues"

    SECRET_PATTERNS = [
        (r"password\s*=\s*['\"]", "hardcoded_password", FindingSeverity.CRITICAL),
        (r"api_key\s*=\s*['\"]", "hardcoded_api_key", FindingSeverity.CRITICAL),
        (r"secret\s*=\s*['\"]", "hardcoded_secret", FindingSeverity.CRITICAL),
        (r"token\s*=\s*['\"]", "hardcoded_token", FindingSeverity.CRITICAL),
        (r"aws_access_key_id\s*=", "aws_key", FindingSeverity.CRITICAL),
        (r"aws_secret_access_key\s*=", "aws_secret", FindingSeverity.CRITICAL),
        (r"PRIVATE KEY", "private_key", FindingSeverity.CRITICAL),
    ]

    def analyze(self, root_path: str, files: list[dict[str, Any]]) -> dict[str, Any]:
        root = Path(root_path)
        file_names = {f["name"] for f in files}

        has_security_md = "SECURITY.md" in file_names
        has_gitignore = ".gitignore" in file_names
        has_env_example = ".env.example" in file_names
        has_env_committed = ".env" in file_names and ".env.example" not in file_names

        findings: list[dict[str, Any]] = []
        secret_count = 0

        if has_env_committed:
            findings.append(
                {
                    "type": "env_committed",
                    "severity": FindingSeverity.CRITICAL.value,
                    "message": ".env file committed without .env.example",
                }
            )

        for f in files:
            if f["size"] > 100000:
                continue
            filepath = root / f["path"]
            try:
                content = filepath.read_text(encoding="utf-8", errors="ignore")
                for pattern, ftype, severity in self.SECRET_PATTERNS:
                    if re.search(pattern, content):
                        secret_count += 1
                        findings.append(
                            {
                                "type": ftype,
                                "severity": severity.value,
                                "file": f["path"],
                                "message": f"Potential {ftype.replace('_', ' ')} detected",
                            }
                        )
            except (OSError, PermissionError):
                continue

        score = 1.0
        critical_count = sum(1 for f in findings if f["severity"] == "critical")
        score -= critical_count * 0.2
        if not has_gitignore:
            score -= 0.1
        if not has_security_md:
            score -= 0.05

        return {
            "score": round(max(score, 0.0), 2),
            "has_security_md": has_security_md,
            "has_gitignore": has_gitignore,
            "has_env_example": has_env_example,
            "secret_patterns_found": secret_count,
            "findings": findings,
        }


class DependencyAnalyzer(BaseAnalyzer):
    name = "dependencies"
    description = "Analyzes dependency health"

    DEP_FILES = {
        "requirements.txt": "pip",
        "setup.cfg": "pip",
        "pyproject.toml": "pip",
        "package.json": "npm",
        "go.mod": "go",
        "Cargo.toml": "cargo",
        "pom.xml": "maven",
        "build.gradle": "gradle",
        "Gemfile": "bundler",
        "composer.json": "composer",
    }

    def analyze(self, root_path: str, files: list[dict[str, Any]]) -> dict[str, Any]:
        dep_files_found: list[str] = []
        total_deps = 0

        for f in files:
            if f["name"] in self.DEP_FILES:
                dep_files_found.append(f["path"])
                total_deps += self._count_dependencies(root_path, f)

        score = 0.5
        if dep_files_found:
            score += 0.3
        if total_deps > 0:
            score += 0.2

        return {
            "score": round(min(score, 1.0), 2),
            "total": total_deps,
            "direct": total_deps,
            "transitive": 0,
            "outdated": 0,
            "vulnerable": 0,
            "files_found": dep_files_found,
            "findings": [],
        }

    def _count_dependencies(self, root_path: str, file_info: dict[str, Any]) -> int:
        filepath = Path(root_path) / file_info["path"]
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
            if file_info["name"] == "requirements.txt":
                return len(
                    [
                        line
                        for line in content.splitlines()
                        if line.strip()
                        and not line.startswith("#")
                        and not line.startswith("-")
                    ]
                )
            if file_info["name"] == "package.json":
                data = json.loads(content)
                return len(data.get("dependencies", {})) + len(
                    data.get("devDependencies", {})
                )
        except (OSError, json.JSONDecodeError):
            pass
        return 0


class CIAnalyzer(BaseAnalyzer):
    name = "ci_cd"
    description = "Detects CI/CD pipelines"

    CI_SYSTEMS: dict[str, list[str]] = {
        "GitHub Actions": [".github/workflows/"],
        "GitLab CI": [".gitlab-ci.yml"],
        "Jenkins": ["Jenkinsfile"],
        "CircleCI": [".circleci/config.yml"],
        "Travis CI": [".travis.yml"],
        "Azure DevOps": ["azure-pipelines.yml"],
        "Bitbucket": ["bitbucket-pipelines.yml"],
    }

    def analyze(self, root_path: str, files: list[dict[str, Any]]) -> dict[str, Any]:
        file_paths = {f["path"] for f in files}
        detected_system = ""
        ci_files: list[str] = []

        for system, patterns in self.CI_SYSTEMS.items():
            for pattern in patterns:
                matches = [
                    p for p in file_paths if p.startswith(pattern) or p == pattern
                ]
                if matches:
                    detected_system = system
                    ci_files.extend(matches)

        has_ci = bool(detected_system)
        score = 0.0
        if has_ci:
            score += 0.6
            if any("deploy" in f.lower() for f in ci_files):
                score += 0.4

        return {
            "score": round(score, 2),
            "system": detected_system,
            "has_ci": has_ci,
            "stages": [],
            "deployment_configured": any("deploy" in f.lower() for f in ci_files),
            "files_found": ci_files,
        }


class DockerAnalyzer(BaseAnalyzer):
    name = "docker"
    description = "Detects container configuration"

    DOCKER_FILES = {
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        ".dockerignore",
    }

    def analyze(self, root_path: str, files: list[dict[str, Any]]) -> dict[str, Any]:
        root = Path(root_path)
        file_names = {f["name"] for f in files}
        docker_files = [f["path"] for f in files if f["name"] in self.DOCKER_FILES]

        has_dockerfile = "Dockerfile" in file_names
        has_compose = (
            "docker-compose.yml" in file_names or "docker-compose.yaml" in file_names
        )

        base_image = ""
        multi_stage = False
        ports: list[int] = []

        if has_dockerfile:
            try:
                dockerfile = root / "Dockerfile"
                content = dockerfile.read_text(encoding="utf-8", errors="ignore")
                base_image = self._extract_base_image(content)
                multi_stage = content.count("FROM ") > 1
                ports = self._extract_ports(content)
            except (OSError, PermissionError):
                pass

        return {
            "detected": has_dockerfile or has_compose,
            "base_image": base_image,
            "ports": ports,
            "multi_stage": multi_stage,
            "has_compose": has_compose,
            "files_found": docker_files,
        }

    def _extract_base_image(self, content: str) -> str:
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("FROM ") and "AS" not in line.upper():
                return line.split()[1] if len(line.split()) > 1 else ""
        return ""

    def _extract_ports(self, content: str) -> list[int]:
        ports: list[int] = []
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("EXPOSE"):
                parts = line.split()[1:]
                for part in parts:
                    port_str = part.split("/")[0]
                    if port_str.isdigit():
                        ports.append(int(port_str))
        return ports


def run_all_analyzers(root_path: str, files: list[dict[str, Any]]) -> AnalysisResult:
    """Run all built-in analyzers and return combined analysis result."""
    analyzers = [
        LanguageAnalyzer(),
        FrameworkAnalyzer(),
        ArchitectureAnalyzer(),
        DocumentationAnalyzer(),
        TestingAnalyzer(),
        SecurityAnalyzer(),
        DependencyAnalyzer(),
        CIAnalyzer(),
        DockerAnalyzer(),
    ]

    result = AnalysisResult()

    for analyzer in analyzers:
        if not analyzer.enabled:
            continue

        analysis = analyzer.analyze(root_path, files)

        if analyzer.name == "language":
            result.language = LanguageInfo(
                primary=analysis["primary"],
                distribution=analysis["distribution"],
                total_files=analysis["total_files"],
            )
        elif analyzer.name == "framework":
            result.framework = FrameworkInfo(
                name=analysis["primary"],
                frameworks=analysis["detected"],
                confidence=(
                    analysis["detected"][0]["confidence"]
                    if analysis["detected"]
                    else 0.0
                ),
            )
        elif analyzer.name == "architecture":
            result.architecture = ArchitectureInfo(
                pattern=analysis["pattern"],
                confidence=analysis["confidence"],
                features=analysis["features"],
            )
        elif analyzer.name == "documentation":
            result.documentation = DocumentationInfo(
                score=analysis["score"],
                has_readme=analysis["has_readme"],
                has_changelog=analysis["has_changelog"],
                has_contributing=analysis["has_contributing"],
                has_license=analysis["has_license"],
                has_api_docs=analysis["has_api_docs"],
                has_architecture_docs=analysis["has_architecture_docs"],
                findings=analysis["findings"],
            )
        elif analyzer.name == "testing":
            result.testing = TestingInfo(
                score=analysis["score"],
                test_framework=analysis["test_framework"],
                test_files=analysis["test_files"],
                has_test_config=analysis["has_test_config"],
                coverage_available=analysis["coverage_available"],
                test_to_code_ratio=analysis["test_to_code_ratio"],
                findings=analysis["findings"],
            )
        elif analyzer.name == "security":
            result.security = SecurityInfo(
                score=analysis["score"],
                has_security_md=analysis["has_security_md"],
                has_gitignore=analysis["has_gitignore"],
                has_env_example=analysis["has_env_example"],
                secret_patterns_found=analysis["secret_patterns_found"],
                findings=analysis["findings"],
            )
        elif analyzer.name == "dependencies":
            result.dependencies = DependencyInfo(
                score=analysis["score"],
                total=analysis["total"],
                direct=analysis["direct"],
                files_found=analysis["files_found"],
                findings=analysis["findings"],
            )
        elif analyzer.name == "ci_cd":
            result.ci_cd = CIInfo(
                score=analysis["score"],
                system=analysis["system"],
                has_ci=analysis["has_ci"],
                stages=analysis["stages"],
                deployment_configured=analysis["deployment_configured"],
                files_found=analysis["files_found"],
            )
        elif analyzer.name == "docker":
            result.docker = DockerInfo(
                detected=analysis["detected"],
                base_image=analysis["base_image"],
                ports=analysis["ports"],
                multi_stage=analysis["multi_stage"],
                has_compose=analysis["has_compose"],
                files_found=analysis["files_found"],
            )

    findings: list[Finding] = []
    for analyzer in analyzers:
        if not analyzer.enabled:
            continue
        analysis = analyzer.analyze(root_path, files)
        for f in analysis.get("findings", []):
            findings.append(
                Finding(
                    category=FindingCategory(
                        analyzer.name if analyzer.name != "ci_cd" else "ci_cd"
                    ),
                    type=f.get("type", ""),
                    severity=FindingSeverity(f.get("severity", "info")),
                    message=f.get("message", ""),
                    file=f.get("file", ""),
                )
            )
    result.findings = findings

    return result
