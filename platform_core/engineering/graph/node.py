from dataclasses import dataclass, field


@dataclass(slots=True)
class GraphNode:

    id: str

    kind: str

    path: str

    metadata: dict = field(default_factory=dict)
