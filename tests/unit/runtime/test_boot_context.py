from platform_core.kernel import Bootstrap


def test_boot_context() -> None:

    context = Bootstrap().boot()

    assert context.container is not None

    assert context.events is not None
