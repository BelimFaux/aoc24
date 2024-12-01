from util import read

INPUT_FILE_PATH: str = "../input/day1.txt"


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


def main() -> None:
    # example_right: list[int] = [4, 3, 5, 3, 9, 3]
    # example_left: list[int] = [3, 4, 2, 1, 3, 3]
    left, right = read.two_int_cols(read.to_string(INPUT_FILE_PATH))

    print("task1:", task1(left, right))
    print("task2:", task2(left, right))


if __name__ == "__main__":
    main()
