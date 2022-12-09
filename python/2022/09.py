# pyright: strict
from .. import ks
import typing

offset: dict[str, tuple[int, int]] = {
    "L": (-1, 0),
    "R": (1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def parse(stdin: typing.TextIO) -> typing.Iterator[tuple[tuple[int, int], int]]:
    for d, n in ks.parse.lines_pattern(stdin, "%s %d"):
        yield offset[d], n


def advance(a: ks.coord.Coord, b: ks.coord.Coord) -> ks.coord.Coord:
    return a if a.dist_max(b) <= 1 else a + (b - a).sign()


def part1(stdin: typing.TextIO) -> int:
    head = tail = ks.coord.Coord()
    seen: set[ks.coord.Coord] = {head}

    for d, n in parse(stdin):
        for _ in range(n):
            head += d
            tail = advance(tail, head)
            seen.add(tail)

    return len(seen)


def part2(stdin: typing.TextIO) -> int:
    rope = [ks.coord.Coord()] * 10
    seen: set[ks.coord.Coord] = set()

    for d, n in parse(stdin):
        for _ in range(n):
            rope[0] += d
            for i in range(len(rope) - 1):
                rope[i + 1] = advance(rope[i + 1], rope[i])
            seen.add(rope[-1])

    return len(seen)
