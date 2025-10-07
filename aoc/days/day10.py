from pathlib import Path
from collections import deque
from aoc.util import read, file, bench, env
from aoc.util.point import in_range, point, add

CURR_DAY: int = 10
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


def find_trailheads(map: list[str]) -> list[point]:
    return [
        (li, col)
        for col in range(len(map[0]))
        for li in range(len(map))
        if map[li][col] == "0"
    ]


def get_all_connections(map: list[str], pos: point) -> list[point]:
    value: int = int(map[pos[0]][pos[1]])
    ret: list[point] = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        next: point = add(pos, (dx, dy))
        if in_range(next, range(len(map)), range(len(map[0]))):
            if map[next[0]][next[1]] == str(value + 1):
                ret.append(next)
    return ret


# bfs solution to finding all paths
def find_paths(map: list[str], start: point) -> list[list[point]]:
    all_paths: list[list[point]] = []
    q: deque = deque()

    path: list[point] = []
    path.append(start)
    q.append(path.copy())

    while q:
        path = q.popleft()
        last = path[-1]

        if map[last[0]][last[1]] == "9":
            all_paths.append(path)

        for conn in get_all_connections(map, last):
            if conn not in path:
                new_path: list[point] = path.copy()
                new_path.append(conn)
                q.append(new_path)

    return all_paths


def find_score(map: list[str], start: point) -> int:
    goals: set[point] = set()

    for path in find_paths(map, start):
        goals.add(path[-1])

    return len(goals)


def task2(input: list[str]) -> int:
    trailheads: list[point] = find_trailheads(input)
    return sum(len(find_paths(input, t)) for t in trailheads)


def task1(input: list[str]) -> int:
    trailheads: list[point] = find_trailheads(input)
    return sum(find_score(input, t) for t in trailheads)


# since both tasks use the same function, execution time can be halfed by combining both tasks
def both_tasks(input: list[str]) -> tuple[int, int]:
    trailheads: list[point] = find_trailheads(input)
    paths: list[list[list[point]]] = [find_paths(input, t) for t in trailheads]

    part1: int = sum(len({p[-1] for p in path}) for path in paths)
    part2: int = sum(len(path) for path in paths)
    return part1, part2


@bench.timer
def day10() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    if len(test):
        part1, part2 = both_tasks(test)
        print("test1:", task1(test))
        print("test2:", task2(test))

    if not ONLY_TESTS:
        part1, part2 = both_tasks(input)
        print("part1:", part1)
        print("part2:", part2)


if __name__ == "__main__":
    day10()
