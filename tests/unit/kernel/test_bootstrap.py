from platform_core.kernel import Bootstrap


def test_boot() -> None:

    bootstrap = Bootstrap()

    context = bootstrap.boot()

    assert context.container is not None

    assert context.events is not None
