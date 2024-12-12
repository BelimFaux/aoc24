from pathlib import Path
from aoc.util import read, file, bench, env

CURR_DAY: int = 6
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")

DIRECTIONS: list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def start_pos(input: list[str]) -> tuple[int, int]:
    for i, line in enumerate(input):
        for j, column in enumerate(line):
            if column == "^":
                return i, j

    raise ValueError("NO START FOUND")


def visit(input: list[str]) -> dict | None:
    s_li, s_col = start_pos(input)
    dir: int = 0

    visited: dict = {(s_li, s_col): dir}
    curr_li: int = s_li
    curr_col: int = s_col
    while True:
        d_li, d_col = DIRECTIONS[dir]

        # check if in bounds
        if not (
            0 <= curr_li + d_li < len(input) and 0 <= curr_col + d_col < len(input[0])
        ):
            break

        if input[curr_li + d_li][curr_col + d_col] == "#":
            dir = (dir + 1) % 4
            continue

        curr_li += d_li
        curr_col += d_col

        if (curr_li, curr_col) in visited:
            if dir == visited[(curr_li, curr_col)]:
                return None
        visited[(curr_li, curr_col)] = dir

    return visited


def task2(input: list[str]) -> int:
    copy: list[str] = input.copy()
    visited: dict = visit(copy) or {}

    counter: int = 0
    for li, col in visited.keys():
        field: list[str] = input.copy()
        if field[li][col] == "^":
            continue
        field[li] = field[li][:col] + "#" + field[li][col + 1 :]
        if not visit(field):
            counter += 1

    return counter


def task1(input: list[str]) -> int:
    return len(visit(input) or {})


@bench.timer
def day6() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    print("test1:", task1(test.copy()))
    print("test2:", task2(test.copy()))

    if not ONLY_TESTS:
        print("task1:", task1(input.copy()))
        print("task2:", task2(input.copy()))


if __name__ == "__main__":
    day6()
