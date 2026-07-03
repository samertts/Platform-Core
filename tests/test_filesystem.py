from pathlib import Path

from platform_core.filesystem.filesystem import FileSystem


def test_write_read(tmp_path: Path) -> None:

    file = tmp_path / "demo.txt"

    FileSystem.write_text(
        file,
        "Platform-Core",
    )

    assert FileSystem.exists(file)

    assert FileSystem.read_text(file) == "Platform-Core"
