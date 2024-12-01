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
