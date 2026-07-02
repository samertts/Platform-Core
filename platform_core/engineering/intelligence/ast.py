"""
Platform-Core Engineering Intelligence

Python AST Scanner
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ImportRecord:

    module: str

    name: str | None


@dataclass(slots=True)
class FunctionRecord:

    name: str

    lineno: int


@dataclass(slots=True)
class ClassRecord:

    name: str

    lineno: int


@dataclass(slots=True)
class PythonFileAnalysis:

    path: Path

    imports: list[ImportRecord]

    functions: list[FunctionRecord]

    classes: list[ClassRecord]


class PythonAstScanner:

    def scan(
        self,
        file: Path,
    ) -> PythonFileAnalysis:

        tree = ast.parse(
            file.read_text(
                encoding="utf-8",
            )
        )

        imports = []

        functions = []

        classes = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:

                    imports.append(
                        ImportRecord(
                            module=alias.name,
                            name=alias.asname,
                        )
                    )

            elif isinstance(node, ast.ImportFrom):

                for alias in node.names:

                    imports.append(
                        ImportRecord(
                            module=node.module or "",
                            name=alias.name,
                        )
                    )

            elif isinstance(
                node,
                ast.FunctionDef,
            ):

                functions.append(
                    FunctionRecord(
                        name=node.name,
                        lineno=node.lineno,
                    )
                )

            elif isinstance(
                node,
                ast.ClassDef,
            ):

                classes.append(
                    ClassRecord(
                        name=node.name,
                        lineno=node.lineno,
                    )
                )

        return PythonFileAnalysis(
            path=file,
            imports=imports,
            functions=functions,
            classes=classes,
        )
