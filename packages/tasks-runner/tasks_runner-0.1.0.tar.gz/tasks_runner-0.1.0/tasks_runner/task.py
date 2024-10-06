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
    i: int
    value: T
    step: int
    total_steps: int
    retries: int
    max_retries: int

    @classmethod
    def create_tasks(cls, data: list[T], total_steps: int, max_retries: int) -> set['Task']:
        """Create tasks given a list of data and total steps."""
        logger.trace('create_tasks')
        return {
            cls(i, x, 0, total_steps, 0, max_retries)
            for i, x in enumerate(data)
        }

    def copy(self, **kwargs) -> 'Task':
        """Copy the task modifying the given attributes."""
        logger.trace('copy')
        return Task(**{**dataclasses.asdict(self), **kwargs})

    def run_step(self, steps: list[Callable]):
        """Run the current step of the task."""
        logger.trace('run_step')
        try:
            res = steps[self.step](self.value)
            return self.copy(value=res, step=self.step + 1, retries=0)
        # pylint: disable=broad-except
        except Exception:
            if self.retries >= 3:
                raise
            return self.copy(retries=self.retries + 1)

    @property
    def done(self) -> bool:
        """Check if the task is done."""
        logger.trace('done')
        return self.step >= self.total_steps


Tasks = set[Task]
