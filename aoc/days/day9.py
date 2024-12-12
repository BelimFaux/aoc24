from pathlib import Path
from util import read, file, bench, env

CURR_DAY: int = 9
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def uncompress_blocks(compressed: str) -> list[int]:
    blocks: list[int] = []
    for idx, c in enumerate(compressed):
        if c == "\n":
            continue
        if idx % 2 == 0:
            for _ in range(int(c)):
                blocks.append(idx // 2)
        else:
            for _ in range(int(c)):
                blocks.append(-1)
    return blocks


def find_free(blocks: list[int], needed: int) -> int:
    start: int = 0
    size: int = 0
    empty: bool = False
    for idx, bl in enumerate(blocks):
        if bl == -1:
            if not empty:
                start = idx
                empty = True
            size += 1
            if size >= needed:
                return start
        else:
            size = 0
            empty = False

    return -1


def free_blocks(input: str) -> dict[int, int]:
    out: dict[int, int] = {}
    curr: int = 0
    for idx, c in enumerate(input):
        if c == "\n":
            continue
        if idx % 2 == 0:
            curr += int(c)
        else:
            for i in range(int(c)):
                out[curr] = int(c) - i
                curr += 1
    return out


def task2(input: str) -> int:
    blocks: list[int] = uncompress_blocks(input)
    free: dict[int, int] = free_blocks(input)  # keeps track of free blocks

    last: int = len(blocks) - 1
    while last > 0:
        if blocks[last] != -1:
            needed: int = 0
            ptr: int = last
            while blocks[last] == blocks[ptr]:
                needed += 1
                ptr -= 1
            # find the next free block
            start: int = next((idx for idx, sz in free.items() if sz >= needed), -1)
            if start == -1 or start > last:
                last -= needed
                continue
            for _ in range(needed):
                blocks[start], blocks[last] = blocks[last], blocks[start]
                del free[start]
                start += 1
                last -= 1
        else:
            last -= 1

    sum: int = 0
    for idx, bl in enumerate(blocks):
        if bl == -1:
            continue
        sum += idx * bl

    return sum


def task1(input: str) -> int:
    blocks: list[int] = uncompress_blocks(input)

    next: int = 0
    last: int = len(blocks) - 1
    sum: int = 0
    while next < last:
        if blocks[next] != -1:
            sum += next * blocks[next]
        else:
            if blocks[last] == -1:
                last -= 1
                continue

            sum += next * blocks[last]
            last -= 1
        next += 1
    if blocks[next] != -1:
        sum += next * blocks[next]

    return sum


@bench.timer
def day9() -> None:
    test: str = read.to_string(TEST_FILE_PATH)
    input: str = read.to_string(INPUT_FILE_PATH)

    print("test1:", task1(test))
    print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day9()
