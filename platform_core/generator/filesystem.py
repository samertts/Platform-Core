from pathlib import Path


class FileAlreadyExistsError(RuntimeError):
    pass


class FileSystem:
    def mkdir(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)

    def write_file(
        self,
        path: Path,
        content: str,
        overwrite: bool = False,
    ) -> None:

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if path.exists() and not overwrite:
            raise FileAlreadyExistsError(f"{path} already exists.")

        path.write_text(
            content,
            encoding="utf-8",
        )
