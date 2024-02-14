"""Private module for encapsulating low-level work with profiler stats."""

from pstats import Stats
from typing import Iterable, Mapping, Sequence, TypeAlias

SerializedPStatsT: TypeAlias = str | bytes | Mapping


class PStats(Stats):
    """A dummy override to explicitly describe class attributes.

    In the standard library, attributes are not defined in the constructor,
    which breaks the type analyzer.
    """

    def __init__(self, *args, stream=None) -> None:
        """Initialize profile stats object."""
        self.all_callees = None
        self.files: Sequence = []
        self.fcn_list = None
        self.total_tt = 0
        self.total_calls = 0
        self.prim_calls = 0
        self.max_name_len = 0
        self.top_level: Iterable = set()
        self.stats: Mapping = {}
        self.sort_arg_dict: Mapping = {}

        super().__init__(*args, stream)


class PStatsSerializer:
    """Base class for serializer of profiling results."""

    def __init__(self, pstats: PStats, amount: int) -> None:
        """Initialize base stats serializer object."""
        self.pstats = pstats
        self.amount = amount

    def serialize(self) -> SerializedPStatsT:
        """Interface for serialization method of profiling results.

        Must be implemented in child classes.

        Raises:
            NotImplementedError: If called directly.
        """
        raise NotImplementedError


class StringPStatsSerializer(PStatsSerializer):
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
        cc, nc, tt, ct, callers = self.pstats.stats[func]
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
        width = self.pstats.max_name_len

        if self.pstats.fcn_list:
            func_list = self.pstats.fcn_list[:]
        else:
            func_list = list(self.pstats.stats.keys())

        count = len(func_list)

        if not func_list:
            return 0, func_list

        if count < len(self.pstats.stats):
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

        for filename in self.pstats.files:
            lines.append(filename)

        for func in self.pstats.top_level:
            lines.append(f"{self.indent}{func[2]}")

        lines.append(f"{self.pstats.total_calls} function calls ")

        if self.pstats.total_calls != self.pstats.prim_calls:
            lines.append(f"({self.pstats.prim_calls!r} primitive calls) ")

        lines.append(f"in {self.pstats.total_tt:.3f} seconds\n\n")

        _, func_list = self.get_func_list()

        if func_list:
            lines.append("Ordered by: cumulative time, function name\n\n")
            lines.append(f"{self.title}\n")
            for func in func_list:
                lines.append(f"{self.print_line(func)}\n")

        return "".join(lines)
