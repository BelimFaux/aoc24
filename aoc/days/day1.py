from pathlib import Path
from aoc.util import read, parse, file, bench, env

CURR_DAY: int = 1
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def task2(input: list[str]) -> int:
    left, right = parse.two_int_cols(input)
    sim_score: int = 0
    for num in left:
        count_in_right: int = right.count(num)
        sim_score += num * count_in_right
    return sim_score


def task1(input: list[str]) -> int:
    left, right = parse.two_int_cols(input)
    right = sorted(right)
    left = sorted(left)
    diff: list[int] = [abs(x - y) for x, y in zip(right, left)]
    return sum(diff)


@bench.timer
def day1() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    print("test1:", task1(test))
    print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day1()
