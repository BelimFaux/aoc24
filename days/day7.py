from pathlib import Path
from util import read, file, timer, env

CURR_DAY: int = 7
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def parse_line(input: str) -> tuple[int, list[int]]:
    l1, l2 = input.split(":", 1)
    return int(l1), [int(n) for n in l2.split(" ") if n != ""]


# solution inspired by https://github.com/maneatingape/advent-of-code-rust/blob/main/src/year2024/day07.rs
# i adopted this solution, because mine takes ~5 min to terminate...
def is_valid(nums: list[int], target: int, index: int, concat: bool) -> bool:
    # basecase: if the list only has one number left it has to be equal to the target num
    if index == 0:
        return target == nums[0]

    if concat:
        # if the target can be concatennated by the last number,
        # the numbers are valid, if the target without the last number as suffix can be constructed by the rest of the numbers
        if str(target).endswith(str(nums[index])) and is_valid(
            nums,
            int(str(target).removesuffix(str(nums[index])) or "0"),
            index - 1,
            concat,
        ):
            return True

    # if the target is divisible by the last number,
    # the numbers are valid if the target divided by the last number can be constructed by the rest of the numbers
    if target % nums[index] == 0 and is_valid(
        nums, target // nums[index], index - 1, concat
    ):
        return True

    # if the target is bigger or equal to the last number,
    # the numbers are valid if the target minus the last number can be constructed by the rest of the numbers
    if target >= nums[index] and is_valid(
        nums, target - nums[index], index - 1, concat
    ):
        return True

    return False


def task2(input: list[str], prev_res: list[int]) -> int:
    total: int = 0
    for line in input:
        target, nums = parse_line(line)
        if len(prev_res) and prev_res[0] == target:
            prev_res.pop(0)
            total += target
            continue
        if is_valid(nums, target, len(nums) - 1, True):
            total += target
    return total


def task1(input: list[str]) -> list[int]:
    results: list[int] = []  # caching results for part 2
    for line in input:
        target, nums = parse_line(line)

        if is_valid(nums, target, len(nums) - 1, False):
            results.append(target)
    return results


@timer.timer
def day7() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    res: list[int] = task1(test)
    print("test1:", sum(res))
    print("test2:", task2(test, res))

    if not ONLY_TESTS:
        res = task1(input)
        print("task1:", sum(res))
        print("task2:", task2(input, res))


if __name__ == "__main__":
    day7()
