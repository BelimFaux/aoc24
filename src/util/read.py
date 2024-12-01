def to_string(path: str) -> str:
    with open(path, "r") as f:
        i: str = f.read()
    return i


def to_str_list(path: str) -> list[str]:
    return to_string(path).splitlines()
