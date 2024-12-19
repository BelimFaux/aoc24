from pathlib import Path
from PIL import Image
import numpy as np
from aoc.util import read, file, bench, env
from aoc.util.point import point, add

CURR_DAY: int = 14
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


class Robot:

    def __init__(self, pos: point, vel: point, bounds: point) -> None:
        self.ipos: point = pos
        self.pos: point = pos
        self.ivel: point = vel
        self.vel: point = vel
        self.bounds: tuple[int, int] = bounds

    def move(self, times: int) -> None:
        self.pos = (
            (self.pos[0] + times * self.vel[0]) % self.bounds[0],
            (self.pos[1] + times * self.vel[1]) % self.bounds[1],
        )

    def reset(self) -> None:
        self.pos = self.ipos
        self.vel = self.ivel

    def __str__(self) -> str:
        return f"Robot: pos: {self.pos}, vel: {self.vel}"


def parse_robots(input: list[str], size: tuple[int, int]) -> list[Robot]:
    ret: list[Robot] = []

    for line in input:
        p, v = line.split(" ", 1)
        p1, p2 = p.removeprefix("p=").split(",", 1)
        v1, v2 = v.removeprefix("v=").split(",", 1)
        r = Robot((int(p1), int(p2)), (int(v1), int(v2)), size)
        ret.append(r)

    return ret


def count_quadrants(robots: list[Robot], size: tuple[int, int]) -> int:
    top_half = range(0, size[1] // 2)
    left_half = range(0, size[0] // 2)

    def in_middle(pos):
        return pos[0] == size[0] // 2 or pos[1] == size[1] // 2

    top_left: int = 0
    top_right: int = 0
    bot_left: int = 0
    bot_right: int = 0
    for robot in robots:
        if in_middle(robot.pos):
            continue

        if robot.pos[0] in left_half:
            if robot.pos[1] in top_half:
                top_left += 1
            else:
                bot_left += 1
        else:
            if robot.pos[1] in top_half:
                top_right += 1
            else:
                bot_right += 1

    return top_left * top_right * bot_left * bot_right


def task2(input: list[str], size: tuple[int, int]):
    robots: list[Robot] = parse_robots(input, size)

    folder: Path = file.bench_image_path().parent / f"day14part2{size[0]}x{size[1]}"
    folder.mkdir(exist_ok=True)

    pixels = np.zeros([size[1], size[0], 3], dtype=np.uint8)
    for i in range(0, 100):
        for robot in robots:
            robot.move(i)
            col, li = robot.pos
            pixels[li, col] = [255, 255, 255]
            robot.reset()

        img = Image.fromarray(pixels)
        img.save(folder / f"{i}.bmp")
        pixels = np.zeros([size[1], size[0], 3], dtype=np.uint8)

    # inspecting the first 100 steps, you can see some artifacts, that repeat periodically with the image dimensions

    FIRST_HOR_ARTIFACT: int = 4  # the horizontal artifacts repeat every 103 seconds
    HOR_ARTIFACT_REPEAT: int = size[1]
    FIRST_VER_ARTIFACT: int = 29  # the vertical artifacts repeat every 101 seconds
    VER_ARTIFACT_REPEAT: int = size[0]

    # every second where horizontal and vertical artifacts meet should produce a christmas tree
    # so the answer is the first integer, that produces an integer for both (i-4) / 103 and (i-29) / 101
    # since the seconds have to be full integers

    first_meet: int = next(
        (
            i
            for i in range(10000)
            if ((i - FIRST_HOR_ARTIFACT) / HOR_ARTIFACT_REPEAT) % 1 == 0
            and ((i - FIRST_VER_ARTIFACT) / VER_ARTIFACT_REPEAT) % 1 == 0
        ),
        0,
    )

    # for manually checking
    for robot in robots:
        robot.move(first_meet)
        col, li = robot.pos
        pixels[li, col] = [255, 255, 255]
        robot.reset()

        img = Image.fromarray(pixels)
        img.save(folder / "christmastree.bmp")

    return first_meet


def task1(input: list[str], size: tuple[int, int]) -> int:
    robots: list[Robot] = parse_robots(input, size)
    for robot in robots:
        robot.move(100)
    return count_quadrants(robots, size)


TEST_SIZE: tuple[int, int] = (11, 7)
SIZE: tuple[int, int] = (101, 103)


@bench.timer
def day14() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    print("test1:", task1(test, TEST_SIZE))
    print("test2:", task2(test, TEST_SIZE))

    if not ONLY_TESTS:
        print("task1:", task1(input, SIZE))
        print("task2:", task2(input, SIZE))


if __name__ == "__main__":
    day14()
