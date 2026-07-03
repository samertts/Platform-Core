from platform_core.engineering.registry.models import RegistryEntry
from platform_core.engineering.registry.registry import EngineeringRegistry


def test_registry_register() -> None:

    registry = EngineeringRegistry()

    registry.register(
        RegistryEntry(
            id="runtime",
            kind="capability",
            path="runtime",
            name="Runtime",
        )
    )

    assert registry.exists("runtime")

    assert registry.count() == 1


def test_registry_remove() -> None:

    registry = EngineeringRegistry()

    registry.register(
        RegistryEntry(
            id="runtime",
            kind="capability",
            path="runtime",
            name="Runtime",
        )
    )

    registry.unregister("runtime")

    assert registry.count() == 0
