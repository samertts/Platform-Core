"""
Platform-Core Engineering Intelligence

Global constants used by the Engineering Intelligence
subsystem.

This module intentionally contains only immutable values.
"""

from __future__ import annotations

from pathlib import Path

###############################################################################
# Engine
###############################################################################

ENGINE_NAME = "Platform-Core Engineering Intelligence"

ENGINE_VERSION = "1.0.0"

ENGINE_SCHEMA_VERSION = "1"

###############################################################################
# Repository
###############################################################################

DEFAULT_BRANCH = "main"

DEFAULT_ENCODING = "utf-8"

DEFAULT_HASH = "sha256"

CACHE_DIRECTORY = ".platform/cache"

KNOWLEDGE_DIRECTORY = ".engineering/knowledge"

CAPABILITIES_DIRECTORY = ".engineering/capabilities"

MANIFEST_DIRECTORY = ".engineering/manifests"

###############################################################################
# Limits
###############################################################################

MAX_SCAN_DEPTH = 128

MAX_FILE_SIZE_MB = 20

MAX_REPAIR_ITERATIONS = 10

MAX_ANALYSIS_ITERATIONS = 25

MAX_PLUGINS = 1024

###############################################################################
# Quality
###############################################################################

MINIMUM_COVERAGE = 90.0

MINIMUM_ENGINEERING_SCORE = 90.0

DEFAULT_TIMEOUT_SECONDS = 300

###############################################################################
# Supported files
###############################################################################

SUPPORTED_SOURCE_EXTENSIONS = (
    ".py",
    ".pyi",
)

SUPPORTED_CONFIGURATION_FILES = (
    "pyproject.toml",
    "requirements.txt",
    "Dockerfile",
    "docker-compose.yml",
    ".pre-commit-config.yaml",
)

SUPPORTED_MANIFESTS = (
    "runtime.yaml",
    "registry.yaml",
    "governance.yaml",
)

###############################################################################
# Ignore
###############################################################################

DEFAULT_IGNORE_DIRECTORIES = (
    ".git",
    ".venv",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
)

###############################################################################
# Paths
###############################################################################

PROJECT_ROOT = Path(".")

ENGINEERING_ROOT = Path(".engineering")

PLATFORM_ROOT = Path("platform_core")

###############################################################################
# GitHub
###############################################################################

MAX_GITHUB_RESULTS = 50

MAX_SIMILAR_PROJECTS = 20

MAX_REFERENCE_IMPLEMENTATIONS = 10

###############################################################################
# Auto Repair
###############################################################################

ENABLE_SAFE_REPAIR = True

ENABLE_BACKUP = True

ENABLE_DRY_RUN = False

ENABLE_GIT_CHECKPOINT = True
