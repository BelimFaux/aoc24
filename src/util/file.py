import os.path
from urllib.request import Request, HTTPError, urlopen
from pathlib import Path
import env

YEAR: int = 2024
SESSION_TOKEN: str = env.get_env("SESSION_TOKEN")


def __abs_path(day: int) -> Path:
    filename: str = f"day{day}.txt"
    filepath: Path = Path(os.path.abspath(__file__)).parents[2]
    filepath = filepath / "input" / filename

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


def abs_inp_path(day: int) -> Path:
    filepath: Path = __abs_path(day)
    download_puzzle_input(day)

    return filepath
