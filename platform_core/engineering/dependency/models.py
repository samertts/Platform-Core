from dataclasses import dataclass, field


@dataclass(slots=True)
class DependencyNode:
    """
    Represents one engineering capability.
    """

    id: str

    dependencies: list[str] = field(default_factory=list)
