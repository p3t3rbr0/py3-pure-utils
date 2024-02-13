"""Helper classes for working with the cProfile."""

from cProfile import Profile
from pstats import Stats
from typing import Any, Mapping, Sequence, Type, TypeAlias

SerializedStatsT: TypeAlias = str | bytes | Mapping


class BaseStatsSerializer:
    """Base class for serializer of profiling results."""

    def __init__(self, stats: Stats, amount: int) -> None:
        self.stats = stats
        self.amount = amount

    def serialize(self) -> SerializedStatsT:
        """Interface for serialization method of profiling results.

        Must be implemented in child classes.

        Raises:
            NotImplementedError: If called directly.
        """
        raise NotImplementedError


class Profiler:
    """..."""

    def __init__(self) -> None:
        self._profile = Profile()

    @property
    def stats(self) -> Stats:
        """...

        Returns:
            ...
        """
        return Stats(self._profile).strip_dirs().sort_stats("cumulative", "name")

    def profile(self, func, *args, **kwargs) -> Any:
        """...

        Args:
            func: ...
            *args: ...
            **kwargs: ...
        """
        self._profile.runcall(func, *args, **kwargs)

    def serialize_stats(self, *, serializer: Type[BaseStatsSerializer], stack_size: int) -> str:
        """...

        Args:
            serializer: ...
            stack_size: ...

        Returns:
            ....
        """
        return serializer(self.stats, stack_size).serialize()


class StringProfileStatsSerializer(BaseStatsSerializer):
    """..."""

    @property
    def indent(self) -> str:
        """...

        Returns:
            ...
        """
        return " " * 8

    @property
    def title(self) -> str:
        """...

        Returns:
            ...
        """
        return "   ncalls  tottime  percall  cumtime  percall filename:lineno(function)"

    def f8(self, x: float) -> str:
        """...

        Returns:
            ...
        """
        return f"{x:8.3f}"

    def func_std_string(self, func_name) -> str:
        """...

        Args:
            func_name: ...

        Returns:
            ...
        """
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
        """...

        Args:
            func: ...

        Returns:
            ...
        """
        lines = []
        cc, nc, tt, ct, callers = self.stats.stats[func]  # type: ignore
        c = str(nc)

        if nc != cc:
            c = c + "/" + str(cc)

        lines.append(f"{c.rjust(9)} ")
        lines.append(f"{self.f8(tt)} ")

        if nc == 0:
            lines.append(f"{self.indent} ")
        else:
            lines.append(f"{self.f8(tt / nc)} ")

        lines.append(f"{self.f8(ct)} ")

        if cc == 0:
            lines.append(f"{self.indent} ")
        else:
            lines.append(f"{self.f8(ct / cc)} ")

        lines.append(self.func_std_string(func))

        return "".join(lines)

    def get_func_list(self) -> tuple[int, Sequence]:
        """...

        Returns:
            ...
        """
        width = self.stats.max_name_len  # type: ignore

        if self.stats.fcn_list:  # type: ignore
            func_list = self.stats.fcn_list[:]  # type: ignore
        else:
            func_list = list(self.stats.stats.keys())  # type: ignore

        count = len(func_list)

        if not func_list:
            return 0, func_list

        if count < len(self.stats.stats):  # type: ignore
            width = 0
            for func in func_list:
                if len(self.func_std_string(func)) > width:
                    width = len(self.func_std_string(func))

        return width + 2, func_list

    def serialize(self) -> str:
        """...

        Returns:
            ...
        """
        lines = []

        for filename in self.stats.files:  # type: ignore
            lines.append(filename)

        for func in self.stats.top_level:  # type: ignore
            lines.append(f"{self.indent}{func[2]}")

        lines.append(f"{self.stats.total_calls} function calls ")  # type: ignore

        if self.stats.total_calls != self.stats.prim_calls:  # type: ignore
            lines.append(f"({self.stats.prim_calls!r} primitive calls) ")  # type: ignore

        lines.append(f"in {self.stats.total_tt:.3f} seconds\n\n")  # type: ignore

        _, func_list = self.get_func_list()

        if func_list:
            lines.append("Ordered by: cumulative time, function name\n\n")
            lines.append(f"{self.title}\n")
            for func in func_list:
                lines.append(f"{self.print_line(func)}\n")

        return "".join(lines)
