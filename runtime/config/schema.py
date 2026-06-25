from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConfigField:
    name: str
    type: type = str
    default: Any = None
    required: bool = False
    description: str = ""
    env_var: str | None = None
    sensitive: bool = False

    def validate(self, value: Any) -> list[str]:
        errors: list[str] = []
        if self.required and value is None:
            errors.append(f"Required field '{self.name}' is missing")
            return errors
        if value is not None and not isinstance(value, self.type):
            try:
                value = self.type(value)
            except (ValueError, TypeError):
                errors.append(
                    f"Field '{self.name}' must be {self.type.__name__}, got {type(value).__name__}"
                )
        return errors


@dataclass
class ConfigSchema:
    fields: dict[str, ConfigField] = field(default_factory=dict)

    def add_field(self, field: ConfigField) -> None:
        self.fields[field.name] = field

    def validate(self, config: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        for name, field in self.fields.items():
            value = config.get(name, field.default)
            errors.extend(field.validate(value))
        return errors
