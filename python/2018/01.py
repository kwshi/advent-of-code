# pyright: strict
import itertools as it
import typing
from .. import ks


def parse(stdin: typing.TextIO):
    return map(int, ks.parse.lines(stdin))


def part1(stdin: typing.TextIO):
    return sum(parse(stdin))


def part2(stdin: typing.TextIO):
    seen: set[int] = set()
    for s in it.accumulate(it.cycle(parse(stdin))):
        if s in seen:
            return s
        seen.add(s)
