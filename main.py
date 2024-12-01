import argparse
from pathlib import Path
import runpy
from util import file


def create_day(args: argparse.Namespace) -> None:
    print(f"Create Day {args.day}")
    file.create_new_day(args.day)


def run_day(args: argparse.Namespace) -> None:
    name: Path = file.get_day(args.day)
    runpy.run_path(str(name), run_name="__main__")


def runall(args: argparse.Namespace) -> None:
    del args
    for day in file.get_all_days():
        runpy.run_path(str(day), run_name="__main__")


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Commands")

    create_parser: argparse.ArgumentParser = subparsers.add_parser(
        "create", help="Create new Day"
    )
    create_parser.add_argument(
        "day", type=int, help="Number of the Day that should be created"
    )
    create_parser.set_defaults(func=create_day)

    run_parser: argparse.ArgumentParser = subparsers.add_parser(
        "run", help="Run only a certain Day"
    )
    run_parser.add_argument(
        "day", type=int, help="Number of the Day that should be run"
    )
    run_parser.set_defaults(func=run_day)

    runall_parser: argparse.ArgumentParser = subparsers.add_parser(
        "runall", help="Run all available Days"
    )
    runall_parser.set_defaults(func=runall)

    args: argparse.Namespace = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
