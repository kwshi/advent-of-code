# pyright: strict

from .. import ks
import typing

import re

re_line = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")


def parse(stdin: typing.TextIO):
    for line in ks.parse.lines(stdin):
        m = re_line.fullmatch(line)
        assert m is not None
        a, b, c, d = map(int, m.groups())
        yield a, b, c, d


def part1(stdin: typing.TextIO):
    return sum(a <= c <= d <= b or c <= a <= b <= d for a, b, c, d in parse(stdin))


def part2(stdin: typing.TextIO):
    return sum(a <= d and b >= c for a, b, c, d in parse(stdin))
