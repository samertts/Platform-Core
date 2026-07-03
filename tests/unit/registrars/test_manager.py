from platform_core.registrars import RegistrarManager
from platform_core.registrars.core import CoreRegistrar
from platform_core.services.collection import ServiceCollection


def test_register_all() -> None:

    services = ServiceCollection()

    manager = RegistrarManager()

    manager.add(
        CoreRegistrar(),
    )

    manager.register_all(
        services,
    )

    assert isinstance(
        services.descriptors,
        tuple,
    )


def test_multiple_registrars() -> None:

    services = ServiceCollection()

    manager = RegistrarManager()

    manager.add(
        CoreRegistrar(),
    )

    manager.add(
        CoreRegistrar(),
    )

    manager.register_all(
        services,
    )

    assert (
        len(
            manager._registrars,
        )
        == 2
    )
