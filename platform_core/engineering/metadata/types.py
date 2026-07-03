from enum import StrEnum


class MetadataKind(StrEnum):
    MANIFEST = "manifest"

    CAPABILITY = "capability"

    POLICY = "policy"

    KNOWLEDGE = "knowledge"

    GOAL = "goal"

    RUNTIME = "runtime"

    GOVERNANCE = "governance"

    REGISTRY = "registry"
