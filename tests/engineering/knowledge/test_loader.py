from pathlib import Path

from platform_core.engineering.knowledge.loader import KnowledgeLoader


def test_load(tmp_path: Path) -> None:

    root = tmp_path / "knowledge"

    root.mkdir()

    (root / "runtime.md").write_text(
        "# Runtime",
        encoding="utf8",
    )

    loader = KnowledgeLoader(root)

    docs = loader.load()

    assert "runtime" in docs
