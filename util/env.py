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
