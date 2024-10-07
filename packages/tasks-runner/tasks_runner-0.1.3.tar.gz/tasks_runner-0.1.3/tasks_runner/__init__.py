from loguru import logger
from ._tasks_runner import TasksRunner

__version__ = "0.1.3"

logger.disable('tasks_runner')

__all__ = [
  'TasksRunner',
]
