import pytest

from pure_utils import bisect


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
