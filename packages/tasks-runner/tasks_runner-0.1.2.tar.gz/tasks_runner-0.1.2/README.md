# Tasks Runner

Wrapper for `ThreadPoolExecutor` to run tasks concurrently step by step.

## Installation

```bash
pip install tasks-runner
```

## Usage Example

```python
from tasks_runner import TasksRunner

def add1(x):
    return x + 1

def mul2(x):
    return x * 2

def sub3(x):
    return x - 3

steps = [add1, mul2, sub3]
data = [1, 2, 3]

runner = TasksRunner(data, steps)

runner = runner.run()

print(runner.collect())
# [1, 3, 5]
```
