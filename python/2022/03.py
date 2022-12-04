# pyright: strict

from .. import ks
import typing

import string


priority: dict[str, int] = {}
for i, c in enumerate(string.ascii_lowercase):
    priority[c] = i + 1
    priority[c.upper()] = i + 1 + 26


@ks.func.sumify
def part1(stdin: typing.TextIO):
    for line in ks.parse.lines(stdin):
        i = len(line) // 2
        both = {*line[:i]} & {*line[i:]}
        assert len(both) == 1
        yield priority[both.pop()]


@ks.func.sumify
def part2(stdin: typing.TextIO):
    for a, b, c in ks.iter.grouper(ks.parse.lines(stdin), 3):
        trip = {*a} & {*b} & {*c}
        assert len(trip) == 1
        yield priority[trip.pop()]
