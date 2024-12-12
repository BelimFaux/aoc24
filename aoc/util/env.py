"""Module for handling environment variables."""

from dotenv import load_dotenv
import os

# load .env when module is imported
load_dotenv()


def get_env(name: str) -> str:
    """
    Get value of environment variable with `name`.
    If the variable doesn't exist, an error message is printed, and the program is exited.
    ----------
    Parameters
    name : str
        name of the variable to be retrieved.
    """
    cont: str | None = os.environ.get(name)
    if cont is None:
        print(
            f"Couldn't retrieve Environment Variable '{name}'.\nPlease make sure this Variable exists."
        )
        exit(1)

    return cont


def is_set(name: str) -> bool:
    """
    Test if an environment variable is set.
    ----------
    Parameters
    name : str
        name of the environment variable
    """
    return os.environ.get(name) is not None


def set(name: str) -> None:
    """
    sets an environment variable if it doesn't yet exist.
    ----------
    Parameters
    name : str
        name of the environment variable
    """
    if os.environ.get(name):
        return
    os.environ[name] = "1"


def unset(name: str) -> None:
    """
    unset an environment variable if it is set.
    ----------
    Parameters
    name : str
        name of the environment variable
    """
    if os.environ.get(name):
        del os.environ[name]
