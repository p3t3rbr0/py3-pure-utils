"""Private module for encapsulating low-level work with profiler stats."""

from pstats import Stats
from typing import Iterable, Mapping, Sequence, TypeAlias

ProfilerStatsT: TypeAlias = str | bytes | Mapping


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

    def serialize(self) -> ProfilerStatsT:
        """Interface for serialization method of profiling results.

        Must be implemented in child classes.

        Raises:
            NotImplementedError: If called directly.
        """
        raise NotImplementedError


class StringPStatsSerializer(PStatsSerializer):
    """Serialize profiler result to string."""

    def __init__(self, *args, **kwargs):
        """Initialize serializer."""
        super().__init__(*args, **kwargs)

        self.indent = " " * 8
        self.title = "   ncalls  tottime  percall  cumtime  percall filename:lineno(function)"

    def f8(self, x: float) -> str:
        """Convert float to float with eight digits before point and three digits after point."""
        return f"{x:8.3f}"

    def func_std_string(self, func_name) -> str:
        """Prepare a PStats function according to a string pattern."""
        if func_name[:2] == ("~", 0):
            # special case for built-in functions
            name = func_name[2]
            if name.startswith("<") and name.endswith(">"):
                return "{%s}" % name[1:-1]
            else:
                return name
        else:
            return "%s:%d(%s)" % func_name

    def prepare_func_line(self, func) -> str:
        """Prepare the PStats function as a string representation."""
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

    def get_func_list(self) -> Sequence[str]:
        """Get list of PStats functions."""
        if self.pstats.fcn_list:
            return self.pstats.fcn_list[:]

        return list(self.pstats.stats.keys())

    def serialize(self) -> str:
        """Serialize PStats object to string."""
        lines = []

        for filename in self.pstats.files:
            lines.append(filename)

        for func in self.pstats.top_level:
            lines.append(f"{self.indent}{func[2]}")

        lines.append(f"{self.pstats.total_calls} function calls ")

        if self.pstats.total_calls != self.pstats.prim_calls:
            lines.append(f"({self.pstats.prim_calls!r} primitive calls) ")

        lines.append(f"in {self.pstats.total_tt:.3f} seconds\n\n")

        func_list = self.get_func_list()

        if func_list:
            lines.append("Ordered by: cumulative time, function name\n\n")
            lines.append(f"{self.title}\n")
            for func in func_list:
                lines.append(f"{self.prepare_func_line(func)}\n")

        return "".join(lines)
