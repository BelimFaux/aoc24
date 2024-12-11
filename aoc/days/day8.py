from pathlib import Path
from itertools import product
from aoc.util import read, file, timer, env

CURR_DAY: int = 8
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def parse_freqs(input: list[str]) -> dict[str, list[tuple[int, int]]]:
    frequencies: dict[str, list[tuple[int, int]]] = {}
    for li in range(len(input)):
        for col in range(len(input[0])):
            if (freq := input[li][col]) != ".":
                frequencies[freq] = frequencies.get(freq, [])
                frequencies[freq].append((li, col))

    return frequencies


def add(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    return (p1[0] + p2[0], p1[1] + p2[1])


def sub(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    return (p1[0] - p2[0], p1[1] - p2[1])


def coord_in_range(coord: tuple[int, int], range_li: range, range_col: range) -> bool:
    return coord[0] in range_li and coord[1] in range_col


def task2(input: list[str]):
    frequencies: dict[str, list[tuple[int, int]]] = parse_freqs(input)
    range_li: range = range(0, len(input))
    range_col: range = range(0, len(input[0]))

    spots: set[tuple[int, int]] = set()
    for coords in frequencies.values():
        spots.update(coords)
        for pair in product(coords, repeat=2):
            if pair[0] == pair[1]:
                continue
            dist: tuple[int, int] = sub(pair[0], pair[1])
            left: tuple[int, int] = add(pair[0], dist)
            right: tuple[int, int] = add(pair[1], dist)

            # walk the line as long as the spots are in range
            while coord_in_range(left, range_li, range_col):
                spots.add(left)
                left = add(left, dist)
            while coord_in_range(right, range_li, range_col):
                spots.add(right)
                right = add(right, dist)

    return len(spots)


def task1(input: list[str]) -> int:
    frequencies: dict[str, list[tuple[int, int]]] = parse_freqs(input)
    range_li: range = range(0, len(input))
    range_col: range = range(0, len(input[0]))

    spots: set[tuple[int, int]] = set()
    for coords in frequencies.values():
        for pair in product(coords, repeat=2):
            if pair[0] == pair[1]:
                continue
            dist: tuple[int, int] = sub(pair[0], pair[1])
            left: tuple[int, int] = add(pair[0], dist)
            right: tuple[int, int] = add(pair[1], dist)
            if coord_in_range(left, range_li, range_col):
                spots.add(left)
            if coord_in_range(right, range_li, range_col):
                spots.add(right)

    return len(spots)


@timer.timer
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
