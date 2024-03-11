import time
from functools import wraps
from logging import Logger
from typing import Any, Callable, Optional, ParamSpec, Type, TypeVar

T = TypeVar("T")
P = ParamSpec("P")
ExceptionT = Type[BaseException]


class ExecuteError(Exception):
    pass


class RepeateError(Exception):
    pass


class BaseRepeater:
    def __init__(
        self,
        fn: Callable,
        *,
        attempts: int,
        sleep_interval: int,
        logger: Optional[Logger] = None,
    ) -> None:
        self.fn = fn
        self.attempts = attempts
        self.sleep_interval = sleep_interval
        self.logger = logger

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Any:
        for attempt in range(self.attempts):
            step = attempt + 1

            try:
                return self.execute(*args, **kwargs)
            except ExecuteError as exc:
                if self.logger:
                    self.logger.warning(
                        f"Function '{self.fn.__name__}' failed! "
                        f"{self.attempts - step} attempts left.\n{exc}"
                    )

                if self.sleep_interval:
                    time.sleep(step * self.sleep_interval)

        raise RepeateError(f"No success for '{self.fn.__name__}' after {self.attempts} attempts.")

    def execute(self, *args, **kwargs) -> Any:
        raise NotImplementedError


class ExceptionBasedRepeater(BaseRepeater):
    def __init__(
        self,
        fn: Callable,
        *,
        attempts: int,
        sleep_interval: int,
        exceptions: ExceptionT | tuple[ExceptionT, ...],
        logger: Optional[Logger] = None,
    ) -> None:
        super().__init__(fn, attempts=attempts, sleep_interval=sleep_interval, logger=logger)
        self.exceptions = exceptions

    def execute(self, *args: P.args, **kwargs: P.kwargs) -> Any:
        try:
            return self.fn(*args, **kwargs)
        except self.exceptions as exc:
            raise ExecuteError(str(exc))


class PredicativeBasedRepeater(BaseRepeater):
    def __init__(
        self,
        fn: Callable,
        *,
        attempts: int,
        sleep_interval: int,
        predicate: Callable,
        logger: Optional[Logger] = None,
    ) -> None:
        super().__init__(fn, attempts=attempts, sleep_interval=sleep_interval, logger=logger)
        self.predicate = predicate

    def execute(self, *args: P.args, **kwargs: P.kwargs) -> Any:
        result = self.fn(*args, **kwargs)

        if not self.predicate(result):
            raise ExecuteError

        return result


def repeat(
    repeater: Type[BaseRepeater],
    attempts: int = 3,
    sleep_interval: int = 1,
    **params,
) -> Callable:
    def decorate(fn: Callable[P, T]) -> Callable[P, T]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            return repeater(fn, attempts=attempts, sleep_interval=sleep_interval, **params)(
                *args, **kwargs
            )

        return wrapper

    return decorate
