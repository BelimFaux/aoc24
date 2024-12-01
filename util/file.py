import os.path
from urllib.request import Request, HTTPError, urlopen
from pathlib import Path
from . import env

YEAR: int = 2024
SESSION_TOKEN: str = env.get_env("SESSION_TOKEN")


def __root_dir() -> Path:
    return Path(os.path.abspath(__file__)).parents[1]


def __abs_path(day: int, test: bool = False) -> Path:
    suffix: str = ".test" if test else ""
    filename: str = f"day{day}{suffix}.txt"
    filepath: Path = __root_dir()
    filepath = filepath / "input"
    filepath.mkdir(exist_ok=True)  # create input dir if it doesnt exist
    filepath /= filename

    return filepath


def download_puzzle_input(day: int):
    filepath: Path = __abs_path(day)

    # dont send unneccessary requests
    if filepath.exists():
        return

    url: str = f"https://adventofcode.com/{YEAR}/day/{day}/input"
    headers: dict[str, str] = {"Cookie": f"session={SESSION_TOKEN}"}
    request: Request = Request(url, headers=headers)

    try:
        with urlopen(request, timeout=2) as response:
            with open(filepath, "wb") as f:
                f.write(response.read())
    except HTTPError as e:
        print(
            f"Error while trying to download Input file for Day {day}.\nReceived: {e}\nPlease Download Input manually from '{url}', and place in {filepath}."
        )
        exit(1)


def input_path(day: int) -> Path:
    filepath: Path = __abs_path(day)
    download_puzzle_input(day)

    return filepath


def test_path(day: int) -> Path:
    filepath: Path = __abs_path(day, True)

    if not filepath.exists():
        os.mknod(filepath)

    return filepath


def get_day(day: int) -> Path:
    filename: str = f"day{day}.py"
    filepath: Path = __root_dir()
    filepath = filepath / "days" / filename
    return filepath


def get_all_days() -> list[Path]:
    filepath: Path = __root_dir() / "days"
    return [p for p in filepath.glob("day*.py") if p.is_file()]


def create_new_day(day: int):
    filepath: Path = get_day(day)
    template: Path = __root_dir() / "template.py.txt"

    with open(template, "r") as f:
        contents: str = f.read()
    contents = contents.replace("{day}", str(day))

    with open(filepath, "w") as f:
        f.write(contents)
