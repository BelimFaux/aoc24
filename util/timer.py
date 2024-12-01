from collections.abc import Callable
import time
from typing import ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


def timer(func: Callable[P, T]) -> Callable[P, T]:
    """
    Decorator for timing a function.
    """

    def timer_function(*args, **kwargs) -> T:
        print(f"{f'Running {func.__name__}':-^40}")
        before: float = time.time()

        ret: T = func(*args, **kwargs)

        after: float = time.time()
        print(f"Function {func.__name__} took {(after - before):.3} seconds.")
        print("-" * 40)
        return ret

    return timer_function
