from dotenv import load_dotenv
import os


def get_env(name: str) -> str:
    load_dotenv()
    cont: str | None = os.environ.get(name)
    if cont is None:
        print(
            f"Couldn't retrieve Environment Variable '{name}'.\nPlease make sure this Variable exists."
        )
        exit(1)

    return cont
