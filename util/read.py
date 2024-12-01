from pathlib import Path


def to_string(path: Path) -> str:
    with open(path, "r") as f:
        i: str = f.read()
    return i


def to_str_list(path: Path) -> list[str]:
    return to_string(path).splitlines()
