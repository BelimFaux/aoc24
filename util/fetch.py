from urllib.request import Request, HTTPError, urlopen
from pathlib import Path
import json
import pytz
from datetime import date, datetime
from . import env

YEAR: int = 2024
SESSION_TOKEN: str = env.get_env("SESSION_TOKEN")


def __get_response(url: str) -> str:
    """
    Sends a Request to some url and returns the response as plain text.
    If some Error occurs (like a wrong session key), an Error message with the Response Code is printed, and the Program exits.
    ----------
    Parameters
    url : str
        the complete url of the website
    """
    headers: dict[str, str] = {"Cookie": f"session={SESSION_TOKEN}"}
    request: Request = Request(url, headers=headers)

    try:
        with urlopen(request, timeout=2) as response:
            raw: str = response.read()
    except HTTPError as e:
        print(
            f"Error while trying to access url {url}.\nReceived: {e}\nPlease check if youre Session Token is valid or try to download manually."
        )
        exit(1)

    return raw


def puzzle_input(day: int, filepath: Path):
    """
    Download the puzzle input for some day from the AoC Website.
    If the Input File already exists, the function returns early.
    Be careful with this function, as to not overwhelm the AoC Websites server.
    ----------
    Parameters
    day : int
        The day for which the input should be retrieved.
    """
    # dont send unneccessary requests
    if filepath.exists():
        return

    url: str = f"https://adventofcode.com/{YEAR}/day/{day}/input"
    response = __get_response(url)
    with open(filepath, "w") as f:
        f.write(response)


# A lot of this code is taken from `https://github.com/J0B10/aoc-badges-action/blob/master/aoc-badges.py`
def user_stats(userid: str) -> tuple[int, int, int]:
    """
    Fetch the user stats from the AoC Website.
    Returned is a tuple of integers representing in following order the current day, total stars, and completed days
    ----------
    Parameters
    userid : str
        userid of the user for whom to fetch the stats
    -------
    Returns
    `[curr_day, total_stars, completed_days]`
    """
    url: str = f"https://adventofcode.com/{YEAR}/leaderboard/private/view/{userid}.json"
    response: str = __get_response(url)

    json_obj: dict = json.loads(response)
    user_dict: dict = json_obj["members"][userid]

    try:
        stars: int = user_dict["stars"]
        days_completed: int = sum(
            1
            for d in user_dict["completion_day_level"]
            if "2" in user_dict["completion_day_level"][d]
        )  # count the number of days that have both tasks completed

    except KeyError as e:
        print(f"Invalid Json response while trying to fetch user stats.\n{e}")
        exit(1)

    new_york_tz = pytz.timezone(
        "America/New_York"
    )  # AoC is published with UTC-5 (New York)

    day: int = 0
    today: date = datetime.now(new_york_tz).date()
    # clamp day to december of the current year
    if today < datetime(YEAR, 12, 1, tzinfo=new_york_tz).date():
        day = 0
    elif today > datetime(YEAR, 12, 31, tzinfo=new_york_tz).date():
        day = 24
    else:
        day = today.day

    return (day, stars, days_completed)
