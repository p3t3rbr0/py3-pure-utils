from datetime import datetime, timedelta
from functools import lru_cache, wraps
from typing import Any, Callable, ParamSpec


P = ParamSpec("P")


def timed_lru_cache(seconds: int, maxsize: int = 1024) -> Callable[[Callable], Callable]:
    """..."""

    def wrapper_cache(func: Callable):
        func = lru_cache(maxsize=maxsize)(func)
        func._lifetime = timedelta(seconds=seconds)  # type: ignore[attr-defined]
        func._expiration = datetime.utcnow() + func._lifetime  # type: ignore[attr-defined]

        @wraps(func)
        def wrapped_func(*args: P.args, **kwargs: P.kwargs) -> Any:
            """..."""
            if datetime.utcnow() >= func._expiration:  # type: ignore[attr-defined]
                func.cache_clear()  # type: ignore[attr-defined]
                func._expiration = (  # type: ignore[attr-defined]
                    datetime.utcnow() + func._lifetime  # type: ignore[attr-defined]
                )
            return func(*args, **kwargs)  # type: ignore[misc]

        return wrapped_func

    return wrapper_cache
