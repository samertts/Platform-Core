from dataclasses import dataclass, field


@dataclass(slots=True)
class Capability:

    id: str

    name: str

    owner: str

    status: str

    description: str

    provides: list[str] = field(default_factory=list)

    depends_on: list[str] = field(default_factory=list)

    required_by: list[str] = field(default_factory=list)

    tags: list[str] = field(default_factory=list)
