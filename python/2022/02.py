# pyright: strict
from .. import ks
import typing

to_num = {"A": 0, "B": 1, "C": 2, "X": 0, "Y": 1, "Z": 2}


def parse(stdin: typing.TextIO):
    for line in ks.parse.lines(stdin):
        yield map(to_num.__getitem__, line.split())


def outcome_points(diff: int):
    match diff % 3:
        case 0:
            return 3
        case 1:
            return 6
        case _:
            return 0


def part1(stdin: typing.TextIO):
    points = 0
    for opp, me in parse(stdin):
        points += outcome_points(me - opp) + me + 1
    return points


def part2(stdin: typing.TextIO):
    points = 0
    for opp, result in parse(stdin):
        me = (opp + result - 1) % 3
        points += outcome_points(result - 1) + me + 1
    return points
