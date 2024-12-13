from pathlib import Path
from aoc.util import read, file, bench, env

CURR_DAY: int = 13
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


class Machine:

    def __init__(self) -> None:
        # uninizialized
        self.a: tuple[int, int] = (0, 0)
        self.b: tuple[int, int] = (0, 0)
        self.goal: tuple[int, int] = (0, 0)

    def push_a(self, times: int) -> tuple[int, int]:
        return (self.a[0] * times, self.a[1] * times)

    def push_b(self, times: int) -> tuple[int, int]:
        return (self.b[0] * times, self.b[1] * times)

    # cramers rule
    def solve(self) -> tuple[int, int] | None:
        det = self.a[0] * self.b[1] - self.a[1] * self.b[0]
        push_a = (self.goal[0] * self.b[1] - self.goal[1] * self.b[0]) // det
        push_b = (self.goal[1] * self.a[0] - self.goal[0] * self.a[1]) // det

        if (
            self.a[0] * push_a + self.b[0] * push_b,
            self.a[1] * push_a + self.b[1] * push_b,
        ) == self.goal:
            return (push_a, push_b)

        return None

    def __str__(self) -> str:
        return f"Button A: {self.a}, Button B: {self.b}, Goal: {self.goal}"


def tuple_add(lhs: tuple[int, int], rhs: tuple[int, int]) -> tuple[int, int]:
    return (lhs[0] + rhs[0], lhs[1] + lhs[1])


def parse_val(line: str) -> tuple[int, int]:
    x: int = int(line[line.find("X") + 2 : line.find(",")])
    y: int = int(line[line.find("Y") + 2 :])
    return (x, y)


def parse_machines(input: list[str]) -> list[Machine]:
    ret: list[Machine] = []

    m: Machine = Machine()
    for line in input:
        if line.strip() == "":
            ret.append(m)
            m = Machine()
            continue
        name, vals = line.split(":", 1)
        if "A" in name:
            m.a = parse_val(vals)
        elif "B" in name:
            m.b = parse_val(vals)
        else:
            m.goal = parse_val(vals)

    ret.append(m)

    return ret


CONVERSION_ERROR: int = 10000000000000


def task2(input: list[str]) -> int:
    machines: list[Machine] = parse_machines(input)

    tokens: int = 0
    for m in machines:
        m.goal = (m.goal[0] + CONVERSION_ERROR, m.goal[1] + CONVERSION_ERROR)
        ret = m.solve()
        if ret is not None:
            push_a, push_b = ret

            tokens += push_a * 3 + push_b

    return tokens


def task1(input: list[str]) -> int:
    machines: list[Machine] = parse_machines(input)

    tokens: int = 0
    for m in machines:
        ret = m.solve()
        if ret is not None:
            push_a, push_b = ret
            if push_a > 100 or push_b > 100:
                continue

            tokens += push_a * 3 + push_b

    return tokens


@bench.timer
def day13() -> None:
    test: list[str] = read.to_str_list(TEST_FILE_PATH)
    input: list[str] = read.to_str_list(INPUT_FILE_PATH)

    print("test1:", task1(test))
    print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day13()
