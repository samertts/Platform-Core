from pathlib import Path

from .types import MetadataKind


class MetadataRegistry:

    ROOT = Path(".engineering")

    MAP = {
        MetadataKind.MANIFEST: ROOT / "manifest.yaml",
        MetadataKind.CAPABILITY: ROOT / "capabilities",
        MetadataKind.KNOWLEDGE: ROOT / "knowledge",
        MetadataKind.POLICY: ROOT / "policies",
        MetadataKind.RUNTIME: ROOT / "capabilities/core/runtime.yaml",
        MetadataKind.REGISTRY: ROOT / "capabilities/core/registry.yaml",
        MetadataKind.GOVERNANCE: ROOT / "capabilities/core/governance.yaml",
        MetadataKind.GOAL: ROOT / "goals",
    }

    @classmethod
    def resolve(cls, kind: MetadataKind):

        return cls.MAP[kind]
