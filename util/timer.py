from collections.abc import Callable
import time
from typing import ParamSpec, TypeVar
from util import env

T = TypeVar("T")
P = ParamSpec("P")
TIME: bool = not env.is_set("NO_TIME")


def timer(func: Callable[P, T]) -> Callable[P, T]:
    """
    Decorator for timing a function.
    """
    times: int = 30

    def no_timer_function(*args, **kwargs) -> T:
        print(f"{f'Running {func.__name__}':-^{times}}")
        ret: T = func(*args, **kwargs)
        print("-" * times)
        return ret

    def timer_function(*args, **kwargs) -> T:
        print(f"{f'Running {func.__name__}':-^{times}}")
        before: float = time.time()

        ret: T = func(*args, **kwargs)

        after: float = time.time()
        print("-" * times)
        print(f"{func.__name__} took {(after - before):.3} seconds.")
        return ret

    return timer_function if TIME else no_timer_function
