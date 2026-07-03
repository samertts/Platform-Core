from dataclasses import dataclass, field


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

    metadata: dict[str, str] = field(default_factory=dict)
