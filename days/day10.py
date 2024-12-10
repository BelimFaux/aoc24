from pathlib import Path
from collections import deque
from util import read, file, timer, env

CURR_DAY: int = 10
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def find_trailheads(map: list[str]) -> list[tuple[int, int]]:
    return [
        (li, col)
        for col in range(len(map[0]))
        for li in range(len(map))
        if map[li][col] == "0"
    ]


def get_all_connections(map: list[str], pos: tuple[int, int]) -> list[tuple[int, int]]:
    value: int = int(map[pos[0]][pos[1]])
    ret: list[tuple[int, int]] = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if pos[0] + dx in range(len(map)) and pos[1] + dy in range(len(map[0])):
            if map[pos[0] + dx][pos[1] + dy] == str(value + 1):
                ret.append((pos[0] + dx, pos[1] + dy))
    return ret


def not_visited(path: list[tuple[int, int]], pos: tuple[int, int]) -> bool:
    return pos not in path


# bfs solution to finding all paths
def find_paths(map: list[str], start: tuple[int, int]) -> list[list[tuple[int, int]]]:
    all_paths: list[list[tuple[int, int]]] = []
    q: deque = deque()

    path: list[tuple[int, int]] = []
    path.append(start)
    q.append(path.copy())

    while q:
        path = q.popleft()
        last = path[-1]

        if map[last[0]][last[1]] == "9":
            all_paths.append(path)

        for conn in get_all_connections(map, last):
            if not_visited(path, conn):
                new_path: list[tuple[int, int]] = path.copy()
                new_path.append(conn)
                q.append(new_path)

    return all_paths


def find_score(map: list[str], start: tuple[int, int]) -> int:
    goals: set[tuple[int, int]] = set()

    for path in find_paths(map, start):
        goals.add(path[-1])

    return len(goals)


def task2(input: list[str]) -> int:
    trailheads: list[tuple[int, int]] = find_trailheads(input)
    return sum(len(find_paths(input, t)) for t in trailheads)


def task1(input: list[str]) -> int:
    trailheads: list[tuple[int, int]] = find_trailheads(input)
    return sum(find_score(input, t) for t in trailheads)


@timer.timer
def day10() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    print("test1:", task1(test))
    print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day10()
