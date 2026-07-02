from enum import Enum


class MetadataKind(str, Enum):

    MANIFEST = "manifest"

    CAPABILITY = "capability"

    POLICY = "policy"

    KNOWLEDGE = "knowledge"

    GOAL = "goal"

    RUNTIME = "runtime"

    GOVERNANCE = "governance"

    REGISTRY = "registry"
