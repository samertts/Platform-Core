from __future__ import annotations

from .models import Capability


class CapabilityRegistry:
    def __init__(self) -> None:
        self.capabilities: dict[str, Capability] = {}

    def add(self, capability: Capability) -> None:
        self.capabilities[capability.id] = capability

    def get(self, capability_id: str) -> Capability | None:
        return self.capabilities.get(capability_id)

    def all(self) -> list[Capability]:
        return list(self.capabilities.values())
