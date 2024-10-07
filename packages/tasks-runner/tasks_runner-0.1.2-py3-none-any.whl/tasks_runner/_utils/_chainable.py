"""
This module provides a decorator `chainable` that allows methods to return the instance (`self`)
after execution, enabling method chaining.
The decorated method should return `None` or the instance itself.

Functions:
    chainable(fn: Callable[Concatenate[S, P], None | S]) -> Callable[Concatenate[S, P], S]:
        Decorator that takes a function, and when called, returns self.
"""

from functools import wraps
from typing import TypeVar, ParamSpec, Concatenate
from collections.abc import Callable

S = TypeVar('S', bound=object)
P = ParamSpec('P')
def chainable(fn: Callable[Concatenate[S, P], None | S]) -> Callable[Concatenate[S, P], S]:
    """Decorator that takes a function, and when called, returns self"""
    @wraps(fn)
    def wrapper(*args, **kwargs) -> S:
        fn(*args, **kwargs)
        return args[0]
    return wrapper

__all__ = [
    'chainable',
]
