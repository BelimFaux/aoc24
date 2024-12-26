from pathlib import Path
from collections import defaultdict
from aoc.util import read, file, bench, env

CURR_DAY: int = 23
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def task2(input: list[str]) -> str:
    connec: defaultdict[str, list] = defaultdict(list)
    groups: list[set[str]] = []

    for line in input:
        left, right = line.split("-", 1)
        connec[left].append(right)
        connec[right].append(left)

        found: bool = False
        for g in groups:
            invalid: bool = False
            for com in g:
                if com == left or com == right:
                    continue
                if com not in connec[left] or com not in connec[right]:
                    invalid = True
                    break
            if not invalid:
                g.add(left)
                g.add(right)
                found = True
                break
        if not found:
            groups.append({left, right})

    biggest: set[str] = max(groups, key=len)
    return ",".join(sorted(biggest))


def task1(input: list[str]) -> int:
    connec: defaultdict[str, list] = defaultdict(list)
    groups: list[set[str]] = []

    for line in input:
        left, right = line.split("-", 1)
        connec[left].append(right)
        connec[right].append(left)
        for com in connec[left]:
            if com == right:
                continue
            if com in connec[right]:
                groups.append({com, left, right})

    return sum(any(com.startswith("t") for com in s) for s in groups)


@bench.timer
def day23() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    print("test1:", task1(test))
    print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day23()
