from pathlib import Path

import pytest

from platform_core.generator.filesystem import (
    FileAlreadyExistsError,
    FileSystem,
)


def test_prevent_overwrite(tmp_path: Path) -> None:

    fs = FileSystem()

    path = tmp_path / "file.txt"

    fs.write_file(path, "one")

    with pytest.raises(FileAlreadyExistsError):
        fs.write_file(path, "two")
