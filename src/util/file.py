import os.path
from pathlib import Path


def abs_inp_path(day: int) -> Path:
    filename: str = f"day{day}.txt"
    filepath: Path = Path(os.path.abspath(__file__)).parents[2]
    filepath = filepath / "input" / filename

    return filepath
