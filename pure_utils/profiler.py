"""Helper classes for working with the cProfile."""

from cProfile import Profile
from typing import Callable, ParamSpec, Type, TypeVar

from pure_utils._pstats import ProfilerStatsT, PStats, PStatsSerializer

__all__ = ["Profiler"]


T = TypeVar("T")
P = ParamSpec("P")


class Profiler:
    """A class provides a simple interface for profiling code.

    Example::

        from pure_utils import Profiler

        profiler = Profiler()
        some_function_retval = profiler.profile(some_func, *func_args, **func_kwargs)
        profile_result = profiler.serialize_result(SomeProfilerStatsSerializer())
    """

    def __init__(self) -> None:
        """Initialize profiler object."""
        self._profile = Profile()

    @property
    def pstats(self) -> PStats:
        """Get raw profile stats."""
        return PStats(self._profile).strip_dirs().sort_stats("cumulative", "name")

    def profile(self, func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
        """Profile function.

        Args:
            func: Function for profiling
            *args: Profiling function positional arguments.
            **kwargs: Profiling function named arguments.

        Return:
            Native profiling function return value.
        """
        return self._profile.runcall(func, *args, **kwargs)

    def serialize_result(
        self, *, serializer: Type[PStatsSerializer], stack_size: int
    ) -> ProfilerStatsT:
        """Serialize profiler result with custom serializer class.

        Args:
            serializer: Serializer class.
            stack_size: Stack size for limitation

        Returns:
            Serialized profiler result.
        """
        return serializer(self.pstats, stack_size).serialize()
