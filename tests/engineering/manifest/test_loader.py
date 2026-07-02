from pathlib import Path

from platform_core.engineering.manifest.loader import ManifestLoader


def test_load_manifest():

    loader = ManifestLoader()

    manifest = loader.load(Path(".engineering/manifest.yaml"))

    assert manifest.project.name == "Platform-Core"

    assert manifest.engineering.mode == "enterprise"

    assert manifest.learning.enabled
