from platform_core.services.scope import ServiceScope


class Logger:
    pass


def test_empty():

    scope = ServiceScope()

    assert len(scope) == 0


def test_set():

    scope = ServiceScope()

    logger = Logger()

    scope.set(
        "logger",
        logger,
    )

    assert scope.exists("logger")

    assert scope.get("logger") is logger


def test_clear():

    scope = ServiceScope()

    scope.set(
        "logger",
        Logger(),
    )

    scope.clear()

    assert len(scope) == 0
