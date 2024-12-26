from pathlib import Path
from aoc.util import read, file, bench, env

CURR_DAY: int = 22
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def task2(input: list[str]):
    pass


def next_number(num: int) -> int:
    # step 1
    num ^= num << 6
    num &= 16777215
    # step 2
    num ^= num >> 5
    num &= 16777215
    # step 3
    num ^= num << 11
    num &= 16777215
    return num


def task1(input: list[str]) -> int:
    numbers: list[int] = [int(s) for s in input]

    for _ in range(2000):
        for i, num in enumerate(numbers):
            numbers[i] = next_number(num)

    return sum(numbers)


@bench.timer
def day22() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    print("test1:", task1(test))
    print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day22()
