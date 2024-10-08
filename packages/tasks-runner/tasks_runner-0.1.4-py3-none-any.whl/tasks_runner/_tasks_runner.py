# pylint: disable=missing-function-docstring, missing-module-docstring, missing-class-docstring
from collections.abc import Iterator, Callable
import random
from threading import Lock
import time
from typing import Generic, Literal, TypeVar
import concurrent.futures as cf

from loguru import logger
from tqdm import tqdm

from ._utils import chainable
from ._task import Task, Tasks

T = TypeVar('T')

TaskState = Literal['PENDING', 'RUNNING', 'DONE']

class TasksRunner(Generic[T]):
    total: int
    _steps: list[Callable]

    _tasks: dict[TaskState, Tasks]
    _locks: dict[TaskState, Lock]

    __pbar: tqdm | None

    _exceptions: list[BaseException]
    _exceptions_lock: Lock

    def __init__(self,
                 data: list[T],
                 steps: list[Callable],
                 max_workers: int | None = None,
                 max_retries: int = 3):
        logger.trace('__init__')
        self.total = len(data) * len(steps)
        self._steps = steps

        self._tasks = {
            'PENDING': Task.create_tasks(data, steps, max_retries),
            'RUNNING': set(),
            'DONE': set(),
        }
        self._locks = {
            'PENDING': Lock(),
            'RUNNING': Lock(),
            'DONE': Lock(),
        }

        self.max_workers = max_workers

        self.__pbar = None

        self._exceptions = []
        self._exceptions_lock = Lock()

    def __del__(self):
        logger.trace('__del__')
        self._close_pbar()

    @property
    def _pbar(self) -> tqdm:
        logger.trace('_pbar')
        if self.__pbar is None:
            self.__pbar = tqdm(total=self.total)
        return self.__pbar

    def _close_pbar(self):
        logger.trace('_close_pbar')
        if self.__pbar is None:
            return

        self.__pbar.close()
        self.__pbar = None

    def _is_done(self) -> bool:
        logger.trace('_is_done')
        with self._locks['PENDING'], self._locks['RUNNING']:
            return len(self._tasks['PENDING']) == 0 and len(self._tasks['RUNNING']) == 0

    def _submit_task(self, task: Task):
        logger.trace('_submit_task')
        key: TaskState = 'DONE' if task.done else 'PENDING'
        with self._locks[key]:
            self._tasks[key].add(task)

    def _remove_running_task(self, task: Task):
        logger.trace('_remove_running_task')
        with self._locks['RUNNING']:
            self._tasks['RUNNING'].remove(task)

    def _fetch_task_to_run(self) -> Task:
        logger.trace('_fetch_task_to_run')
        with self._locks['PENDING'], self._locks['RUNNING']:
            task = random.choice(list(self._tasks['PENDING']))
            self._tasks['PENDING'].remove(task)
            self._tasks['RUNNING'].add(task)
            return task

    def _run_task(self, task: Task) -> bool:
        logger.trace('_run_task')

        try:
            next_task = task.run_step()
            self._submit_task(next_task)
            return next_task.retries == 0

        finally:
            self._remove_running_task(task)

    @chainable
    def run(self) -> None:
        logger.trace('run')

        with cf.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for x in self.pending_tasks():
                future = executor.submit(self._run_task, x)
                future.add_done_callback(self._done_callback)

        self._close_pbar()
        self._raise_first_exception()

    def _done_callback(self, future: cf.Future):
        logger.trace('_done_callback')
        if e := future.exception():
            with self._exceptions_lock:
                self._exceptions.append(e)
            return

        if future.result():
            with self._pbar.get_lock():
                self._pbar.update(1)


    def collect(self) -> list[T]:
        logger.trace('collect')

        as_dict = {x.key: x for x in self._tasks['DONE']}
        return [as_dict[i].value for i in range(len(as_dict))]

    def pending_tasks(self) -> Iterator[Task]:
        logger.trace('pending_tasks')
        while not self._is_done():
            self._raise_first_exception()
            if len(self._tasks['PENDING']) > 0:
                yield self._fetch_task_to_run()
            else:
                logger.debug('Waiting for tasks to finish')
                time.sleep(0.1)

    def _raise_first_exception(self):
        with self._exceptions_lock:
            if len(self._exceptions) > 0:
                raise self._exceptions[0]


__all__ = [
  'TasksRunner',
]
