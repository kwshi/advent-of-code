# pyright: strict
from .. import ks
import typing

import itertools as it
import collections as co

import re

re_claim = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")


def parse(stdin: typing.TextIO):
    for line in ks.parse.lines(stdin):
        match = re_claim.fullmatch(line)
        assert match
        i, x, y, width, height = map(int, match.groups())
        yield i, x, y, width, height


def part1(stdin: typing.TextIO):
    grid: co.defaultdict[tuple[int, int], int] = co.defaultdict(int)
    for _, x, y, width, height in parse(stdin):
        for p in it.product(range(x, x + width), range(y, y + height)):
            grid[p] += 1
    return sum(1 for v in grid.values() if v >= 2)


def part2(stdin: typing.TextIO):
    ids: set[int] = set()
    dependent: set[int] = set()
    owner: dict[tuple[int, int], int] = {}
    for i, x, y, width, height in parse(stdin):
        ids.add(i)
        for p in it.product(range(x, x + width), range(y, y + height)):
            if p in owner:
                dependent.add(owner[p])
                dependent.add(i)
                continue
            owner[p] = i
    return (ids - dependent).pop()
