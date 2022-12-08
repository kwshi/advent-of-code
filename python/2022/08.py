# pyright: strict
from .. import ks
import typing

import itertools as it

Grid = list[list[int]]
Position = tuple[int, int]
Positions = typing.Iterable[Position]


def parse(stdin: typing.TextIO):
    grid = [[*map(int, row)] for row in ks.parse.lines(stdin)]
    return grid, len(grid), len(grid[0])


def visualize(grid: Grid, pos: Positions):
    highest = None
    for i, j in pos:
        c = grid[i][j]
        if highest is None or highest < c:
            yield i, j
            highest = c


def part1(stdin: typing.TextIO):
    grid, m, n = parse(stdin)
    visible: set[Position] = set()

    for i in range(m):
        visible.update(visualize(grid, ((i, j) for j in range(n))))
        visible.update(visualize(grid, ((i, n - 1 - j) for j in range(n))))

    for j in range(n):
        visible.update(visualize(grid, ((i, j) for i in range(m))))
        visible.update(visualize(grid, ((m - 1 - i, j) for i in range(m))))

    return len(visible)


def view(grid: Grid, here: int, pos: Positions) -> int:
    dist = 0
    for (i, j) in pos:
        dist += 1
        if grid[i][j] >= here:
            break
    return dist


def part2(stdin: typing.TextIO):
    grid, m, n = parse(stdin)

    best = 0
    for i, j in it.product(range(m), range(n)):
        here = grid[i][j]
        best = max(
            best,
            view(grid, here, ((ii, j) for ii in range(i + 1, m, 1)))
            * view(grid, here, ((ii, j) for ii in range(i - 1, -1, -1)))
            * view(grid, here, ((i, jj) for jj in range(j + 1, n, 1)))
            * view(grid, here, ((i, jj) for jj in range(j - 1, -1, -1))),
        )

    return best
