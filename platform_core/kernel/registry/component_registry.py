from __future__ import annotations


class ComponentRegistry:

    def __init__(self):

        self._components: dict[str, object] = {}

    def register(
        self,
        name: str,
        component: object,
    ):

        self._components[name] = component

    def unregister(
        self,
        name: str,
    ):

        self._components.pop(
            name,
            None,
        )

    def get(
        self,
        name: str,
    ):

        return self._components.get(
            name,
        )

    def exists(
        self,
        name: str,
    ):

        return name in self._components

    def all(self):

        return dict(
            self._components
        )
