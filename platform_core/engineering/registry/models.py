from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(slots=True)
class RegistryEntry:

    id: str

    kind: str

    path: str

    name: str

    description: str = ""

    tags: List[str] = field(default_factory=list)

    metadata: Dict[str, str] = field(default_factory=dict)
