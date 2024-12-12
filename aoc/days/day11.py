from pathlib import Path
from collections import Counter, defaultdict
from aoc.util import read, parse, file, bench, env

CURR_DAY: int = 11
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def split(nr: int) -> tuple[int, int]:
    return int(str(nr)[: len(str(nr)) // 2]), int(str(nr)[len(str(nr)) // 2 :])


# naive approach
def iterate(pebbles: list[int]) -> list[int]:
    new_pebbles: list[int] = []
    for stone in pebbles:
        if stone == 0:
            new_pebbles.append(1)
        elif len(str(stone)) % 2 == 0:
            st1, st2 = split(stone)
            new_pebbles.append(st1)
            new_pebbles.append(st2)
        else:
            new_pebbles.append(stone * 2024)
    return new_pebbles


# idea: save memory by reducing doubled numbers, that would evaluate to the same number
def dict_iterate(pebbles: dict[int, int]) -> dict[int, int]:
    new_pebbles: dict[int, int] = defaultdict(int)
    for stone, occ in pebbles.items():
        if stone == 0:
            new_pebbles[1] += occ
        elif len(str(stone)) % 2 == 0:
            st1, st2 = split(stone)
            new_pebbles[st1] += occ
            new_pebbles[st2] += occ
        else:
            new_pebbles[stone * 2024] += occ
    return new_pebbles


def task2(input: str) -> int:
    pebbles: dict[int, int] = Counter(parse.to_int_list(input, sep=" "))

    for _ in range(75):
        pebbles = dict_iterate(pebbles)

    return sum(pebbles.values())


def task1(input: str) -> int:
    pebbles: list[int] = parse.to_int_list(input, sep=" ")

    for _ in range(25):
        pebbles = iterate(pebbles)

    return len(pebbles)


@bench.timer
def day11() -> None:
    test: str = read.to_string(TEST_FILE_PATH)
    input: str = read.to_string(INPUT_FILE_PATH)

    print("test1:", task1(test))
    print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day11()
