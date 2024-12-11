from collections.abc import Callable
import time
from typing import ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")
TIME: bool = True
BENCHMARK: bool = False

__EXEC_TIMES: dict[str, float] = {}


def bench() -> None:
    import matplotlib.pyplot as plt
    from . import file

    global __EXEC_TIMES
    max: float = sum(__EXEC_TIMES.values())
    __EXEC_TIMES = dict(
        sorted(__EXEC_TIMES.items(), key=lambda item: item[1], reverse=True)
    )  # sort so the longest times are on top

    days = [
        f"{name} ({time / max * 100:.3}%)" for name, time in __EXEC_TIMES.items()
    ]  # calulate percentages for each day

    times = list(__EXEC_TIMES.values())

    ret = plt.pie(times, startangle=90)
    plt.legend(ret[0], days, loc="upper left")
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig(file.bench_image_path())


def get_exec_times() -> dict[str, float] | None:
    """
    Get the recorded execution times, if they exist.
    """
    if BENCHMARK:
        return __EXEC_TIMES
    return None


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

        if BENCHMARK:
            __EXEC_TIMES[func.__name__] = after - before

        print("-" * times)
        print(f"{func.__name__} took {(after - before):.3} seconds.")
        return ret

    return timer_function if TIME else no_timer_function
