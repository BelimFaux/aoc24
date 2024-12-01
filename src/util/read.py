def to_string(path: str) -> str:
    with open(path, "r") as f:
        i: str = f.read()
    return i


def two_int_cols(input: str) -> tuple[list[int], list[int]]:
    left: list[int] = []
    right: list[int] = []

    for line in input.splitlines():
        if line.strip() == "":
            continue
        sp: list[str] = line.split(" ", 1)
        left.append(int(sp[0]))
        right.append(int(sp[1]))

    return (left, right)
