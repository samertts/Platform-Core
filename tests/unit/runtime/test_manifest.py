from __future__ import annotations

import json
import os
import tempfile

from platform_core.runtime.manifest.loader import ManifestLoader

VALID_MANIFEST = {
    "manifest": {
        "schema_version": "1.0.0",
        "version": "1.0.0",
        "created_at": "2026-06-25T00:00:00Z",
        "updated_at": "2026-06-25T00:00:00Z",
    },
    "identity": {
        "name": "test-module",
        "slug": "test-module",
        "description": "A test module for unit testing",
        "type": "module",
    },
    "purpose": {
        "summary": "Test module purpose",
        "scope": "module-specific",
    },
    "ownership": {
        "team": "test-team",
        "organization": "test-org",
        "contact": "test@example.com",
        "repository_url": "https://github.com/test/test-module",
    },
    "runtime": {
        "language": "python",
        "version": ">=3.11",
    },
    "maturity": {
        "level": "alpha",
        "since": "2026-06-25",
    },
    "compatibility": {
        "platform_core": ">=1.0.0",
        "min_platform_version": "1.0.0",
    },
}


class TestManifestLoader:
    def test_init(self) -> None:
        loader = ManifestLoader()
        assert loader is not None

    def test_parse_json(self) -> None:
        loader = ManifestLoader()
        content = json.dumps(VALID_MANIFEST)
        result = loader.parse(content, "json")
        assert result["identity"]["name"] == "test-module"

    def test_parse_yaml(self) -> None:
        loader = ManifestLoader()
        content = (
            "identity:\n  name: test\n  slug: test\n  description: test module\n  type: module\n"
        )
        result = loader.parse(content, "yaml")
        assert result["identity"]["name"] == "test"

    def test_validate_valid(self) -> None:
        loader = ManifestLoader()
        errors = loader.validate(VALID_MANIFEST)
        assert errors == []

    def test_validate_missing_sections(self) -> None:
        loader = ManifestLoader()
        errors = loader.validate({})
        assert len(errors) > 0

    def test_validate_bad_name(self) -> None:
        loader = ManifestLoader()
        manifest = dict(VALID_MANIFEST)
        manifest["identity"] = dict(VALID_MANIFEST["identity"])
        manifest["identity"]["name"] = "INVALID_NAME"
        errors = loader.validate(manifest)
        assert any("identity.name" in e for e in errors)

    def test_validate_short_description(self) -> None:
        loader = ManifestLoader()
        manifest = dict(VALID_MANIFEST)
        manifest["identity"] = dict(VALID_MANIFEST["identity"])
        manifest["identity"]["description"] = "short"
        errors = loader.validate(manifest)
        assert any("description" in e for e in errors)

    def test_load_json_file(self) -> None:
        loader = ManifestLoader()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(VALID_MANIFEST, f)
            f.flush()
            try:
                result = loader.load(f.name)
                assert result["identity"]["name"] == "test-module"
            finally:
                os.unlink(f.name)

    def test_verify_signature_no_sig(self) -> None:
        loader = ManifestLoader()
        assert loader.verify_signature(VALID_MANIFEST) is False

    def test_validate_version_compatibility(self) -> None:
        loader = ManifestLoader()
        errors = loader.validate_version_compatibility(VALID_MANIFEST)
        assert errors == []
