from platform_core.host.application_host import ApplicationHost


def test_application_host():

    host = ApplicationHost()

    context = host.boot()

    assert context.kernel.lifecycle.running

    assert context.container is not None

    assert context.events is not None
