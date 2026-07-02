from pathlib import Path


class FileGenerator:
    @staticmethod
    def create(path: Path, content: str = ""):

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not path.exists():
            path.write_text(
                content,
                encoding="utf-8",
            )
