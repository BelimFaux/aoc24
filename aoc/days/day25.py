from pathlib import Path
from itertools import groupby
from aoc.util import read, file, bench, env

CURR_DAY: int = 25
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def task2(input: list[str]):
    # not enough stars :(
    pass


def pin_height(scheme: list[str]) -> list[int]:
    heights: list[int] = [-1] * len(scheme[0])
    for s in scheme:
        for i in range(len(scheme[0])):
            heights[i] += s[i] == "#"
    return heights


def fits(key: list[int], lock: list[int]) -> bool:
    for i, k in enumerate(key):
        if k + lock[i] >= 6:
            return False
    return True


def task1(input: list[str]) -> int:
    # split list at empty strings
    schematics: list[list[str]] = [
        list(sub) for ele, sub in groupby(input, key=bool) if ele
    ]

    lock_scheme: list[list[str]] = []
    key_scheme: list[list[str]] = []

    for schema in schematics:
        if all(c == "." for c in schema[0]):
            key_scheme.append(schema)
        else:
            lock_scheme.append(schema)

    locks: list[list[int]] = [pin_height(lock) for lock in lock_scheme]
    keys: list[list[int]] = [pin_height(lock) for lock in key_scheme]

    return sum(sum(1 for lock in locks if fits(key, lock)) for key in keys)


@bench.timer
def day25() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    print("test1:", task1(test))
    print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day25()
