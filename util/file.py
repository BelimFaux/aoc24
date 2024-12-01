import os.path
from urllib.request import Request, HTTPError, urlopen
from pathlib import Path
from . import env

YEAR: int = 2024
SESSION_TOKEN: str = env.get_env("SESSION_TOKEN")


def __root_dir() -> Path:
    """Get the absolute path of the root directory of the project (parent directory of this directory)"""
    return Path(os.path.abspath(__file__)).parents[1]


def __abs_path(day: int, test: bool = False) -> Path:
    """
    Get the absolute path of some input file.
    Will create an "input" dir if not already present.
    ----------
    Parameters
    day : int
        number of the day for the input file.
    test : bool (default = False)
        if the input file is a test file.
    """
    suffix: str = ".test" if test else ""
    filename: str = f"day{day}{suffix}.txt"
    filepath: Path = __root_dir()
    filepath = filepath / "input"
    filepath.mkdir(exist_ok=True)  # create input dir if it doesnt exist
    filepath /= filename

    return filepath


def download_puzzle_input(day: int):
    """
    Download the puzzle input for some day from the AoC Website.
    If the Input File already exists, the function returns early.
    If some Error occurs (like a wrong session key), an Error message with the Response Code is printed, and the Program exits.
    Be careful with this function, as to not overwhelm the AoC Websites server.
    ----------
    Parameters
    day : int
        The day for which the input should be retrieved.
    """
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
    """
    Get the absolute path to the input file for a specific day.
    Might download the file, if not already present.
    ----------
    Parameters
    day : int
        day for which to retrieve the path
    """
    filepath: Path = __abs_path(day)
    download_puzzle_input(day)

    return filepath


def test_path(day: int) -> Path:
    """
    Get the absolute path to the test file for a specific day.
    Might create an empty file, if not already present.
    ----------
    Parameters
    day : int
        day for which to retrieve the path
    """
    filepath: Path = __abs_path(day, True)

    if not filepath.exists():
        os.mknod(filepath)

    return filepath


def get_day(day: int) -> Path:
    """
    Get the absolute path to the Python file for a specific day.
    Doesn't check whether the file exists or not.
    ----------
    Parameters
    day : int
        day for which to retrieve the path
    """
    filename: str = f"day{day}.py"
    filepath: Path = __root_dir()
    filepath = filepath / "days" / filename
    return filepath


def get_all_days() -> list[Path]:
    """
    Get a list of absolute paths to the python files for all days that are currently present.
    """
    filepath: Path = __root_dir() / "days"
    return [p for p in filepath.glob("day*.py") if p.is_file()]


def create_new_day(day: int):
    """
    Create a template python file for the given day.
    The template is specified by a `template.py.txt` file in the root directory.
    If the file already exists, the function returns early.
    ----------
    Parameters
    day : int
        day for which to create the file
    """
    filepath: Path = get_day(day)
    if filepath.exists():
        return

    template: Path = __root_dir() / "template.py.txt"

    with open(template, "r") as f:
        contents: str = f.read()
    contents = contents.replace("{day}", str(day))

    with open(filepath, "w") as f:
        f.write(contents)
