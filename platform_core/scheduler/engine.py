from __future__ import annotations

from platform_core.scheduler.queue import TaskQueue


class SchedulerEngine:

    def __init__(self) -> None:

        self._queue = TaskQueue()

    @property
    def queue(
        self,
    ) -> TaskQueue:

        return self._queue

    def run(
        self,
    ) -> None:

        while not self._queue.empty():

            task = self._queue.dequeue()

            task.action()
