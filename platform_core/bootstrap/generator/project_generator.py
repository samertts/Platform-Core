from .base_generator import BaseGenerator
from .directory_generator import DirectoryGenerator
from .file_generator import FileGenerator


class ProjectGenerator(BaseGenerator):
    def generate(self):

        root = self.workspace

        directories = [
            "apps",
            "docs",
            "tests",
            "platform_core",
            "templates",
        ]

        for directory in directories:
            DirectoryGenerator.create(root / directory)

        FileGenerator.create(
            root / "README.md",
            "# New Platform Project\n",
        )

        FileGenerator.create(
            root / ".gitignore",
            "__pycache__/\n.venv/\n",
        )
