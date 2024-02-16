from logging import getLogger

import pytest
from debug import around, caller, deltatime, profileit


class TestAround:
    def before_handler(self, *args, **kwargs):
        assert "_pipe" in kwargs
        assert kwargs["_pipe"] == {}
        kwargs["_pipe"]["key"] = "some data (from before to after handlers)"

    def after_handler(self, *args, **kwargs):
        assert kwargs["_pipe"]["key"] == "some data (from before to after handlers)"

    def after_handler_without_pipe(self, *args, **kwargs):
        assert kwargs["_pipe"] == {}

    @around(before=before_handler, after=after_handler)
    def func1(self, *args, **kwargs):
        return "some result"

    @around(before=before_handler)
    def func2(self, *args, **kwargs):
        return "some result"

    @around(after=after_handler_without_pipe)
    def func3(self, *args, **kwargs):
        return "some result"

    @around()
    def func4(self, *args, **kwargs):
        return "some result"

    def test_with_before_and_after_handlers(self):
        assert self.func1() == "some result"

    def test_with_before_handler_only(self):
        assert self.func2() == "some result"

    def test_with_after_handler_only(self):
        assert self.func3() == "some result"

    def test_without_before_and_after_handlers(self):
        with pytest.raises(ValueError) as excinfo:
            self.func4()
            assert excinfo.value.message == (
                "One of the handlers (`before`, `after`) is not specified. Read the doc - "
                "https://p3t3rbr0.github.io/py3-pure-utils/refs/debug.html#debug.around"
            )


class TestCaller:
    def func1(self, at_frame=2):
        return caller(at_frame)

    def func2(self, *args, **kwargs):
        return self.func1(*args, **kwargs)

    def func3(self, *args, **kwargs):
        return self.func2(*args, **kwargs)

    def func4(self, *args, **kwargs):
        return self.func3(*args, **kwargs)

    def test_with_default_params(self):
        assert self.func2() == "func2"
        assert self.func4() == "func2"

    def test_with_at_frame(self):
        assert self.func3(at_frame=3) == "func3"
        assert self.func4(at_frame=4) == "func4"


class TestDeltatime:
    @deltatime()
    def func(self):
        return True

    @deltatime(logger=getLogger())
    def func2(self):
        return True

    def test_with_side_effect(self, mocker):
        log_mock = mocker.patch("logging.Logger.log")

        retval, delta = self.func2()

        assert retval is True
        assert isinstance(delta, float)
        log_mock.assert_called_once()

    def test_without_side_effect(self, mocker):
        log_mock = mocker.patch("logging.Logger.log")

        retval, delta = self.func()

        assert retval is True
        assert isinstance(delta, float)
        log_mock.assert_not_called()


class TestProfileit:
    def test_sample(self):
        assert True
