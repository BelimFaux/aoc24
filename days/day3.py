from pathlib import Path
from util import read, file, timer, env

CURR_DAY: int = 3
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def parse_num(input: str) -> tuple[int, int]:
    substr: str = ""
    for c in input:
        if c.isdigit():
            substr += c
        else:
            break
    if len(substr) == 0 or len(substr) > 3:
        return 0, -1
    return len(substr), int(substr)


def task2(input: str):
    result: int = 0
    do: bool = True
    idx: int = 0
    while idx < len(input):
        if do and input[idx] == "m":
            if input[idx : idx + 4] == "mul(":
                idx += 4
                ln, num1 = parse_num(input[idx:])
                idx += ln
                if input[idx] != "," or num1 == -1:
                    continue
                idx += 1
                ln, num2 = parse_num(input[idx:])
                idx += ln
                if input[idx] != ")" or num1 == -1:
                    continue
                result += num1 * num2
        if input[idx] == "d":
            if input[idx : idx + 7] == "don't()":
                do = False
                idx += 7
                continue
            elif input[idx : idx + 4] == "do()":
                do = True
                idx += 4
                continue

        idx += 1

    return result


def task1(input: str) -> int:
    result: int = 0
    idx: int = 0
    while idx < len(input):
        if input[idx] == "m":
            if input[idx : idx + 4] == "mul(":
                idx += 4
                ln, num1 = parse_num(input[idx:])
                idx += ln
                if input[idx] != "," or num1 == -1:
                    continue
                idx += 1
                ln, num2 = parse_num(input[idx:])
                idx += ln
                if input[idx] != ")" or num1 == -1:
                    continue
                result += num1 * num2
        idx += 1

    return result


@timer.timer
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
