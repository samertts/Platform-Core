from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(slots=True)
class Manifest:

    capabilities: list = field(default_factory=list)


@dataclass(slots=True)
class ProjectManifest:

    name: str

    owner: str

    description: str


@dataclass(slots=True)
class EngineeringManifest:

    language: str

    mode: str

    architecture: str

    governance: bool

    tests: bool

    typing: bool

    documentation: bool

@dataclass(slots=True)
class RepositoryManifest:

    default_branch: str


@dataclass(slots=True)
class LearningManifest:

    enabled: bool


@dataclass(slots=True)
class Manifest:

    version: int

    project: ProjectManifest

    engineering: EngineeringManifest

    repository: RepositoryManifest

    learning: LearningManifest

    metadata: Dict[str, str] = field(default_factory=dict)
