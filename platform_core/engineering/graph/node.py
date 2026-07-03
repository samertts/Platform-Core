from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class GraphNode:
    id: str

    kind: str

    path: str

    metadata: dict[str, Any] = field(default_factory=dict)
