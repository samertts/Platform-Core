from platform_core.execution.command import Command
from platform_core.execution.dispatcher import CommandDispatcher
from platform_core.execution.handler import CommandHandler


class Create(Command):
    pass


class Handler(CommandHandler):
    def __init__(self) -> None:

        self.called = False

    def handle(
        self,
        command: Command,
    ) -> None:

        self.called = True


def test_dispatch() -> None:

    handler = Handler()

    CommandDispatcher().dispatch(
        handler,
        Create(),
    )

    assert handler.called
