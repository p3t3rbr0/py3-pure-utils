"""Utilities for repeatedly execute custom logic."""

from functools import wraps
from logging import Logger
from time import sleep
from typing import Any, Callable, Optional, ParamSpec, Type, TypeVar

T = TypeVar("T")
P = ParamSpec("P")
ExceptionT = Type[BaseException]


__all__ = [
    "ExceptionBasedRepeater",
    "PredicativeBasedRepeater",
    "repeat",
    "ExecuteError",
    "RepeateError",
]


class ExecuteError(Exception):
    """Raised when execute is failed."""

    pass


class RepeateError(Exception):
    """Raised after last execution attempt."""

    pass


class BaseRepeater:
    """Implements a base logic, such as constructor and execute method."""

    def __init__(self, *, attempts: int, interval: int, logger: Optional[Logger] = None) -> None:
        """Constructor.

        Args:
            fn: Callable object for execution.
            attempts: Maximum number of execution attempts
            interval: Time interval between attempts.
            logger: Logger object for detailed info about repeats.
        """
        self.attempts = attempts
        self.interval = interval
        self.logger = logger

    def __call__(self, fn: Callable, *args: P.args, **kwargs: P.kwargs) -> Any:
        """Callable interface for repeater object.

        Calls the object's execute method inside.
        After exhausting all available attempts, raises an RepeateError exception.

        Args:
            *args: Positional arguments to be passed to function being repeated.
            *kwargs: Named arguments to be passed to function being repeated.

        Returns:
            Result of executing a repeatable function.

        Raises:
            RepeateError: If all retry attempts have been exhausted.
        """
        for attempt in range(self.attempts):
            step = attempt + 1

            try:
                return self.execute(fn, *args, **kwargs)
            except ExecuteError as exc:
                self._log(f"'{fn.__name__}' failed! {self.attempts - step} attempts left.\n{exc}")
                sleep(step * self.interval)

        raise RepeateError(f"No success for '{fn.__name__}' after {self.attempts} attempts.")

    def execute(self, *args, **kwargs) -> Any:
        """Execute repeatable function.

        Needs to be implemented in inheritor classes.
        """
        raise NotImplementedError

    def _log(self, message: str) -> None:
        if self.logger:
            self.logger.warning(f"Repeater: {message}")


class ExceptionBasedRepeater(BaseRepeater):
    """Repeater based on catching targeted exceptions."""

    def __init__(
        self,
        *,
        attempts: int,
        interval: int,
        exceptions: tuple[ExceptionT, ...],
        logger: Optional[Logger] = None,
    ) -> None:
        """Constructor.

        Args:
            fn: Callable object for execution.
            attempts: Maximum number of execution attempts
            interval: Time interval between attempts.
            exceptions: Single or multiple (into tuple) targeted exceptions.
            logger: Logger object for detailed info about repeats.
        """
        super().__init__(attempts=attempts, interval=interval, logger=logger)
        self.exceptions = exceptions

    def execute(self, fn: Callable, *args: P.args, **kwargs: P.kwargs) -> Any:
        """Execute repeatable function.

        Args:
            *args: Positional arguments for repeatable function.
            *kwargs: Named arguments for repeatable function.

        Returns:
            Result of executing a repeatable function.

        Raises:
            ExecuteError: If one of the target exceptions was caught.
        """
        try:
            return fn(*args, **kwargs)
        except self.exceptions as exc:
            raise ExecuteError(str(exc))


class PredicativeBasedRepeater(BaseRepeater):
    """Repeater based on predicate function."""

    def __init__(
        self,
        *,
        attempts: int,
        interval: int,
        predicate: Callable[[Any], bool],
        logger: Optional[Logger] = None,
    ) -> None:
        """Constructor.

        Args:
            fn: Callable object for execution.
            attempts: Maximum number of execution attempts
            interval: Time interval between attempts.
            predicate: Predicate function.
            logger: Logger object for detailed info about repeats.
        """
        super().__init__(attempts=attempts, interval=interval, logger=logger)
        self.predicate = predicate

    def execute(self, fn: Callable, *args: P.args, **kwargs: P.kwargs) -> Any:
        """Execute repeatable function.

        Args:
            *args: Positional arguments for repeatable function.
            *kwargs: Named arguments for repeatable function.

        Returns:
            Result of executing a repeatable function.

        Raises:
            ExecuteError: If predicate function return a False.
        """
        result = fn(*args, **kwargs)

        if not self.predicate(result):
            raise ExecuteError

        return result


def repeat(repeater: BaseRepeater) -> Callable:
    """Decorator for repeat wrapped function by `repeater` logic.

    Args:
        repeater: Repeater object.
    """

    def decorate(fn: Callable[P, T]) -> Callable[P, T]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            return repeater(fn, *args, **kwargs)

        return wrapper

    return decorate
