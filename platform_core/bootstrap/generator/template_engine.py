from __future__ import annotations

from string import Template
from typing import Any


class TemplateEngine:
    @staticmethod
    def render(template: str, values: dict[str, Any]) -> str:
        return Template(template).safe_substitute(values)
