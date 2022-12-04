# pyright: strict
import argparse
import sys
import os
import importlib
import re

from . import _aoc


if __name__ == "__main__":
    years = filter(
        re.compile(r"\d{4}", flags=re.ASCII).fullmatch,
        os.listdir(os.path.dirname(__file__)),
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("year", metavar="year", type=int, choices=[*map(int, years)])
    parser.add_argument("day", metavar="day", type=int, choices=[*range(1, 25 + 1)])
    parser.add_argument("part", metavar="part", type=int, choices=[1, 2])

    parser.add_argument(
        "-c",
        "--cache",
        type=str,
        help="path to downloaded (cached) AoC input files",
        required=True,
    )

    auto_group = parser.add_mutually_exclusive_group()
    auto_group.add_argument(
        "-f",
        "--fetch",
        dest="auto",
        action="store_const",
        const="fetch",
        help="run on official input fetched from AoC website",
    )
    auto_group.add_argument(
        "-F",
        "--fetch-and-submit",
        dest="auto",
        action="store_const",
        const="submit",
        help="run on official input fetched from AoC website & submit as final answer",
    )
    auto_group.add_argument(
        "-t",
        "--test",
        dest="auto",
        action="store_const",
        const="test",
        help="try to extract & test on sample input from problem statement",
    )

    args = parser.parse_args()
    try:
        mod = importlib.import_module(
            f".{args.year}.{args.day:02d}", package=__package__
        )
    except ModuleNotFoundError:
        print(
            f"{args.year} day {args.day} solution hasn't been implemented yet!",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        part = mod.part1 if args.part == 1 else mod.part2
    except AttributeError:
        print(
            f"{args.year} day {args.day} solution part {args.part} not yet implemented! "
            f"(hint: define a function named `part{args.part}`)"
        )
        sys.exit(2)

    if args.auto is None:
        print(part(sys.stdin))
    else:
        session = _aoc.get_session()
        client = _aoc.Client(session, args.cache)

        match args.auto:
            case "fetch" | "submit":
                with client.fetch_input(args.year, args.day) as f:
                    result = part(f)

                if not (isinstance(result, int) or isinstance(result, str)):
                    print(
                        f"{args.year} day {args.day} solution part {args.part} result is neither string nor integer:"
                        f"  {result!repr}"
                    )
                    sys.exit(3)

                print(result)

                if args.auto == "submit":
                    client.submit_answer(args.year, args.day, args.part, str(result))

            case "test":
                pass

            case _:
                pass
