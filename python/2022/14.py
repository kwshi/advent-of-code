# pyright: strict

from .. import ks
import typing

import itertools as it

Grid = dict[ks.coord.Coord, str]


def parse_point(s: str) -> ks.coord.Coord:
    x, y = map(int, s.split(","))
    return ks.coord.Coord(x, y)


def inc_range(a: int, b: int) -> range:
    return range(min(a, b), max(a, b) + 1)


def parse(stdin: typing.TextIO) -> tuple[Grid, int]:
    grid: Grid = {}
    for line in ks.parse.lines(stdin):
        for a, b in it.pairwise(map(parse_point, line.split(" -> "))):
            if a.x == b.x:
                for y in inc_range(a.y, b.y):
                    grid[ks.coord.Coord(a.x, y)] = "#"
            elif a.y == b.y:
                for x in inc_range(a.x, b.x):
                    grid[ks.coord.Coord(x, a.y)] = "#"
            else:
                assert False, "non-hv edge"
    return grid, max(p.y for p in grid.keys())


def step(grid: Grid, pos: ks.coord.Coord) -> ks.coord.Coord | None:
    for dp in [(0, 1), (-1, 1), (1, 1)]:
        if (p := pos + dp) not in grid:
            return p


@ks.func.sumify
def part1(stdin: typing.TextIO) -> typing.Iterator[int]:
    grid, lowest = parse(stdin)
    while True:
        pos = ks.coord.Coord(500, 0)
        while (p := step(grid, pos)) is not None:
            if p.y == lowest:
                return
            pos = p
        grid[pos] = "o"
        yield 1


@ks.func.sumify
def part2(stdin: typing.TextIO):
    grid, lowest = parse(stdin)
    start = ks.coord.Coord(500, 0)
    while start not in grid:
        pos = start
        while pos.y < lowest + 1 and (p := step(grid, pos)) is not None:
            pos = p
        grid[pos] = "o"
        yield 1
