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


class ProfileResultPresenter:
    def __init__(self, stats: Stats, amount: int) -> None:
        self.stats = stats
        self.amount = amount

    @property
    def indent(self) -> str:
        return " " * 8

    @property
    def title(self) -> str:
        return "   ncalls  tottime  percall  cumtime  percall filename:lineno(function)"

    def f8(self, x: float) -> str:
        return f"{x:8.3f}"

    def func_std_string(self, func_name) -> str:
        if func_name[:2] == ("~", 0):
            # special case for built-in functions
            name = func_name[2]
            if name.startswith("<") and name.endswith(">"):
                return "{%s}" % name[1:-1]
            else:
                return name
        else:
            return "%s:%d(%s)" % func_name

    def print_line(self, func) -> str:
        lines = []
        cc, nc, tt, ct, callers = self.stats.stats[func]
        c = str(nc)

        if nc != cc:
            c = c + "/" + str(cc)

        lines.append(f"{c.rjust(9)} ")
        lines.append(f"{self.f8(tt)} ")

        if nc == 0:
            lines.append(f"{self.indent} ")
        else:
            lines.append(f"{self.f8(tt/nc)} ")

        lines.append(f"{self.f8(ct)} ")

        if cc == 0:
            lines.append(f"{self.indent} ")
        else:
            lines.append(f"{self.f8(ct/cc)} ")

        lines.append(self.func_std_string(func))

        return "".join(lines)

    def get_print_list(self) -> tuple[int, int]:
        width = self.stats.max_name_len

        if self.stats.fcn_list:
            stat_list = self.stats.fcn_list[:]
        else:
            stat_list = list(self.stats.stats.keys())

        count = len(stat_list)

        if not stat_list:
            return 0, stat_list

        if count < len(self.stats.stats):
            width = 0
            for func in stat_list:
                if len(self.func_std_string(func)) > width:
                    width = len(self.func_std_string(func))

        return width + 2, stat_list

    def present(self) -> str:
        lines = []

        for filename in self.stats.files:
            lines.append(filename)

        for func in self.stats.top_level:
            lines.append(f"{self.indent}{func[2]}")

        lines.append(f"{self.stats.total_calls} function calls ")

        if self.stats.total_calls != self.stats.prim_calls:
            lines.append(f"({self.stats.prim_calls!r} primitive calls) ")

        lines.append(f"in {self.stats.total_tt:.3f} seconds\n\n")

        width, list = self.get_print_list()

        if list:
            lines.append("Ordered by: cumulative time, function name\n\n")
            lines.append(f"{self.title}\n")
            for func in list:
                lines.append(f"{self.print_line(func)}\n")

        return "".join(lines)


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

    Raises:
        ValueError: If one of the handlers (`before`, `after`) is not specified.

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

        # !!! Use around with only BEFORE handler !!!
        @around(before=before_handler)
        def func2():
            print("in da func2")
        # before!
        # in da func2

        # !!! Use around with only AFTER handler !!!
        @around(after=after_handler)
        def func3():
            print("in da func3")
        # after!
        # in da func3
    """

    def decorate(func) -> CallableAnyT:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not before and not after:
                raise ValueError(
                    "One of the handlers (`before`, `after`) is not specified. Read the doc - "
                    "https://p3t3rbr0.github.io/py3-pure-utils/refs/debug.html#debug.around"
                )

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
            print(f"I'am 'func1', '{caller()}' called me.")

        def func2(*args, **kwargs):
            return func1()

        func2()  # I'am 'func1', 'func2' called me.
    """
    return str(stack()[at_frame].function)


def deltatime(logger: Optional[Logger] = None) -> Callable:
    """Measure execution time of decorated function and print it to log.

    Args:
        logger: Optional logger object for printing execution time to file.

    Example::

        from pure_utils import deltatime

        @deltatime()
        def aim_func():
            for _ in range(1, 1000_000):
                ...

        result, delta = aim_func()
        print(f"Execution time of aim_func: {delta} sec.")
        # Execution time of aim_func: 0.025 sec.

        # !!! Or use decorator with logger (side effect) !!!

        from logging import getLogger, DEBUG, basicConfig
        basicConfig(level=DEBUG)

        @deltatime(logger=getLogger())
        def aim_func2():
            for _ in range(1, 1000_000):
                ...

        result, _ = aim_func2()
        # DEBUG:root:[DELTATIME]: 'aim_func2' (0.025 sec.)
    """

    def decorate(func) -> CallableAnyT:
        @wraps(func)
        def wrapper(*args, **kwargs) -> tuple[Any, float]:
            t0 = time()
            retval = func(*args, **kwargs)
            delta = float(f"{time() - t0:.3f}")
            if logger:
                logger.log(msg=f"[DELTATIME]: '{func.__name__}' ({delta} sec.)", level=logger.level)
            return retval, delta

        return wrapper

    return decorate


def profileit(logger: Optional[Logger] = None, stack_size: int = DEFAULT_STACK_SIZE) -> Callable:
    """Profile decorated function being with 'cProfile'.

    Args:
        logger: Optional logger object for printing execution time to file.
        stack_size: Stack size limit for profiler results.

    Example::

    from pure_utils import profileit

    def func1():
        ...

    def func2():
        func1()

    def func3():
        func2()

    @profileit()
    def func4():
        func3()

    _, profile_info = func4()
    print(profile_info)
    # 5 function calls in 0.000 seconds
    #    Ordered by: cumulative time, function name
    #    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    #         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
    #         1    0.000    0.000    0.000    0.000 scriptname.py:13(func4)
    #         1    0.000    0.000    0.000    0.000 scriptname.py:10(func3)
    #         1    0.000    0.000    0.000    0.000 scriptname.py:7(func2)
    #         1    0.000    0.000    0.000    0.000 scriptname.py:4(func1)
    # <pstats.Stats object at 0x10cf1a390>

    # !!! Or use decorator with logger (side effect) !!!

    from logging import getLogger, DEBUG, basicConfig
    basicConfig(level=DEBUG)

    @profileit(logger=getLogger())
    def func4():
        func3()

    func4()
    """
    profiler = Profile()

    def decorate(func) -> CallableAnyT:
        @wraps(func)
        def wrapper(*args, **kwargs) -> tuple[Any, Stats]:
            retval = None
            try:
                retval = profiler.runcall(func, *args, **kwargs)
            finally:
                profiler_stats = Stats(profiler).strip_dirs().sort_stats("cumulative", "name")

                # s = stats2str(profiler_stats, stack_size)
                s = ProfileResultPresenter(profiler_stats, stack_size).present()
                if logger:
                    # logger.log(msg=f"[PROFILEIT]: {s}", level=logger.level)
                    print(s)
            return retval, profiler_stats

        return wrapper

    return decorate
