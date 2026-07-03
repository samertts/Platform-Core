from __future__ import annotations

from collections.abc import Iterable

from .models import RegistryEntry


class EngineeringRegistry:
    def __init__(self) -> None:
        self._entries: dict[str, RegistryEntry] = {}

    def register(self, entry: RegistryEntry) -> None:
        self._entries[entry.id] = entry

    def unregister(self, identifier: str) -> None:
        self._entries.pop(identifier, None)

    def get(self, identifier: str) -> RegistryEntry | None:
        return self._entries.get(identifier)

    def exists(self, identifier: str) -> bool:
        return identifier in self._entries

    def all(self) -> Iterable[RegistryEntry]:
        return self._entries.values()

    def count(self) -> int:
        return len(self._entries)
