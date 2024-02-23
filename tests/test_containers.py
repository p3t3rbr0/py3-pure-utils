import pytest

from pure_utils import bisect, first, flatten, get_or_else, symmdiff


class TestBisect:
    def test_with_non_empty_list(self):
        source_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        a, b = bisect(source_list)

        assert a == [1, 2, 3, 4, 5]
        assert b == [6, 7, 8, 9, 10, 11]

        # Source list not changed.
        assert source_list == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    def test_with_empty_list(self):
        source_list = []

        with pytest.raises(AssertionError):
            bisect(source_list)

        assert source_list == []


class TestFirst:
    def test_with_non_empty_list(self):
        assert first([1, 2, 3]) == 1

    def test_with_non_empty_set(self):
        assert first(set([1, 2, 3])) == 1

    def test_with_non_empty_tuple(self):
        assert first((1, 2, 3)) == 1

    def test_with_empty_list(self):
        assert first([]) is None


class TestFlatten:
    def test_with_one_dimention_list_seequence(self):
        seq = [1, 2, 3, 4, 5]
        result = list(flatten(seq))

        assert result == [1, 2, 3, 4, 5]

    def test_with_one_dimention_set_seequence(self):
        seq = {1, 2, 3, 4, 5}
        result = set(flatten(seq))

        assert result == {1, 2, 3, 4, 5}

    def test_with_one_dimention_tuple_seequence(self):
        seq = (1, 2, 3, 4, 5)
        result = tuple(flatten(seq))

        assert result == (1, 2, 3, 4, 5)

    def test_with_two_dimention_list_seequence(self):
        seq = [[1], [2], [3], [4], [5]]
        result = list(flatten(seq))

        assert result == [1, 2, 3, 4, 5]

    def test_with_two_dimention_tuple_seequence(self):
        seq = ((1,), (2,), (3,), (4,), (5,))
        result = tuple(flatten(seq))

        assert result == (1, 2, 3, 4, 5)

    def test_with_multiple_dimention_list_seequence(self):
        seq = [[[[[[1]]]]], [[[[[2]]]]], [[[[[3]]]]], [[[[[4]]]]], [[[[[5]]]]]]
        result = list(flatten(seq))

        assert result == [1, 2, 3, 4, 5]

    def test_with_multiple_dimention_tuple_seequence(self):
        seq = (
            (((((1,),),),),),
            (((((2,),),),),),
            (((((3,),),),),),
            (((((4,),),),),),
            (((((5,),),),),),
        )
        result = tuple(flatten(seq))

        assert result == (1, 2, 3, 4, 5)


class TestGetOrElse:
    def test_regular_usage(self):
        seq = (1, 2, 3)
        assert get_or_else(seq, 0) == 1
        assert get_or_else(seq, 3) is None
        assert get_or_else(seq, 3, -1) == -1

        seq = ["a", "b", "c"]
        assert get_or_else(seq, 5, "does not exists") == "does not exists"


class TestSymmdiff:
    def test_with_two_lists(self):
        l1 = ["a", "b", "c"]
        l2 = ["e", "b", "a"]
        diff = symmdiff(l1, l2)

        assert sorted(diff) == ["c", "e"]

        # The original lists has not changed
        assert l1 == ["a", "b", "c"]
        assert l2 == ["e", "b", "a"]

    def test_with_two_tuples(self):
        t1 = ("a", "b", "c")
        t2 = ("e", "b", "a")
        diff = symmdiff(t1, t2)

        assert sorted(diff) == ["c", "e"]

    def test_with_two_sets(self):
        s1 = set(["a", "b", "c"])
        s2 = set(["e", "b", "a"])
        diff = symmdiff(s1, s2)

        assert sorted(diff) == ["c", "e"]
