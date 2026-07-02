from __future__ import annotations

from platform_core.scheduler.task import ScheduledTask


class TaskQueue:

    def __init__(self) -> None:

        self._tasks: list[ScheduledTask] = []

    def enqueue(
        self,
        task: ScheduledTask,
    ) -> None:

        self._tasks.append(task)

    def dequeue(
        self,
    ) -> ScheduledTask:

        return self._tasks.pop(0)

    def empty(
        self,
    ) -> bool:

        return len(self._tasks) == 0

    def __len__(
        self,
    ) -> int:

        return len(self._tasks)
