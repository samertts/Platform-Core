from platform_core.scheduler.queue import TaskQueue
from platform_core.scheduler.task import ScheduledTask


def test_queue():

    queue = TaskQueue()

    queue.enqueue(
        ScheduledTask(
            "x",
            lambda: None,
        )
    )

    assert len(queue) == 1

    queue.dequeue()

    assert queue.empty()
