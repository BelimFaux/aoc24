from pathlib import Path
from util import read, parse, file, timer

CURR_DAY: int = 1
INPUT_FILE_PATH: Path = file.abs_inp_path(CURR_DAY)


def task2(left: list[int], right: list[int]) -> int:
    sim_score: int = 0
    for num in left:
        count_in_right: int = right.count(num)
        sim_score += num * count_in_right
    return sim_score


def task1(left: list[int], right: list[int]) -> int:
    right = sorted(right)
    left = sorted(left)
    diff: list[int] = [abs(x - y) for x, y in zip(right, left)]
    return sum(diff)


@timer.timer
def main() -> None:
    # example_right: list[int] = [4, 3, 5, 3, 9, 3]
    # example_left: list[int] = [3, 4, 2, 1, 3, 3]
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)
    left, right = parse.two_int_cols(input)

    print("task1:", task1(left, right))
    print("task2:", task2(left, right))


if __name__ == "__main__":
    main()
