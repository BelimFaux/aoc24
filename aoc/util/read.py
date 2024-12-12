"""Module for reading input data to a specified format"""

from pathlib import Path


def to_string(path: Path) -> str:
    """
    Read the content of a file into a string.
    ---------
    Parameter
    path : Path
        path to the input file
    """
    with open(path, "r") as f:
        i: str = f.read()
    return i


def to_str_list(path: Path) -> list[str]:
    """
    Read the content of a file into a list of strings, representing the lines from the original file.
    ---------
    Parameter
    path : Path
        path to the input file
    """
    return to_string(path).splitlines()
