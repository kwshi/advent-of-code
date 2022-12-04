# pyright: strict

from .. import ks
import typing


def parse(stdin: typing.TextIO):
    return ks.parse.lines_pattern(stdin, "%u-%u,%u-%u")


def part1(stdin: typing.TextIO):
    return sum(a <= c <= d <= b or c <= a <= b <= d for a, b, c, d in parse(stdin))


def part2(stdin: typing.TextIO):
    return sum(a <= d and b >= c for a, b, c, d in parse(stdin))
