def two_int_cols(input: list[str]) -> tuple[list[int], list[int]]:
    left: list[int] = []
    right: list[int] = []

    for line in input:
        if line.strip() == "":
            continue
        sp: list[str] = line.split(" ", 1)
        left.append(int(sp[0]))
        right.append(int(sp[1]))

    return (left, right)
