from pathlib import Path

from platform_core.engineering.dependency.graph import DependencyGraph
from platform_core.engineering.dependency.models import DependencyNode
from platform_core.engineering.registry.models import RegistryEntry
from platform_core.engineering.registry.registry import EngineeringRegistry
from platform_core.engineering.scanner.scanner import EngineeringScanner

from .models import Manifest


class ManifestLoader:
    """
    Loads the complete engineering manifest.

    Responsibilities:

    - scan .engineering
    - build registry
    - build dependency graph
    - validate metadata
    """

    def __init__(
        self,
        engineering_root: Path,
    ):

        self.root = engineering_root

    def load(self) -> Manifest:

        registry = EngineeringRegistry()

        scanner = EngineeringScanner(
            self.root,
            registry,
        )

        scanner.scan()

        graph = DependencyGraph()

        manifest = Manifest()

        for capability in registry.list():

            graph.add_node(
                DependencyNode(
                    id=capability.id,
                    dependencies=list(
                        capability.metadata.get(
                            "depends_on",
                            [],
                        )
                    ),
                )
            )

            for dependency in capability.metadata.get(
                "depends_on",
                [],
            ):

                graph.add_dependency(
                    capability.id,
                    dependency,
                )

            manifest.capabilities.append(capability)

        manifest.registry = registry
        manifest.graph = graph

        return manifest


from pathlib import Path

from platform_core.engineering.manifest.models import (EngineeringManifest,
                                                       LearningManifest,
                                                       Manifest,
                                                       ProjectManifest,
                                                       RepositoryManifest)
from platform_core.engineering.metadata.base import BaseMetadataLoader


class ManifestLoader(BaseMetadataLoader):
    """
    Loads the engineering manifest from YAML into strongly typed models.
    """

    def load(self, path: Path) -> Manifest:
        data = self.load_yaml(path)

        return Manifest(
            version=data["version"],
            project=ProjectManifest(
                **data["project"],
            ),
            engineering=EngineeringManifest(
                **data["engineering"],
            ),
            repository=RepositoryManifest(
                **data["repository"],
            ),
            learning=LearningManifest(
                **data["learning"],
            ),
            metadata=data.get("metadata", {}),
        )

    def load_default(self) -> Manifest:
        """
        Load the default project manifest.
        """
        return self.load(Path(".engineering/manifest.yaml"))
