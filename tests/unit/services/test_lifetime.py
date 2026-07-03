from platform_core.services.lifetime import ServiceLifetime


def test_values() -> None:

    assert ServiceLifetime.SINGLETON.value == "singleton"

    assert ServiceLifetime.SCOPED.value == "scoped"

    assert ServiceLifetime.TRANSIENT.value == "transient"
