"""Module for parsing input data to common structures."""


def two_int_cols(input: list[str]) -> tuple[list[int], list[int]]:
    """
    Parse a list of strings to two integer lists.
    The strings are expected to have the format `"d1 d2"` where d1 and d2 are valid integers.
    No checks are performed.
    ----------
    Parameters
    input : list[str]
        the input list containing string of the correct format
    -------
    Returns a tuple of two integer lists.
    """
    left: list[int] = []
    right: list[int] = []

    for line in input:
        if line.strip() == "":
            continue
        sp: list[str] = line.split(" ", 1)
        left.append(int(sp[0]))
        right.append(int(sp[1]))

    return (left, right)


def inner_int_list(input: list[str]) -> list[list[int]]:
    """
    Parse a list of strings to a list of lists of integers.
    No checks are performed.
    ----------
    Parameters
    input : list[str]
        the input list containing string of the correct format
    """
    return [[int(s) for s in line.split(" ") if s.strip() != ""] for line in input]


def to_tuples(input: list[str], sep: str) -> list[tuple[str, str]]:
    """
    Parse a list of strings to a list of tuples of two strings.
    No checks are performed.
    ----------
    Parameters
    input : list[str]
        the input list containing string of the correct format
    sep : str
        The string seperating the values
    """
    return [(elem.split(sep)[0], elem.split(sep)[1]) for elem in input]


def to_int_list(input: str, sep: str) -> list[int]:
    return [int(c) for c in input.split(sep)]
