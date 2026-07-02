from pathlib import Path

from platform_core.engineering.registry.registry import EngineeringRegistry
from platform_core.engineering.scanner.scanner import EngineeringScanner


def test_scanner(tmp_path: Path):

    engineering = tmp_path / ".engineering"

    engineering.mkdir()

    (engineering / "runtime.yaml").write_text(
        """
id: runtime
name: Runtime
kind: capability
description: Runtime Engine
""",
        encoding="utf8",
    )

    registry = EngineeringRegistry()

    scanner = EngineeringScanner(
        engineering,
        registry,
    )

    scanner.scan()

    assert registry.exists("runtime")
