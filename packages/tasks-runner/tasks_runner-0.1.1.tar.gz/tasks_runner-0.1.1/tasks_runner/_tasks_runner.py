# pylint: disable=missing-function-docstring, missing-module-docstring, missing-class-docstring
from collections.abc import Hashable, Iterator, Callable
import random
import sys
from threading import Lock
import time
from typing import Generic, TypeVar
import concurrent.futures as cf

from loguru import logger
from tqdm import tqdm

from ._utils import chainable
from ._task import Task, Tasks

T = TypeVar('T', bound=Hashable)

class TasksRunner(Generic[T]):
    total: int
    _steps: list[Callable]

    _pending_tasks: Tasks
    _pending_tasks_lock: Lock = Lock()

    _results: dict[int, Task] = {}
    _results_lock: Lock = Lock()

    _running_tasks: Tasks = set()
    _running_tasks_lock: Lock = Lock()

    def __init__(self,
                 data: list[T],
                 steps: list[Callable],
                 max_workers: int | None = None,
                 max_retries: int = 3):
        logger.trace('__init__')
        self.total = len(data) * len(steps)
        self._steps = steps
        self._pending_tasks = Task.create_tasks(data, len(steps), max_retries)

        self.max_workers = max_workers

    def _is_done(self) -> bool:
        logger.trace('_is_done')
        with self._pending_tasks_lock, self._running_tasks_lock:
            return len(self._pending_tasks) == 0 and len(self._running_tasks) == 0

    def _submit_task(self, task: Task):
        logger.trace('_submit_task')
        if task.done:
            with self._results_lock:
                self._results[task.i] = task
        else:
            with self._pending_tasks_lock:
                self._pending_tasks.add(task)

    def _remove_running_task(self, task: Task):
        logger.trace('_remove_running_task')
        with self._running_tasks_lock:
            self._running_tasks.remove(task)

    def _fetch_task_to_run(self) -> Task:
        logger.trace('_fetch_task_to_run')
        with self._pending_tasks_lock, self._running_tasks_lock:
            task = random.choice(list(self._pending_tasks))
            self._pending_tasks.remove(task)
            self._running_tasks.add(task)
            return task

    def _run_task(self, task: Task) -> bool:
        logger.trace('_run_task')

        try:
            next_task = task.run_step(self._steps)
            self._submit_task(next_task)
            return next_task.retries == 0

        finally:
            self._remove_running_task(task)

    @chainable
    def run(self) -> None:
        logger.trace('run')
        with (
            cf.ThreadPoolExecutor(max_workers=self.max_workers) as executor,
            tqdm(total=self.total) as pbar,
        ):
            for x in self.pending_tasks():
                future = executor.submit(self._run_task, x)
                future.add_done_callback(lambda res: pbar.update(1) if res.result() else None)
                if exc := future.exception():
                    logger.error(exc)
                    sys.exit(1)

    def collect(self) -> list[T]:
        logger.trace('collect')

        return [self._results[i].value for i in range(len(self._results))]

    def pending_tasks(self) -> Iterator[Task]:
        logger.trace('pending_tasks')
        while not self._is_done():
            if len(self._pending_tasks) > 0:
                yield self._fetch_task_to_run()
            else:
                logger.debug('Waiting for tasks to finish')
                time.sleep(0.1)


__all__ = [
  'TasksRunner',
]
