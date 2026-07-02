from dataclasses import dataclass, field


@dataclass(slots=True)
class RegistryEntry:
    id: str

    kind: str

    path: str

    name: str

    description: str = ""

    tags: list[str] = field(default_factory=list)

    metadata: dict[str, str] = field(default_factory=dict)
