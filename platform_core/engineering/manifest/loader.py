from pathlib import Path

from platform_core.engineering.manifest.models import (
    EngineeringManifest,
    LearningManifest,
    Manifest,
    ProjectManifest,
    RepositoryManifest,
)
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
