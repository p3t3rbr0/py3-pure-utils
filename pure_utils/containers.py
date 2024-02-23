"""Utilities for working with data containers (lists, dictionaries, tuples, sets, etc.)."""

from typing import Any, Generator, Mapping, Optional, Sequence, TypeVar

__all__ = ["bisect", "first", "flatten", "get_or_else", "symmdiff"]

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

        from pure_utils import flatten

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


def get_or_else(collection: Sequence[T], index: int, default: Optional[T] = None) -> Optional[T]:
    """Get value of element, and if it is missing, return the default value.

    Used for safety to get the value of a collection element.

    Args:
        collection: Collection of homogeneous elements.
        index: Index of the collection element to get the value.
        default: Optional default value, returned when no element at the specified index.

    Returns:
        The value of the sequence element at the specified index,
        or default value, when no element by this index.

    Example::

        from pure_utils import get_or_else

        seq = (1, 2, 3)
        print(get_or_else(seq, 0))  # 1
        print(get_or_else(seq, 3))  # None
        print(get_or_else(seq, 3, -1))  # -1

        seq = ["a", "b", "c"]
        print(get_or_else(seq, 3, "does not exists"))  # does not exists
    """
    try:
        return collection[index]
    except IndexError:
        return default


def symmdiff(s1: Sequence[T], s2: Sequence[T]) -> list[T]:
    """Obtain the symmetric difference of two sequences.

    Args:
        s1: The first sequence to form a set on the LEFT.
        s2: The second sequence to form a set on the RIGHT.

    Returns:
        The symmetric difference of two sequences as a list.

    Example::

         from pure_utils import symmdiff

         s1 = ["a", "b", "c"]
         s2 = ["e", "b", "a"]
         result = symmdiff(s1, s2)
         print(result)  # ["c", "e"]
    """
    return list(set(s1).symmetric_difference(set(s2)))
