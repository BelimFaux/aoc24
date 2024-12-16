from pathlib import Path
from collections import deque
from aoc.util import read, file, bench, env

CURR_DAY: int = 16
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")

DIR: list[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def is_goal(map: list[str], pos: tuple[int, int]) -> bool:
    return map[pos[0]][pos[1]] == "E"


def tuple_add(lhs: tuple[int, int], rhs: tuple[int, int]) -> tuple[int, int]:
    return (lhs[0] + rhs[0], lhs[1] + rhs[1])


class State:

    def __init__(self, pos: tuple[int, int], dir: int) -> None:
        self.pos = pos
        self.dir = dir

    def actions(self, map: list[str]) -> list[tuple]:
        actions: list[tuple[State, int]] = []

        next_pos: tuple[int, int] = tuple_add(self.pos, DIR[self.dir])
        if map[next_pos[0]][next_pos[1]] != "#":
            actions.append((State(next_pos, self.dir), 1))

        actions.append((State(self.pos, (self.dir + 1) % 4), 1000))
        actions.append((State(self.pos, (self.dir - 1) % 4), 1000))

        return actions

    def __hash__(self) -> int:
        return hash(self.pos) + hash(self.dir)

    def __eq__(self, value, /) -> bool:
        return self.pos == value.pos and self.dir == value.dir


def bfs(input: list[str]):
    start = State((len(input) - 2, 1), 0)
    parent = {start: None}
    d = {start: 0}

    q: deque = deque()
    q.append(start)
    in_queue = {start}

    while q:
        u = q.popleft()
        in_queue.remove(u)

        for n, cost in u.actions(input):
            if n not in d or d[n] > d[u] + cost:
                d[n] = d[u] + cost
                parent[n] = u

                if n not in in_queue:
                    q.append(n)
                    in_queue.add(n)

    cost = min(c for n, c in d.items() if is_goal(input, n.pos))

    return cost, 0


def task2(input: tuple[int, int]) -> int:
    return input[1]


def task1(result: tuple[int, int]) -> int:
    return result[0]


@bench.timer
def day16() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    res_test = bfs(test)
    print("test1:", task1(res_test))
    print("test2:", task2(res_test))

    if not ONLY_TESTS:
        res_input = bfs(input)
        print("task1:", task1(res_input))
        print("task2:", task2(res_input))


if __name__ == "__main__":
    day16()
