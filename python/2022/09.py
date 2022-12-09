# pyright: strict
from .. import ks
import typing
import itertools as it

offset: dict[str, tuple[int, int]] = {
    "L": (-1, 0),
    "R": (1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def parse(stdin: typing.TextIO) -> typing.Iterator[tuple[int, int]]:
    for d, n in ks.parse.lines_pattern(stdin, "%s %d"):
        yield from it.repeat(offset[d], n)


def advance(a: ks.coord.Coord, b: ks.coord.Coord) -> ks.coord.Coord:
    return a if a.dist_max(b) <= 1 else a + (b - a).sign()


@ks.func.count_unique
def part1(stdin: typing.TextIO) -> typing.Iterator[ks.coord.Coord]:
    head = tail = ks.coord.Coord()
    for d in parse(stdin):
        head += d
        tail = advance(tail, head)
        yield tail


@ks.func.count_unique
def part2(stdin: typing.TextIO) -> typing.Iterator[ks.coord.Coord]:
    rope = [ks.coord.Coord()] * 10
    for d in parse(stdin):
        rope[0] += d
        for i in range(len(rope) - 1):
            rope[i + 1] = advance(rope[i + 1], rope[i])
        yield rope[-1]
