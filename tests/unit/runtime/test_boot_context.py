from platform_core.kernel import Bootstrap


def test_boot_context():

    context = Bootstrap().boot()

    assert context.container is not None

    assert context.events is not None
