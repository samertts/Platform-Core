from platform_core.execution.command import Command


class CreateUser(Command):
    pass


def test_command() -> None:

    cmd = CreateUser()

    assert isinstance(cmd, Command)
