import os.path
from pathlib import Path
from re import sub
from . import fetch

DAY_REGEX: str = r"(?<=https:\/\/img\.shields\.io\/badge\/day%20📅-)[0-9]+(?=-blue)"
STARS_REGEX: str = (
    r"(?<=https:\/\/img\.shields\.io\/badge\/stars%20⭐-)[0-9]+(?=-yellow)"
)
COMPLETED_REGEX: str = (
    r"(?<=https:\/\/img\.shields\.io\/badge\/days%20completed-)[0-9]+(?=-red)"
)


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


# A lot of this code is taken from `https://github.com/J0B10/aoc-badges-action/blob/master/aoc-badges.py`
def replace_badges(day: int, stars: int, completed_days: int) -> None:
    """
    Replaces the numbers in the badges in the README.md file with the given Arguments
    ----------
    Parameters
    day : int
        the current day
    stars : int
        the amount of stars the user has
    completed_days : int
        the amount of days that the user completed successfully
    """
    readme: Path = __root_dir() / "README.md"
    with open(readme, "r") as f:
        text: str = f.read()

    text = sub(DAY_REGEX, str(day), text)
    text = sub(STARS_REGEX, str(stars), text)
    text = sub(COMPLETED_REGEX, str(completed_days), text)

    with open(readme, "w") as f:
        f.write(text)


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
    fetch.puzzle_input(day, filepath)

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

    _ = test_path(day)  # make sure a test file is also created

    template: Path = __root_dir() / "template.py.txt"

    with open(template, "r") as f:
        contents: str = f.read()
    contents = contents.replace("{day}", str(day))

    with open(filepath, "w") as f:
        f.write(contents)
