from platform_core.scheduler.engine import SchedulerEngine
from platform_core.scheduler.task import ScheduledTask


def test_scheduler() -> None:

    called = []

    engine = SchedulerEngine()

    engine.queue.enqueue(
        ScheduledTask(
            "test",
            lambda: called.append(True),
        )
    )

    engine.run()

    assert called == [True]
