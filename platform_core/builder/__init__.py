"""Package Builder - Build, sign, compress, manifest, checksum, SBOM generation."""

from __future__ import annotations

import hashlib
import json
import shutil
import tarfile
import threading
from datetime import UTC, datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any
from uuid import uuid4

from platform_core.packages import (
    PackageChecksum,
    PackageManifest,
    PackageSignature,
    SignatureAlgorithm,
)


class BuildError(Exception):
    pass


class PackageBuilder:
    """Builds, signs, and compresses .platform packages."""

    def __init__(self, output_dir: str = "/opt/platform/packages") -> None:
        self._output_dir = Path(output_dir)
        self._build_log: list[dict[str, Any]] = []
        self._lock = threading.RLock()

    def _log(self, message: str, level: str = "info", **kwargs: Any) -> None:
        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": level,
            "message": message,
            **kwargs,
        }
        self._build_log.append(entry)

    def generate_manifest(
        self,
        name: str,
        version: str,
        description: str = "",
        publisher: str = "",
        license: str = "proprietary",
        dependencies: list[dict[str, Any]] | None = None,
        capabilities: dict[str, list[str]] | None = None,
        compatibility: dict[str, str] | None = None,
    ) -> PackageManifest:
        from platform_core.packages import (
            PackageCapabilities,
            PackageCompatibility,
            PackageDependencies,
            PackageIdentity,
            PackageLifecycle,
            PackageUUID,
        )

        manifest = PackageManifest(
            package=PackageIdentity(
                uuid=PackageUUID(),
                name=name,
                version=version,
                description=description,
                publisher=publisher,
                license=license,
            ),
            dependencies=PackageDependencies(
                required=dependencies or [],
            ),
            capabilities=PackageCapabilities(
                provides=capabilities.get("provides", []) if capabilities else [],
                requires=capabilities.get("requires", []) if capabilities else [],
            ),
            compatibility=PackageCompatibility(
                platform_core=(
                    compatibility.get("platform_core", ">=1.0.0") if compatibility else ">=1.0.0"
                ),
                runtime=(
                    compatibility.get("runtime", "python>=3.11")
                    if compatibility
                    else "python>=3.11"
                ),
                sdk_version=(
                    compatibility.get("sdk_version", ">=1.0.0") if compatibility else ">=1.0.0"
                ),
            ),
        )
        return manifest

    def generate_sbom(self, manifest: PackageManifest, files: list[str]) -> dict[str, Any]:
        return {
            "sbom_version": "1.0.0",
            "generated_at": datetime.now(UTC).isoformat(),
            "package": {
                "name": manifest.package.name,
                "version": manifest.package.version,
                "supplier": manifest.package.publisher,
            },
            "components": [
                {
                    "name": f,
                    "version": manifest.package.version,
                    "type": "file",
                    "checksum": {"algorithm": "sha256", "value": ""},
                }
                for f in files
            ],
            "dependencies": manifest.dependencies.required,
        }

    def compute_checksum(self, data: bytes, algorithm: str = "sha256") -> str:
        if algorithm == "sha256":
            return hashlib.sha256(data).hexdigest()
        elif algorithm == "sha512":
            return hashlib.sha512(data).hexdigest()
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    def sign_package(self, data: bytes, private_key: str = "") -> PackageSignature:
        data_hash = hashlib.sha256(data).hexdigest()
        signature_value = hashlib.sha256(f"{data_hash}:{private_key}".encode()).hexdigest()

        return PackageSignature(
            algorithm=SignatureAlgorithm.SHA256,
            signature=signature_value,
            signer=private_key or "platform-core",
            signed_at=datetime.now(UTC),
        )

    def build_package(
        self,
        source_dir: str,
        manifest: PackageManifest,
        sign: bool = True,
        private_key: str = "",
    ) -> str:
        source_path = Path(source_dir)
        if not source_path.exists():
            raise BuildError(f"Source directory not found: {source_dir}")

        self._output_dir.mkdir(parents=True, exist_ok=True)

        package_name = f"{manifest.package.name}-{manifest.package.version}.platform"
        output_path = self._output_dir / package_name

        files: list[str] = []
        for item in source_path.rglob("*"):
            if item.is_file():
                rel = str(item.relative_to(source_path))
                files.append(rel)

        sbom = self.generate_sbom(manifest, files)
        manifest_data = self._manifest_to_dict(manifest)

        with tarfile.open(str(output_path), "w:gz") as tar:
            manifest_bytes = json.dumps(manifest_data, indent=2, default=str).encode()
            manifest_info = tarfile.TarInfo(name="manifest.yaml")
            manifest_info.size = len(manifest_bytes)
            tar.addfile(manifest_info, BytesIO(manifest_bytes))

            sbom_bytes = json.dumps(sbom, indent=2, default=str).encode()
            sbom_info = tarfile.TarInfo(name="metadata/sbom.json")
            sbom_info.size = len(sbom_bytes)
            tar.addfile(sbom_info, BytesIO(sbom_bytes))

            for file_name in files:
                file_path = source_path / file_name
                tar.add(str(file_path), arcname=f"module/{file_name}")

        package_data = output_path.read_bytes()
        checksum = self.compute_checksum(package_data)

        checksum_content = f"{checksum}  {package_name}\n"
        checksum_path = self._output_dir / f"{package_name}.sha256"
        checksum_path.write_text(checksum_content, encoding="utf-8")

        if sign:
            signature = self.sign_package(package_data, private_key)
            signature_data = {
                "algorithm": signature.algorithm.value,
                "signature": signature.signature,
                "signer": signature.signer,
                "signed_at": signature.signed_at.isoformat(),
            }
            sig_path = self._output_dir / f"{package_name}.sig"
            sig_path.write_text(json.dumps(signature_data, indent=2), encoding="utf-8")

        self._log(f"Built package: {package_name}")

        return str(output_path)

    def _manifest_to_dict(self, manifest: PackageManifest) -> dict[str, Any]:
        return {
            "package": {
                "uuid": str(manifest.package.uuid),
                "name": manifest.package.name,
                "version": manifest.package.version,
                "description": manifest.package.description,
                "publisher": manifest.package.publisher,
                "license": manifest.package.license,
            },
            "dependencies": {
                "required": manifest.dependencies.required,
                "optional": manifest.dependencies.optional,
            },
            "capabilities": {
                "provides": manifest.capabilities.provides,
                "requires": manifest.capabilities.requires,
            },
            "compatibility": {
                "platform_core": manifest.compatibility.platform_core,
                "runtime": manifest.compatibility.runtime,
                "sdk_version": manifest.compatibility.sdk_version,
            },
        }

    def get_build_log(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._build_log[-limit:])
