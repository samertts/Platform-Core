"""
Platform-Core Engineering Intelligence

Repository Scanner
"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from .models import (
    RepositoryFile,
    RepositoryModule,
    RepositorySnapshot,
)
from .protocols import ScannerProtocol

SUPPORTED_SUFFIXES = {
    ".py",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
    ".md",
    ".ini",
    ".cfg",
    ".txt",
}


class RepositoryScanner(ScannerProtocol):
    """
    Scans a Platform-Core repository and produces
    a RepositorySnapshot.
    """

    def scan(
        self,
        root: Path,
    ) -> RepositorySnapshot:

        root = root.resolve()

        modules: list[RepositoryModule] = []

        for directory in sorted(root.iterdir()):
            if not directory.is_dir():
                continue

            if directory.name.startswith("."):
                continue

            module = RepositoryModule(
                name=directory.name,
                path=directory,
            )

            for file in directory.rglob("*"):
                if not file.is_file():
                    continue

                if file.suffix.lower() not in SUPPORTED_SUFFIXES:
                    continue

                try:
                    checksum = sha256(file.read_bytes()).hexdigest()
                except Exception:
                    checksum = ""

                module.files.append(
                    RepositoryFile(
                        path=file,
                        language=file.suffix.lower().lstrip("."),
                        size=file.stat().st_size,
                        checksum=checksum,
                    )
                )

            modules.append(module)

        return RepositorySnapshot(
            root=root,
            modules=modules,
        )
