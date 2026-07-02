from pathlib import Path


class KnowledgeLoader:
    """
    Loads engineering knowledge from markdown documents.
    """

    def __init__(self, root: Path):
        self.root = root

    def load(self) -> dict[str, str]:
        knowledge: dict[str, str] = {}

        for file in self.root.rglob("*.md"):
            knowledge[file.stem] = file.read_text(encoding="utf8")

        return knowledge
