import heapq
from pathlib import Path
from collections import defaultdict
from aoc.util import read, file, bench, env
from aoc.util.point import point, add, sub

CURR_DAY: int = 16
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")

DIR: list[point] = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def is_goal(map: list[str], pos: point) -> bool:
    return map[pos[0]][pos[1]] == "E"


class State:

    def __init__(self, pos: point, dir: int) -> None:
        self.pos = pos
        self.dir = dir

    def actions(self, map: list[str]) -> list[tuple]:
        actions: list[tuple[State, int]] = []
        if is_goal(map, self.pos):
            return actions

        next_pos: point = add(self.pos, DIR[self.dir])
        if map[next_pos[0]][next_pos[1]] != "#":
            actions.append((State(next_pos, self.dir), 1))

        left: point = add(self.pos, DIR[(self.dir + 1) % 4])
        if map[left[0]][left[1]] != "#":
            actions.append((State(self.pos, (self.dir + 1) % 4), 1000))
        right: point = add(self.pos, DIR[(self.dir - 1) % 4])
        if map[right[0]][right[1]] != "#":
            actions.append((State(self.pos, (self.dir - 1) % 4), 1000))

        return actions

    def __hash__(self) -> int:
        return hash(self.pos) + hash(self.dir)

    def __eq__(self, other, /) -> bool:
        if isinstance(other, State):
            return self.pos == other.pos and self.dir == other.dir
        return False

    # always false, so pq just uses the first tuple value
    def __lt__(self, _) -> bool:
        return False

    def __str__(self) -> str:
        return f"State {self.pos} / {self.dir}"


def all_dijkstra(input: list[str]) -> tuple[int, int]:
    start: State = State((len(input) - 2, 1), 0)
    d: dict[State, int] = {start: 0}
    paths: defaultdict[State, list[tuple[list[State], int]]] = defaultdict(
        list, {start: [([start], 0)]}
    )  # saves all paths to a node, as well as their length

    pq: list[tuple[int, State]] = [(0, start)]
    visited: set[State] = set()

    while pq:
        du, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        for n, cost in u.actions(input):
            dist: int = du + cost
            if n not in d or dist < d[n]:
                d[n] = dist
                paths[n] = [(path + [n], dist) for path, _ in paths[u]]
                heapq.heappush(pq, (d[n], n))
            elif dist == d[n]:  # if cost is equal, create a new path
                paths[n].extend([(p + [n], dist) for p, _ in paths[u]])

    m: int = min(c for n, c in d.items() if is_goal(input, n.pos))

    fields: set[point] = set()
    goals: list[State] = [State((1, len(input[0]) - 2), i) for i in range(4)]
    for goal in goals:
        for path, cost in paths[goal]:
            if cost != m:
                continue
            for s in path:
                fields.add(s.pos)

    return m, len(fields)


def task2(input: tuple[int, int]) -> int:
    return input[1]


def task1(result: tuple[int, int]) -> int:
    return result[0]


@bench.timer
def day16() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    res_test: tuple[int, int] = all_dijkstra(test)
    print("test1:", task1(res_test))
    print("test2:", task2(res_test))

    if not ONLY_TESTS:
        res_input: tuple[int, int] = all_dijkstra(input)
        print("task1:", task1(res_input))
        print("task2:", task2(res_input))


if __name__ == "__main__":
    day16()
