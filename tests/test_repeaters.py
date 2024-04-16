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
    @repeat(repeater=ExceptionBasedRepeater, exceptions=CustomException)
    def some_repeatable_func(self):
        raise CustomException("some error")

    def test_repeat(self, mocker):
        sleep_mock = mocker.patch("pure_utils.repeaters.sleep")

        with pytest.raises(RepeateError):
            self.some_repeatable_func()

        assert sleep_mock.call_count == 3
        sleep_mock.assert_has_calls([mocker.call(1), mocker.call(2), mocker.call(3)])


# class TestPredicativeBasedRepeater:
#     def test_sample(self):
#         assert True


# class TestRepeat:
#     def test_sample(self):
#         assert True
