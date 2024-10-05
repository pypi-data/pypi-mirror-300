"""This package try to mimic pipe operation by overriding the bitwise-or operator, 
turn it into an infix function that take the output of previous expression as the first argument of the current function.
"""

from typing import Callable, Any, Iterable
from functools import partial


class Pipe(object):
    """This class create the `Pipe` object that mimic pipe operation:

    - instatiate by creating partial of existing function
    - turn the bitwise-or operator `|` into an infix function that accept the output of previous expression.
    ie. pipe operator
    """

    def __init__(self, func: Callable, /, *args, **kwargs) -> None:
        """create pipable partial for the target func

        Args:
            func (Callable): func to be pipable
        """
        self.pipe = partial(func, *args, **kwargs)

    def __ror__(self, precedent: Any):
        """override the builit-in `|` operator, turn it into pipe"""
        # return partial(self.func, precedent)
        return self.pipe(precedent)

    def __rrshift__(self, precedent: Iterable):
        """override the builit-in `>>` operator, pass precedent as destructured iterable to the pipe"""
        return self.pipe(*precedent)

    def __rlshift__(self, precedent: dict):
        """override the builit-in `<<` operator, pass as destructured dict to the pipe"""
        return self.pipe(**precedent)

    def __call__(self, *args, **kwargs):
        """replace arguments of the pipable partial"""
        return Pipe(self.pipe.func, *args, **kwargs)
