from platform_core.version import VERSION


def test_version() -> None:

    assert VERSION.string == "0.1.0-alpha"
