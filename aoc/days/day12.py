from pathlib import Path
from collections import defaultdict
from aoc.util import read, file, bench, env

CURR_DAY: int = 12
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


NEIGHBORS: list[tuple[int, int]] = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def get_neighbors(pos: tuple[int, int]) -> list[tuple[int, int]]:
    return [(d[0] + pos[0], d[1] + pos[1]) for d in NEIGHBORS]


def collect_regions(map: list[str]) -> dict[str, list[set[tuple[int, int]]]]:
    regions: dict[str, list[set[tuple[int, int]]]] = defaultdict(list)

    for li, line in enumerate(map):
        for col, c in enumerate(line):
            c_regions: list[set[tuple[int, int]]] = regions[c]

            # find all regions that contain neighbors of this cell
            fitting_reg: list[set[tuple[int, int]]] = [
                region
                for region in c_regions
                if any(n for n in get_neighbors((li, col)) if n in region)
            ]

            # if more than one region contains neighbors of this cell, then they get joined by this cell
            if len(fitting_reg) > 1:
                for fr in fitting_reg:
                    c_regions.remove(fr)
                region = set().union(*fitting_reg)
                region.add((li, col))
                c_regions.append(region)
                continue
            elif len(fitting_reg) == 1:
                fitting_reg[0].add((li, col))
                continue

            # if no region exists yet, a new one gets created
            c_regions.append({(li, col)})

    return regions


def calc_perimeter(region: set[tuple[int, int]]) -> int:
    corners: int = 0
    # count the number of corners for each position
    for pos in region:
        # get boolean for all directions that represents if there is a neighbor
        down, up, right, left, d_right, d_left, u_right, u_left = [
            True if (pos[0] + dx, pos[1] + dy) in region else False
            for (dx, dy) in NEIGHBORS + [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        ]

        # test for each corner (upper left, upper right, lower left, lower right)
        if not (up or left) or (up and left and not u_left):
            corners += 1
        if not (up or right) or (up and right and not u_right):
            corners += 1
        if not (down or left) or (down and left and not d_left):
            corners += 1
        if not (down or right) or (down and right and not d_right):
            corners += 1

    return corners


def task2(regions: dict[str, list[set[tuple[int, int]]]]) -> int:
    total_cost: int = 0
    for r in regions.values():
        for region in r:
            area: int = len(region)
            perimeter: int = calc_perimeter(region)
            total_cost += area * perimeter

    return total_cost


def task1(regions: dict[str, list[set[tuple[int, int]]]]) -> int:
    total_cost: int = 0
    for r in regions.values():
        for region in r:
            area: int = len(region)
            # perimeter is the sum of the number of neighbors that dont belong to the same region for every cell
            perimeter: int = sum(
                [len([n for n in get_neighbors(c) if n not in region]) for c in region]
            )
            total_cost += area * perimeter

    return total_cost


@bench.timer
def day12() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    regions = collect_regions(test)
    print("test1:", task1(regions))
    print("test2:", task2(regions))

    if not ONLY_TESTS:
        regions = collect_regions(input)
        print("task1:", task1(regions))
        print("task2:", task2(regions))


if __name__ == "__main__":
    day12()
