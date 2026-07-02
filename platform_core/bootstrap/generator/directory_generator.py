from pathlib import Path


class DirectoryGenerator:

    @staticmethod
    def create(path: Path):

        path.mkdir(
            parents=True,
            exist_ok=True,
        )
