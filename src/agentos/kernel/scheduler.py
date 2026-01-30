from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List


@dataclass
class ScheduledTask:
    name: str
    handler: Callable[[], None]


class Scheduler:
    def __init__(self) -> None:
        self._queue: List[ScheduledTask] = []

    def add(self, task: ScheduledTask) -> None:
        self._queue.append(task)

    def run_once(self) -> None:
        if not self._queue:
            return
        task = self._queue.pop(0)
        task.handler()
