from pathlib import Path
import itertools
from collections import deque, abc
from util import read, file, timer, env

CURR_DAY: int = 7
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def parse_line(input: str) -> tuple[int, list[int]]:
    l1, l2 = input.split(":", 1)
    return int(l1), [int(n) for n in l2.split(" ") if n != ""]


def calibration_results(nums: list[int], possible_ops: list[str]) -> abc.Iterator[int]:
    for ops in itertools.product(possible_ops, repeat=len(nums) - 1):
        queue: deque = deque(nums)
        for op in ops:
            first: int = queue.popleft()
            sec: int = queue.popleft()
            res: int = 0
            if op == "|":
                res = eval(f"{first}{sec}")
            else:
                res = eval(f"{first} {op} {sec}")
            queue.insert(0, res)
        yield queue[0]


def task2(input: list[str], prev_res: list[int]) -> int:
    total: int = 0
    for line in input:
        target, nums = parse_line(line)
        if len(prev_res) and prev_res[0] == target:
            prev_res.pop(0)
            total += target
            continue
        if target in calibration_results(nums, ["+", "*", "|"]):
            total += target
    return total


def task1(input: list[str]) -> list[int]:
    results: list[int] = []  # caching results for part 2
    for line in input:
        target, nums = parse_line(line)

        if target in calibration_results(nums, ["+", "*"]):
            results.append(target)
    return results


@timer.timer
def day7() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    res: list[int] = task1(test)
    print("test1:", sum(res))
    print("test2:", task2(test, res))

    if not ONLY_TESTS:
        res = task1(input)
        print("task1:", sum(res))
        print("task2:", task2(input, res))


if __name__ == "__main__":
    day7()
