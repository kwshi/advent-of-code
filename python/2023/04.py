# pyright: strict
from .. import ks
import typing

import re
import collections as co


def parse(stdin: typing.TextIO):
    for line in stdin:
        match = re.fullmatch(r"Card\s+(\d+):(.*)\|(.*)", line.rstrip())
        assert match is not None, repr(line.rstrip())
        n, winning, stuff = match.groups()
        yield int(n), map(int, winning.split()), map(int, stuff.split())


@ks.func.sum
def part1(stdin: typing.TextIO):
    for _, winning, stuff in parse(stdin):
        good = {*winning} & {*stuff}
        if not good:
            continue
        yield 2 ** (len(good) - 1)


@ks.func.sum
def part2(stdin: typing.TextIO):
    extra: co.defaultdict[int, int] = co.defaultdict(int)
    for i, winning, stuff in parse(stdin):
        yield (m := extra[i] + 1)
        for j in range(len({*winning} & {*stuff})):
            extra[i + j + 1] += m
