"""Helper classes for working with the cProfile."""

from cProfile import Profile
from typing import Any, Type

from pure_utils._pstats import PStats, PStatsSerializer, SerializedPStatsT

__all__ = ["Profiler"]


class Profiler:
    """..."""

    def __init__(self) -> None:
        """Initialize profiler object."""
        self._profile = Profile()

    @property
    def pstats(self) -> PStats:
        """...

        Returns:
            ...
        """
        return PStats(self._profile).strip_dirs().sort_stats("cumulative", "name")

    def profile(self, func, *args, **kwargs) -> Any:
        """...

        Args:
            func: ...
            *args: ...
            **kwargs: ...
        """
        self._profile.runcall(func, *args, **kwargs)

    def serialize_stats(
        self, *, serializer: Type[PStatsSerializer], stack_size: int
    ) -> SerializedPStatsT:
        """...

        Args:
            serializer: ...
            stack_size: ...

        Returns:
            ....
        """
        return serializer(self.pstats, stack_size).serialize()
