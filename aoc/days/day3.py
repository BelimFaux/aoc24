from pathlib import Path
from aoc.util import read, file, bench, env

CURR_DAY: int = 3
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def parse_num(input: str) -> tuple[int, int]:
    """try to parse a number of up to 3 digits at the start of input"""
    substr: str = ""
    for c in input:
        if c.isdigit():
            substr += c
        else:
            break
    if len(substr) == 0 or len(substr) > 3:
        return 0, -1  # error
    return len(substr), int(substr)


# using custom parser instead of regex
def both_tasks(input: str) -> tuple[int, int]:
    task1: int = 0
    task2: int = 0
    do: bool = True
    idx: int = 0
    while idx < len(input):
        if input[idx : idx + 4] == "mul(":  # parse mul(x,y) instr
            idx += 4
            num_len, num1 = parse_num(input[idx:])
            idx += num_len
            if input[idx] != "," or num1 == -1:
                continue
            idx += 1
            num_len, num2 = parse_num(input[idx:])
            idx += num_len
            if input[idx] != ")" or num1 == -1:
                continue
            task1 += num1 * num2
            if do:
                task2 += num1 * num2
        if input[idx : idx + 7] == "don't()":  # parse don't() instr
            do = False
            idx += 7
            continue
        elif input[idx : idx + 4] == "do()":  # parse do() instr
            do = True
            idx += 4
            continue

        idx += 1

    return task1, task2


def task2(input: str):
    return both_tasks(input)[1]


def task1(input: str) -> int:
    return both_tasks(input)[0]


@bench.timer
def day3() -> None:
    test: str = read.to_string(TEST_FILE_PATH)
    input: str = read.to_string(INPUT_FILE_PATH)

    print("test1:", task1(test))
    print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day3()
