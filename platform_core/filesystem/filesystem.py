"""
Filesystem Service
"""

from pathlib import Path


class FileSystem:

    @staticmethod
    def exists(path: Path) -> bool:

        return path.exists()

    @staticmethod
    def mkdir(path: Path):

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def write_text(
        path: Path,
        text: str,
    ):

        path.write_text(
            text,
            encoding="utf-8",
        )

    @staticmethod
    def read_text(path: Path):

        return path.read_text(
            encoding="utf-8",
        )
