"""Utilities for working with data containers (lists, dictionaries, tuples, sets, etc.)."""

from typing import Generator, Optional, Sequence, TypeVar

__all__ = ["bisect", "first", "flatten"]

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


def first(collection: Sequence[T]) -> Optional[T]:
    """Get the value of the first element from a homogeneous collection.

    Args:
        collection: Collection of homogeneous elements.

    Returns:
        The value of the first element of the collection, or None if there is none.

    Example::

        from pure_utils import first

        seq = (1, 2, 3)
        print(first(seq))  # 1

        seq = []
        print(first(seq))  # None
    """
    return next((_ for _ in collection), None)


def flatten(collection: Sequence[T]) -> Generator[Sequence[T] | T, None, None]:
    """Make the iterated collection a flat (single nesting level).

    Args:
        collection: Collection of homogeneous elements.

    Returns:
        Generator of the flatten function.

    Example::

        seq = [[1], [2], [3], [4], [5]]
        result = list(flatten(seq))
        print(result)  # [1, 2, 3, 4, 5]

        seq = [[[[[[1]]]]], [[[[[2]]]]], [[[[[3]]]]], [[[[[4]]]]], [[[[[5]]]]]]
        result = list(flatten(seq))
        print(result)  # [1, 2, 3, 4, 5]
    """
    if isinstance(collection, (list, tuple, set)):
        for _ in collection:
            yield from flatten(_)
    else:
        yield collection
