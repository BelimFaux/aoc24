from pathlib import Path
from aoc.util import read, parse, file, bench, env

CURR_DAY: int = 2
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def is_safe(report: list[int]) -> bool:
    prev: int = -1
    increasing: bool = report[0] < report[1]
    for num in report:
        if prev != -1:
            if abs(num - prev) < 1 or abs(num - prev) > 3:
                return False
            if num < prev and increasing or num > prev and not increasing:
                return False
        prev = num

    return True


def task2(input: list[str]) -> int:
    reports: list[list[int]] = parse.inner_int_list(input)
    safe: int = 0
    for report in reports:
        if len(report) == 0:
            break
        if is_safe(report):
            safe += 1
        else:
            for index in range(len(report)):
                new_report = [v for i, v in enumerate(report) if i != index]
                if is_safe(new_report):
                    safe += 1
                    break
    return safe


def task1(input: list[str]) -> int:
    reports: list[list[int]] = parse.inner_int_list(input)
    safe: int = 0
    for report in reports:
        if len(report) == 0:
            break
        safe += 1 if is_safe(report) else 0
    return safe


@bench.timer
def day2() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    print("test1:", task1(test))
    print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day2()
