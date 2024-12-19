from pathlib import Path
from aoc.util import read, file, bench, env

CURR_DAY: int = 19
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


# basic idea: store all ways the substring design[0:i] can be constructed in arrs[i]
def possible_arrs(design: str, patterns: list[str]) -> int:
    arrs: list[int] = [0] * (len(design) + 1)
    arrs[0] = 1

    for i in range(1, len(design) + 1):
        for p in patterns:
            if i >= len(p) and design[i - len(p) : i] == p:
                arrs[i] += arrs[i - len(p)]

    return arrs[len(design)]


def task2(input: str):
    first, second = input.split("\n\n", 1)

    patterns: list[str] = first.split(", ")
    designs: list[str] = second.splitlines()

    return sum([possible_arrs(d, patterns) for d in designs])


def possible(design: str, patterns: list[str]) -> bool:
    if design == "":
        return True
    for p in patterns:
        if design.startswith(p) and possible(design.removeprefix(p), patterns):
            return True
    return False


def task1(input: str) -> int:
    first, second = input.split("\n\n", 1)

    patterns: list[str] = first.split(", ")
    designs: list[str] = second.splitlines()

    return len([d for d in designs if possible(d, patterns)])


@bench.timer
def day19() -> None:
    test: str = read.to_string(TEST_FILE_PATH)
    input: str = read.to_string(INPUT_FILE_PATH)

    print("test1:", task1(test))
    print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day19()
