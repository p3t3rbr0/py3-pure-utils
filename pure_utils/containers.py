"""Utilities for working with data containers (lists, dictionaries, tuples, sets, etc.)."""

from typing import Any, Generator, Mapping, Optional, Sequence, TypeVar

__all__ = ["bisect"]

T = TypeVar("T")


def bisect(source_list: list[T]) -> tuple[list[T], list[T]]:
    """Bisect the list into two parts/halves based on the number of elements.

    The function does not change the original list.

    Args:
        source_list: Source list.

    Returns:
        A two-element tuple containing two lists:
        the first list represents the first half of the original list,
        and the second list in the tuple is the second half of the original list, respectively.

    Raises:
        AssertionError: Fires if an empty source list is passed.

    Example::

        from pure_utils import bisect

        l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        a, b = bisect(l)
        print(a, b, sep="; ")
        # [1, 2, 3, 4, 5]; [6, 7, 8, 9, 10, 11]
    """
    assert source_list
    length = len(source_list)
    return (source_list[: length // 2], source_list[length // 2 :])
