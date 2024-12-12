from pathlib import Path
from aoc.util import read, file, bench, env

CURR_DAY: int = 4
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def task2(input: list[str]):
    total: int = 0

    for li in range(len(input) - 2):
        for idx in range(len(input[0]) - 2):
            string_rd: str = "".join(input[li + i][idx + i] for i in range(3))
            string_ru: str = string_rd[::-1]

            # if found, search for other
            if string_rd == "MAS" or string_ru == "MAS":
                left_li: int = li + 2
                left_idx: int = idx
                string_lu: str = "".join(
                    input[left_li - i][left_idx + i] for i in range(3)
                )
                string_ld: str = string_lu[::-1]

                if string_lu == "MAS" or string_ld == "MAS":
                    total += 1
    return total


def count_vert(input: list[str], idx: int) -> int:
    string: str = "".join([x[idx] for x in input])
    return string.count("XMAS")


def task1(input: list[str]):
    total: int = 0

    for line in input:
        total += line.count("XMAS")
        total += line[::-1].count("XMAS")

    for idx in range(len(input[0])):
        total += count_vert(input, idx)
        total += count_vert(input[::-1], idx)

    # construct diagonal strings for all directions
    for li in range(len(input) - 3):
        for idx in range(len(input[0]) - 3):
            string_rd: str = "".join([input[li + i][idx + i] for i in range(4)])
            string_ru: str = string_rd[::-1]
            total += string_ru.count("XMAS")
            total += string_rd.count("XMAS")

            left_idx: int = idx + 3
            string_lu: str = "".join([input[li + i][left_idx - i] for i in range(4)])
            string_ld: str = string_lu[::-1]
            total += string_lu.count("XMAS")
            total += string_ld.count("XMAS")

    return total


@bench.timer
def day4() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    print("test1:", task1(test))
    print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day4()
