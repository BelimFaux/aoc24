from collections import defaultdict
from pathlib import Path
import heapq
from aoc.util import read, parse, file, bench, env
from aoc.util.point import in_range, point, add

CURR_DAY: int = 18
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


MOVEMENTS: list[point] = [(-1, 0), (1, 0), (0, 1), (0, -1)]


def dijkstra(fallen: set[point], end: point) -> list[point]:
    start: point = (0, 0)
    pq: list = [(0, start)]
    d: dict[point, int] = {start: 0}
    path: defaultdict[point, list[point]] = defaultdict(list, {start: [start]})
    visited: set[point] = set()

    while pq:
        dist, elem = heapq.heappop(pq)
        if elem == end:
            return path[elem]

        if elem in visited:
            continue
        visited.add(elem)

        for new_elem in [add(elem, d) for d in MOVEMENTS]:
            if new_elem in fallen or not in_range(
                new_elem, range(end[0] + 1), range(end[1] + 1)
            ):
                continue

            new_dist = dist + 1
            if new_elem not in d or new_dist < d[new_elem]:
                d[new_elem] = new_dist
                path[new_elem] = path[elem] + [new_elem]
                heapq.heappush(pq, (d[new_elem], new_elem))

    return []


def task2(input: list[str], vals: tuple[int, int]) -> point:
    dim, iter = vals
    byte: list[point] = [(int(x), int(y)) for (x, y) in parse.to_tuples(input, sep=",")]
    fallen_bytes: set[point] = {b for b in byte[:iter]}
    path: set = set(dijkstra(fallen_bytes, (dim, dim)))

    while iter < len(byte):
        iter += 1
        if byte[iter - 1] in path:
            fallen_bytes |= {b for b in byte[len(fallen_bytes) - 1 : iter]}
            path = set(dijkstra(fallen_bytes, (dim, dim)))
            if path == set():
                return byte[iter - 1]

    return 0, 0


def task1(input: list[str], vals: tuple[int, int]) -> int:
    dim, iter = vals
    byte: list[point] = [(int(x), int(y)) for (x, y) in parse.to_tuples(input, sep=",")]
    fallen_bytes: set[point] = {b for b in byte[:iter]}

    return len(dijkstra(fallen_bytes, (dim, dim))) - 1


TEST_VALS: tuple[int, int] = (6, 12)
INPUT_VALS: tuple[int, int] = (70, 1024)


@bench.timer
def day18() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    print("test1:", task1(test, TEST_VALS))
    print("test2:", task2(test, TEST_VALS))

    if not ONLY_TESTS:
        print("task1:", task1(input, INPUT_VALS))
        print("task2:", task2(input, INPUT_VALS))


if __name__ == "__main__":
    day18()
