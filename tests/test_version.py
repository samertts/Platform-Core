from platform_core.version import VERSION


def test_version():

    assert VERSION.string == "0.1.0-alpha"
