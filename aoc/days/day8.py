from pathlib import Path
from itertools import product
from aoc.util import read, file, bench, env
from aoc.util.point import point, add, sub, in_range

CURR_DAY: int = 8
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def parse_freqs(input: list[str]) -> dict[str, list[point]]:
    frequencies: dict[str, list[point]] = {}
    for li in range(len(input)):
        for col in range(len(input[0])):
            if (freq := input[li][col]) != ".":
                frequencies[freq] = frequencies.get(freq, [])
                frequencies[freq].append((li, col))

    return frequencies


def task2(input: list[str]):
    frequencies: dict[str, list[point]] = parse_freqs(input)
    range_li: range = range(0, len(input))
    range_col: range = range(0, len(input[0]))

    spots: set[point] = set()
    for coords in frequencies.values():
        spots.update(coords)
        for pair in product(coords, repeat=2):
            if pair[0] == pair[1]:
                continue
            dist: point = sub(pair[0], pair[1])
            left: point = add(pair[0], dist)
            right: point = add(pair[1], dist)

            # walk the line as long as the spots are in range
            while in_range(left, range_li, range_col):
                spots.add(left)
                left = add(left, dist)
            while in_range(right, range_li, range_col):
                spots.add(right)
                right = add(right, dist)

    return len(spots)


def task1(input: list[str]) -> int:
    frequencies: dict[str, list[point]] = parse_freqs(input)
    range_li: range = range(0, len(input))
    range_col: range = range(0, len(input[0]))

    spots: set[point] = set()
    for coords in frequencies.values():
        for pair in product(coords, repeat=2):
            if pair[0] == pair[1]:
                continue
            dist: point = sub(pair[0], pair[1])
            left: point = add(pair[0], dist)
            right: point = add(pair[1], dist)
            if in_range(left, range_li, range_col):
                spots.add(left)
            if in_range(right, range_li, range_col):
                spots.add(right)

    return len(spots)


@bench.timer
def day8() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    print("test1:", task1(test))
    print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day8()
