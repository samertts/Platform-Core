from platform_core.engine.lifecycle import LifecycleState
from platform_core.engine.lifecycle_machine import LifecycleMachine

import pytest


def test_initial_state():

    machine = LifecycleMachine()

    assert machine.state is LifecycleState.CREATED


def test_happy_path():

    machine = LifecycleMachine()

    machine.configure()
    machine.initialize()
    machine.ready()
    machine.running()
    machine.completed()
    machine.disposed()

    assert machine.state is LifecycleState.DISPOSED


def test_failure_path():

    machine = LifecycleMachine()

    machine.configure()
    machine.initialize()
    machine.ready()
    machine.running()
    machine.failed()
    machine.disposed()

    assert machine.state is LifecycleState.DISPOSED


def test_cancel_path():

    machine = LifecycleMachine()

    machine.configure()
    machine.initialize()
    machine.ready()
    machine.running()
    machine.cancelled()
    machine.disposed()

    assert machine.state is LifecycleState.DISPOSED


def test_invalid_transition():

    machine = LifecycleMachine()

    with pytest.raises(RuntimeError):

        machine.completed()


def test_history():

    machine = LifecycleMachine()

    machine.configure()
    machine.initialize()

    assert machine.history == (
        LifecycleState.CREATED,
        LifecycleState.CONFIGURED,
        LifecycleState.INITIALIZED,
    )
