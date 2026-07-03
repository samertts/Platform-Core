from platform_core.host.application_host import ApplicationHost


def test_boot() -> None:

    host = ApplicationHost()

    context = host.boot()

    assert context is host.context

    assert context.container is not None

    assert context.kernel is not None

    assert context.events is not None

    assert context.kernel.lifecycle.running
