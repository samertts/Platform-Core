from __future__ import annotations

from pathlib import Path

from platform_core.generator.filesystem import FileSystem
from platform_core.generator.renderer import TemplateRenderer
from platform_core.generator.result import GeneratorResult


class GeneratorEngine:

    def __init__(self):

        self._fs = FileSystem()

        self._renderer = TemplateRenderer()

    def generate_service(
        self,
        root: Path,
        name: str,
    ) -> GeneratorResult:

        service_dir = (
            root
            / "platform_core"
            / "services"
            / name
        )

        self._fs.mkdir(service_dir)

        created_dirs = [str(service_dir)]

        created_files = []

        files = {

            "__init__.py": "",

            "service.py": (
                "class {{CLASS}}Service:\n"
                "    pass\n"
            ),

            "interface.py": (
                "from abc import ABC\n\n"
                "class {{CLASS}}Interface(ABC):\n"
                "    pass\n"
            ),

            "manifest.yaml": (
                "name: {{NAME}}\n"
                "type: service\n"
            ),

        }

        variables = {

            "NAME": name,

            "CLASS": name.capitalize(),

        }

        for filename, template in files.items():

            content = self._renderer.render(
                template,
                variables,
            )

            path = service_dir / filename

            self._fs.write_file(
                path,
                content,
            )

            created_files.append(
                str(path),
            )

        return GeneratorResult(

            files_created=created_files,

            directories_created=created_dirs,

            success=True,

        )
