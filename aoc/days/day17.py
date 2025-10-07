from pathlib import Path
from aoc.util import read, file, bench, env

CURR_DAY: int = 17
INPUT_FILE_PATH: Path = file.input_path(CURR_DAY)
TEST_FILE_PATH: Path = file.test_path(CURR_DAY)
ONLY_TESTS: bool = env.is_set("TEST")


class OpCode:
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


class VM:

    def __init__(self, reg_a: int, reg_b: int, reg_c: int) -> None:
        self.a: int = reg_a
        self.b: int = reg_b
        self.c: int = reg_c
        self.out: list[int] = []

    def run(self, prg: list[int]) -> list[int]:
        self.out = []
        ip: int = 0

        while ip < len(prg) - 1:
            op_code = prg[ip]
            operand = prg[ip + 1]
            match op_code:
                case OpCode.ADV:
                    self.a >>= self.combo(operand)
                case OpCode.BXL:
                    self.b ^= operand
                case OpCode.BST:
                    self.b = self.combo(operand) & 7
                case OpCode.JNZ:
                    if self.a != 0:
                        ip = operand
                        continue
                case OpCode.BXC:
                    self.b ^= self.c
                case OpCode.OUT:
                    val = self.combo(operand) & 7
                    self.out.append(val)
                case OpCode.BDV:
                    self.b = self.a >> self.combo(operand)
                case OpCode.CDV:
                    self.c = self.a >> self.combo(operand)
            ip += 2

        return self.out

    def combo(self, literal: int) -> int:
        if literal < 0 or literal > 6:
            raise ValueError(f"INVALID LITERAL: {literal}")

        if literal <= 3:
            return literal
        elif literal == 4:
            return self.a
        elif literal == 5:
            return self.b
        else:
            return self.c


def parse_vm(input: str) -> tuple[VM, list[int]]:
    regs, prg = input.split("\n\n", 1)
    a: int = int(regs.splitlines()[0].split(": ", 1)[1])
    b: int = int(regs.splitlines()[1].split(": ", 1)[1])
    c: int = int(regs.splitlines()[2].split(": ", 1)[1])

    program: list[int] = [int(c) for c in prg.split(": ", 1)[1].split(",")]
    vm: VM = VM(a, b, c)
    return vm, program


def find_val(program):
    starts = [0]  # starting values that produce the desired sequence up to this point

    for out in reversed(program):
        next = []

        # loop through every value that could be the solution for this subsequence-1
        for s in starts:

            # by doing the division, 3 bits are lost,
            # so test every possible value (2^3=3) to check if it produces the right value
            for n in range(8):
                # reverse the statement and append the number to test
                a = (s << 3) | n
                vm = VM(a, 0, 0)
                ret = vm.run(program)
                # check if the first digit matches (rest should match because of the previous iterations)
                if out == ret[0]:
                    next.append(a)

        starts = next

    return min(starts)


def task2(input: str):
    _, program = parse_vm(input)
    a = find_val(program)
    return a


def task1(input: str) -> str:
    vm, program = parse_vm(input)
    return ",".join([str(x) for x in vm.run(program)])


@bench.timer
def day17() -> None:
    test: str = read.to_string(TEST_FILE_PATH)
    input: str = read.to_string(INPUT_FILE_PATH)

    if len(test):
        print("test1:", task1(test))
        print("test2:", task2(test))

    if not ONLY_TESTS:
        print("task1:", task1(input))
        print("task2:", task2(input))


if __name__ == "__main__":
    day17()
