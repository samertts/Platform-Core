"""
Platform-Core Engineering Intelligence

Discovery Engine
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


PYTHON_FILES = {
    "pyproject.toml",
    "requirements.txt",
    "requirements-dev.txt",
}

NODE_FILES = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
}

RUST_FILES = {
    "Cargo.toml",
}

DOCKER_FILES = {
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
}

GIT_FILES = {
    ".git",
    ".github",
}

ENGINEERING_FILES = {
    ".engineering",
}

TEST_DIRECTORIES = {
    "tests",
}

DOC_FILES = {
    "README.md",
    "ARCHITECTURE.md",
    "CONSTITUTION.md",
    "PLATFORM_VISION.md",
}


@dataclass(slots=True)
class DiscoveryResult:

    python: bool = False

    node: bool = False

    rust: bool = False

    docker: bool = False

    git: bool = False

    engineering: bool = False

    tests: bool = False

    documentation: bool = False

    workflows: bool = False

    capabilities: bool = False

    manifests: bool = False

    plugins: bool = False

    files: list[Path] = field(default_factory=list)


class DiscoveryEngine:

    def discover(
        self,
        root: Path,
    ) -> DiscoveryResult:

        root = root.resolve()

        result = DiscoveryResult()

        for path in root.rglob("*"):

            result.files.append(path)

            name = path.name

            if name in PYTHON_FILES:
                result.python = True

            if name in NODE_FILES:
                result.node = True

            if name in RUST_FILES:
                result.rust = True

            if name in DOCKER_FILES:
                result.docker = True

            if name in DOC_FILES:
                result.documentation = True

            if name in TEST_DIRECTORIES:
                result.tests = True

            if name in ENGINEERING_FILES:
                result.engineering = True

            if name in GIT_FILES:
                result.git = True

            if ".github/workflows" in str(path):
                result.workflows = True

            if "capabilities" in path.parts:
                result.capabilities = True

            if "manifest" in path.parts:
                result.manifests = True

            if "plugin" in path.parts:
                result.plugins = True

        return result
