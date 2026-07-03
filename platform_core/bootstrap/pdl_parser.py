"""
Platform Definition Language Parser
Genesis Version
"""

from __future__ import annotations

from pathlib import Path


class PDLParser:
    def parse(self, filename: str) -> list[str]:
        path = Path(filename)

        with open(path, encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]

        return lines


if __name__ == "__main__":
    parser = PDLParser()

    data = parser.parse("blueprints/module.pdl")

    for item in data:
        print(item)
