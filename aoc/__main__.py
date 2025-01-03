import argparse
from pathlib import Path
import runpy
from aoc.util import fetch, file, env, bench


def create_day(args: argparse.Namespace) -> None:
    """Handler for the `create` subcommand"""
    print(f"Creating Day {args.day}")
    file.create_new_day(args.day)


def run_day(args: argparse.Namespace) -> None:
    """Handler for the `run` subcommand"""
    name: Path = file.get_day(args.day)
    runpy.run_path(str(name), run_name="__main__")


def runall(args: argparse.Namespace) -> None:
    """Handler for the `runall` subcommand"""
    if args.plot:
        bench.TIME = True
        bench.PLOT = True

    for day in file.get_all_days():
        runpy.run_path(str(day), run_name="__main__")

    if args.plot:
        bench.bench()


def badge(args: argparse.Namespace) -> None:
    """Handler for the `update-badge` subcommand"""
    del args
    print("Warning: don't overuse this method, too limit requests to the AoC Website.")

    stars, completed_days = fetch.user_stats(env.get_env("AOC_USER_ID"))
    file.replace_badges(stars, completed_days)

    print(
        f"""Updated badges to:
    amount of stars: {stars},
    completed days: {completed_days}"""
    )


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "--test",
        action="store_true",
        help="run only test inputs (can also be set via the `TEST` environment variable)",
    )
    parser.add_argument(
        "--no-time",
        action="store_true",
        help="don't time the functions (can also be set via the `NO_TIME` environment variable)",
    )

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
    runall_parser.add_argument(
        "--plot",
        action="store_true",
        help="Plot a chart with the execution times of the days",
    )
    runall_parser.set_defaults(func=runall)

    badge_parser: argparse.ArgumentParser = subparsers.add_parser(
        "update-badge", help="Update badges in README.md file"
    )
    badge_parser.set_defaults(func=badge)

    args: argparse.Namespace = parser.parse_args()

    if args.test:
        env.set("TEST")
    if args.no_time:
        bench.TIME = False

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
