from .models import Capability


class CapabilityRegistry:
    def __init__(self):

        self.capabilities = {}

    def add(self, capability: Capability):

        self.capabilities[capability.id] = capability

    def get(self, capability_id: str):

        return self.capabilities.get(capability_id)

    def all(self):

        return list(self.capabilities.values())
