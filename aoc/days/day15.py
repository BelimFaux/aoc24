from pathlib import Path
from aoc.util import read, file, bench, env
from aoc.util.point import point, add, sub

CURR_DAY: int = 15
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


MOVEMENTS: dict[str, point] = {
    "^": (-1, 0),
    "<": (0, -1),
    ">": (0, 1),
    "v": (1, 0),
}


def double(c: str) -> tuple[str, str]:
    match c:
        case "@":
            return ("@", ".")
        case "O":
            return ("[", "]")
        case _:
            return (c, c)


# add every field to be moved to the list, and returns if they are free to move
def move_box(
    field: list[list[str]],
    b: point,
    dir: point,
    to_move: list[point],
) -> bool:
    bli, bcol = b

    if field[bli][bcol] == "[":
        oli, ocol = (bli, bcol + 1)
    elif field[bli][bcol] == "]":
        oli, ocol = (bli, bcol - 1)
    elif field[bli][bcol] == ".":
        return True
    else:
        return False

    next = add(b, dir)
    if not move_box(field, next, dir, to_move):
        return False
    onext = add((oli, ocol), dir)
    if not move_box(field, onext, dir, to_move):
        return False

    to_move.append((bli, bcol))
    to_move.append((oli, ocol))

    return True


def task2(input: str) -> int:
    f, instr = input.split("\n\n", 1)
    field: list[list[str]] = []
    for x in f.splitlines():
        temp: list[str] = []
        for c in x:
            a, b = double(c)
            temp.append(a)
            temp.append(b)
        field.append(temp)

    robot: point = (0, 0)

    for li, line in enumerate(field):
        for col, c in enumerate(line):
            if c == "@":
                robot = (li, col)

    for i in instr:
        if i == "\n":
            continue
        dli, dcol = MOVEMENTS[i]
        nli, ncol = add((dli, dcol), robot)
        match field[nli][ncol]:
            case "#" | "@":
                continue
            case ".":
                field[robot[0]][robot[1]] = "."
                field[nli][ncol] = "@"
                robot = (nli, ncol)
            case "[" | "]":
                if i == "^" or i == "v":
                    to_move: list[point] = []
                    if not move_box(field, (nli, ncol), (dli, dcol), to_move):
                        continue

                    # deduplicate
                    seen = set()
                    to_move = [x for x in to_move if not (x in seen or seen.add(x))]
                    # swap every box with its neighbor below or above
                    for bli, bcol in to_move:
                        nbli, nbcol = add((bli, bcol), (dli, dcol))
                        field[bli][bcol], field[nbli][nbcol] = (
                            field[nbli][nbcol],
                            field[bli][bcol],
                        )

                else:
                    bli, bcol = (nli, ncol)
                    while field[bli][bcol] == "[" or field[bli][bcol] == "]":
                        bli, bcol = add((bli, bcol), (dli, dcol))

                    # if there is a wall, break
                    if field[bli][bcol] == "#":
                        continue

                    # move each box one to the right
                    while (bli, bcol) != (nli, ncol):
                        prevli, prevcol = sub((bli, bcol), (dli, dcol))
                        field[bli][bcol], field[prevli][prevcol] = (
                            field[prevli][prevcol],
                            field[bli][bcol],
                        )
                        bli, bcol = prevli, prevcol

                # move the robot one to the right
                field[robot[0]][robot[1]] = "."
                field[nli][ncol] = "@"
                robot = (nli, ncol)

    gps_sum: int = 0
    for li, line in enumerate(field):
        for col, c in enumerate(line):
            if c == "[":
                gps_sum += 100 * li + col

    return gps_sum


def task1(input: str) -> int:
    f, instr = input.split("\n\n", 1)
    field: list[list[str]] = [[c for c in line] for line in f.splitlines()]

    robot: point = (0, 0)

    for li, line in enumerate(field):
        if "@" in line:
            for col, c in enumerate(line):
                if c == "@":
                    robot = (li, col)

    for i in instr:
        if i == "\n":
            continue
        dli, dcol = MOVEMENTS[i]
        nli, ncol = add((dli, dcol), robot)
        match field[nli][ncol]:
            case "#" | "@":
                continue
            case ".":
                field[robot[0]][robot[1]] = "."
                field[nli][ncol] = "@"
                robot = (nli, ncol)
            case "O":
                bli, bcol = (nli, ncol)
                # find the furthest box
                while field[bli][bcol] == "O":
                    bli, bcol = add((bli, bcol), (dli, dcol))
                # if there is a wall, break
                if field[bli][bcol] == "#":
                    continue
                # move each box one to the right
                while (bli, bcol) != (nli, ncol):
                    prevli, prevcol = sub((bli, bcol), (dli, dcol))
                    field[bli][bcol], field[prevli][prevcol] = (
                        field[prevli][prevcol],
                        field[bli][bcol],
                    )
                    bli, bcol = prevli, prevcol
                # move the robot one to the right
                field[robot[0]][robot[1]] = "."
                field[nli][ncol] = "@"
                robot = (nli, ncol)

    gps_sum: int = 0
    for li, line in enumerate(field):
        for col, c in enumerate(line):
            if c == "O":
                gps_sum += 100 * li + col

    return gps_sum


@bench.timer
def day15() -> None:
    test: str = read.to_string(TEST_FILE_PATH)
    input: str = read.to_string(INPUT_FILE_PATH)

    if len(test):
        print("test1:", task1(test))
        print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day15()
