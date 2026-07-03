from __future__ import annotations


class ComponentRegistry:
    def __init__(self) -> None:
        self._components: dict[str, object] = {}

    def register(
        self,
        name: str,
        component: object,
    ) -> None:
        self._components[name] = component

    def unregister(
        self,
        name: str,
    ) -> None:
        self._components.pop(
            name,
            None,
        )

    def get(
        self,
        name: str,
    ) -> object | None:
        return self._components.get(
            name,
        )

    def exists(
        self,
        name: str,
    ) -> bool:
        return name in self._components

    def all(self) -> dict[str, object]:
        return dict(self._components)
