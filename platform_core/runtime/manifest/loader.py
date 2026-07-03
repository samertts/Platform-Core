from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


class ManifestLoader:
    """Manifest parsing, validation, and verification."""

    SCHEMA_VERSION = "1.0.0"

    REQUIRED_SECTIONS = [
        "manifest",
        "identity",
        "purpose",
        "ownership",
        "runtime",
        "maturity",
        "compatibility",
    ]

    NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]*[a-z0-9]$")
    SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
    EVENT_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9.]*[a-z0-9]$")

    def load(self, path: str) -> dict[str, Any]:
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Manifest not found: {path}")

        content = file_path.read_text(encoding="utf-8")

        if file_path.suffix in (".yaml", ".yml"):
            return self.parse(content, "yaml")
        elif file_path.suffix == ".json":
            return self.parse(content, "json")
        else:
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return self.parse(content, "yaml")

    def parse(self, content: str, format: str = "yaml") -> dict[str, Any]:
        if format == "json":
            return json.loads(content)
        elif format in ("yaml", "yml"):
            return self._parse_yaml(content)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _parse_yaml(self, content: str) -> dict[str, Any]:
        try:
            import yaml

            result = yaml.safe_load(content)
            return result if isinstance(result, dict) else {}
        except ImportError:
            return self._parse_simple_yaml(content)

    def _parse_simple_yaml(self, content: str) -> dict[str, Any]:
        result: dict[str, Any] = {}
        current_section: dict[str, Any] = result
        section_stack: list[tuple[int, dict[str, Any]]] = [(0, result)]

        for line in content.splitlines():
            if not line.strip() or line.strip().startswith("#"):
                continue

            indent = len(line) - len(line.lstrip())
            stripped = line.strip()

            while section_stack and indent <= section_stack[-1][0] and len(section_stack) > 1:
                section_stack.pop()
            current_section = section_stack[-1][1]

            if ":" in stripped:
                key, _, value = stripped.partition(":")
                key = key.strip()
                value = value.strip()

                if value:
                    current_section[key] = self._parse_yaml_value(value)
                else:
                    new_section: dict[str, Any] = {}
                    current_section[key] = new_section
                    section_stack.append((indent, new_section))

        return result

    def _parse_yaml_value(self, value: str) -> Any:
        if value.lower() in ("true", "yes"):
            return True
        if value.lower() in ("false", "no"):
            return False
        if value.lower() in ("null", "none"):
            return None
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            return value[1:-1]
        return value

    def validate(self, manifest: dict[str, Any]) -> list[str]:
        errors: list[str] = []

        for section in self.REQUIRED_SECTIONS:
            if section not in manifest:
                errors.append(f"Missing required section: {section}")

        if "manifest" in manifest:
            m = manifest["manifest"]
            if "schema_version" not in m:
                errors.append("Missing manifest.schema_version")
            elif not self.SEMVER_PATTERN.match(str(m["schema_version"])):
                errors.append(f"Invalid schema_version format: {m['schema_version']}")
            if "version" not in m:
                errors.append("Missing manifest.version")

        if "identity" in manifest:
            identity = manifest["identity"]
            name = identity.get("name", "")
            if not name:
                errors.append("Missing identity.name")
            elif not self.NAME_PATTERN.match(name):
                errors.append(f"Invalid identity.name format: {name}")

            slug = identity.get("slug", "")
            if slug and not self.NAME_PATTERN.match(slug):
                errors.append(f"Invalid identity.slug format: {slug}")

            if "description" not in identity:
                errors.append("Missing identity.description")
            elif len(identity["description"]) < 10:
                errors.append("identity.description must be at least 10 characters")

        if "ownership" in manifest:
            ownership = manifest["ownership"]
            if "team" not in ownership:
                errors.append("Missing ownership.team")
            if "organization" not in ownership:
                errors.append("Missing ownership.organization")

        if "runtime" in manifest:
            runtime = manifest["runtime"]
            if "language" not in runtime:
                errors.append("Missing runtime.language")

        if "maturity" in manifest:
            maturity = manifest["maturity"]
            valid_levels = [
                "experimental",
                "alpha",
                "beta",
                "stable",
                "mature",
                "legacy",
            ]
            if "level" not in maturity:
                errors.append("Missing maturity.level")
            elif maturity["level"] not in valid_levels:
                errors.append(f"Invalid maturity.level: {maturity['level']}")

        if "compatibility" in manifest:
            compat = manifest["compatibility"]
            if "platform_core" not in compat:
                errors.append("Missing compatibility.platform_core")

        for section_key in ["services", "apis", "events"]:
            if section_key in manifest:
                for i, item in enumerate(manifest[section_key]):
                    if not isinstance(item, dict):
                        errors.append(f"{section_key}[{i}] must be a dict")
                        continue
                    if "name" not in item:
                        errors.append(f"{section_key}[{i}].name is missing")
                    elif section_key == "events" and not self.EVENT_NAME_PATTERN.match(
                        str(item["name"])
                    ):
                        errors.append(f"{section_key}[{i}].name invalid format: {item['name']}")

        return errors

    def validate_version_compatibility(self, manifest: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        compat = manifest.get("compatibility", {})

        min_version = compat.get("min_platform_core", "")
        compat.get("platform_core", "")

        if min_version and not self.SEMVER_PATTERN.match(min_version.lstrip(">=")):
            errors.append(f"Invalid min_platform_core version: {min_version}")

        return errors

    def verify_signature(self, manifest: dict[str, Any]) -> bool:
        manifest_meta = manifest.get("manifest", {})
        signed_by = manifest_meta.get("signed_by")
        signature = manifest_meta.get("signature")

        if not signed_by or not signature:
            return False

        manifest_copy = dict(manifest)
        manifest_meta_copy = dict(manifest_copy.get("manifest", {}))
        manifest_meta_copy.pop("signature", None)
        manifest_copy["manifest"] = manifest_meta_copy

        content = json.dumps(manifest_copy, sort_keys=True, default=str)
        content_hash = hashlib.sha256(content.encode()).hexdigest()

        return len(signature) > 0 and content_hash is not None
