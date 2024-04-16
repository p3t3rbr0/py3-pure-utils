import pytest

from pure_utils.repeaters import (
    ExceptionBasedRepeater,
    PredicativeBasedRepeater,
    RepeateError,
    repeat,
)


class CustomException(Exception):
    pass


class TestExceptionBasedRepeater:
    @repeat(ExceptionBasedRepeater(exceptions=(CustomException,), attempts=5, interval=1))
    def some_repeatable_func(self):
        raise CustomException("some error")

    def test_repeat(self, mocker):
        sleep_mock = mocker.patch("pure_utils.repeaters.sleep")

        with pytest.raises(RepeateError):
            self.some_repeatable_func()

        assert sleep_mock.call_count == 5
        sleep_mock.assert_has_calls(
            [mocker.call(1), mocker.call(2), mocker.call(3), mocker.call(4), mocker.call(5)]
        )


# class TestPredicativeBasedRepeater:
#     def test_sample(self):
#         assert True


# class TestRepeat:
#     def test_sample(self):
#         assert True
