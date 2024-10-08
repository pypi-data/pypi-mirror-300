"""Task module."""

from collections.abc import Hashable
from typing import TypeVar, Generic, Callable
import dataclasses
from dataclasses import dataclass
from loguru import logger

T = TypeVar('T', bound=Hashable)


@dataclass(frozen=True)
class Task(Generic[T]):
    """Task schema."""
    key: int
    value: T = dataclasses.field(compare=False, hash=False)
    step: int
    retries: int
    max_retries: int

    steps: list[Callable] = dataclasses.field(compare=False, hash=False, repr=False)

    @classmethod
    def create_tasks(cls, data: list[T], steps: list[Callable], max_retries: int = 3):
        """Create tasks given a list of data and total steps."""
        logger.trace('create_tasks')
        return {cls.new(i, x, steps, max_retries) for i, x in enumerate(data)}

    @classmethod
    def new(cls, i: int, value: T, steps: list[Callable], max_retries: int = 3) -> 'Task':
        """Create a new task."""
        logger.trace('new')
        return cls(i, value, 0, 0, max_retries, steps)

    def update(self, **kwargs) -> 'Task':
        """Copy the task modifying the given attributes."""
        logger.trace('copy')
        return Task(**{**dataclasses.asdict(self), **kwargs})

    def run_step(self):
        """Run the current step of the task."""
        logger.trace('run_step')

        if self.done:
            return self

        try:
            res = self.steps[self.step](self.value)
            return self.update(value=res, step=self.step + 1, retries=0)

        # pylint: disable=broad-except
        except Exception:
            if self.retries >= self.max_retries:
                raise

            return self.update(retries=self.retries + 1)

    @property
    def done(self) -> bool:
        """Check if the task is done."""
        logger.trace('done')
        return self.step >= len(self.steps)


Tasks = set[Task]


__all__ = [
    'Task',
    'Tasks',
]
