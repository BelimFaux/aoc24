from typing import TypeAlias

point: TypeAlias = tuple[int, int]


def add(p1: point, p2: point) -> point:
    return (p1[0] + p2[0], p1[1] + p2[1])


def sub(p1: point, p2: point) -> point:
    return (p1[0] - p2[0], p1[1] - p2[1])


def mul(p: point, scalar: int) -> point:
    return (p[0] * scalar, p[1] * scalar)


def in_range(p: point, range_li: range, range_col: range) -> bool:
    return p[0] in range_li and p[1] in range_col
