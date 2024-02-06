"""Utilities for debugging and development."""

from copy import deepcopy
from cProfile import Profile
from functools import wraps
from inspect import stack
from logging import Logger
from pstats import Stats
from time import time
from typing import Any, Callable, Optional, TypeAlias

__all__ = ["around", "caller", "deltatime", "profileit"]

CallableAnyT: TypeAlias = Callable[[Any], Any]

DEFAULT_STACK_SIZE: int = 10
DEFAULT_STACK_FRAME: int = 2


def around(before: Optional[Callable] = None, after: Optional[Callable] = None) -> Callable:
    """Add additional behavior before and after execution of decorated function.

    Args:
        before: A reference to afunction/method that must be executed
                BEFORE calling the decorated function.
        after: A reference to afunction/method that must be executed
               AFTER calling the decorated function.

    The decorator highlights additional memory for data exchange
    capabilities between before and after handlers.

    This memory is transferred in the form of additional parameter ("_pipe")
    in the kwargs named argument dictionary.

    Example::

        from pure_utils import around

        def before_handler(*args, **kwargs):
            kwargs["_pipe"]["key"] = "some data (from before to after handlers)"
            print("before!")

        def after_handler(*args, **kwargs):
            print(f"after: {kwargs['_pipe']['key']} !")

        @around(before=before_handler, after=after_handler)
        def func():
            print("in da func")

        func()
        # before!
        # in da func
        # after: some data (from before to after handlers) !
    """

    def decorate(func) -> CallableAnyT:
        @wraps(func)
        def wrapper(*args, **kwargs):
            _buffer = {}
            _args, _kwargs = (deepcopy(args), kwargs.copy())

            if before:
                before(*_args, _pipe=_buffer, **_kwargs)

            result = func(*args, **kwargs)

            if after:
                after(*_args, _pipe=_buffer, **_kwargs)

            return result

        return wrapper

    return decorate


def caller(at_frame: int = DEFAULT_STACK_FRAME) -> str:
    """Get the name of calling function/method (from current function/method context).

    Args:
        at_frame: The frame index number on the call stack (default 2).
                  Need increased with each wrap to decorator.

    Returns:
        The name of calling function/method.

    Example::

        from pure_utils import caller

        def func1(*args, **kwargs):
            print(f"I'am 'func1'. '{caller()}' called me.")

        def func2(*args, **kwargs):
            return func1()

        func2()  # I'am 'func1'. 'func2' called me.
    """
    return str(stack()[at_frame].function)


def deltatime(logger: Optional[Logger] = None) -> Callable:
    """Measure execution time of decorated function and print it to log.

    Args:
        logger: Optional logger object for printing execution time to file.

    Example::

        ...
    """

    def decorate(func) -> CallableAnyT:
        @wraps(func)
        def wrapper(*args, **kwargs):
            t0 = time()
            retval = func(*args, **kwargs)
            delta = float(f"{time() - t0:.3f}")
            if logger:
                logger.debug(f"[DELTATIME]: '{func.__name__}' ({delta} sec.)")
            return retval, delta

        return wrapper

    return decorate


def profileit(logger: Optional[Logger] = None, stack_size: int = DEFAULT_STACK_SIZE) -> Callable:
    """Profile decorated function being with 'cProfile'.

    Args:
        logger: Optional logger object for printing execution time to file.
        stack_size: Stack size limit for profiler results.

    Example::

        ...
    """
    profiler = Profile()

    def decorate(func) -> CallableAnyT:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            try:
                result = profiler.runcall(func, *args, **kwargs)
            finally:
                stack_info = (
                    Stats(profiler)
                    .strip_dirs()
                    .sort_stats("cumulative", "name")
                    .print_stats(stack_size)
                )
                if logger:
                    logger.debug(f"[PROFILEIT]: {stack_info}")
            return result, stack_info

        return wrapper

    return decorate
