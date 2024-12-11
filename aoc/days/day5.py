from pathlib import Path
from functools import cmp_to_key
from aoc.util import read, parse, file, timer, env

CURR_DAY: int = 5
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


# what a return type
def parse_parts(input: list[str]) -> tuple[list[tuple[str, str]], list[list[str]]]:
    half: int = input.index("")
    rules: list[tuple[str, str]] = parse.to_tuples(input[:half], sep="|")
    updates: list[list[str]] = [x.split(",") for x in input[half + 1 :]]

    return rules, updates


def valid_line(line: list[str], rules: list[tuple[str, str]]) -> bool:
    return line == sorted(
        line, key=cmp_to_key(lambda x, y: -1 if (x, y) in rules else 1)
    )


def fix_line(line: list[str], rules: list[tuple[str, str]]) -> list[str]:
    return sorted(
        line, key=cmp_to_key(lambda item1, item2: -1 if (item1, item2) in rules else 1)
    )


def middle_val(input: list[str]) -> int:
    return int(input[len(input) // 2])


def task2(input: list[str]):
    rules, updates = parse_parts(input)
    # not the most efficient but it works...
    updates = [fix_line(u, rules) for u in updates if not valid_line(u, rules)]
    return sum(middle_val(u) for u in updates)


def task1(input: list[str]):
    rules, updates = parse_parts(input)
    updates = [u for u in updates if valid_line(u, rules)]
    return sum(middle_val(u) for u in updates)


@timer.timer
def day5() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    print("test1:", task1(test))
    print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day5()
