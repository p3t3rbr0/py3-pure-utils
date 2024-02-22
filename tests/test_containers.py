import pytest

from pure_utils import bisect, first, flatten


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
