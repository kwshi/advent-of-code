# pyright: strict
import argparse
import sys
import os
import importlib
import re

years = ["2018"]


if __name__ == "__main__":

    re_year = re.compile(r"\d{4}", flags=re.ASCII)
    re_day = re.compile(r"(\d{2})\.py", flags=re.ASCII)
    here = os.path.dirname(__file__)
    years = filter(re_year.match, os.listdir(here))

    parser = argparse.ArgumentParser()
    parser.add_argument("year", metavar="year", type=int, choices=[*map(int, years)])
    parser.add_argument("day", metavar="day", type=int, choices=[*range(1, 25 + 1)])
    parser.add_argument("part", metavar="part", type=int, choices=[1, 2])

    args = parser.parse_args()
    try:
        mod = importlib.import_module(
            f".{args.year}.{args.day:02d}", package=__package__
        )
    except ModuleNotFoundError as e:
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

    result = part()
    if result is not None:
        print(result)
