# pyright: strict
from .. import ks
import typing

import math


def visualize(grid: ks.grid.Grid[int], pos: typing.Iterable[ks.grid.Key]):
    highest = None
    for p in pos:
        if highest is None or highest < grid[p]:
            highest = grid[p]
            yield p


def part1(stdin: typing.TextIO):
    grid = ks.grid.parse_digits(stdin)
    visible: set[ks.grid.Key] = set()

    for i in range(grid.height):
        visible.update(visualize(grid, grid.row_keys(i)))
        visible.update(visualize(grid, grid.row_keys(i, reverse=True)))

    for j in range(grid.width):
        visible.update(visualize(grid, grid.column_keys(j)))
        visible.update(visualize(grid, grid.column_keys(j, reverse=True)))

    return len(visible)


def view(grid: ks.grid.Grid[int], here: int, pos: typing.Iterable[ks.grid.Key]) -> int:
    dist = 0
    for p in pos:
        dist += 1
        if grid[p] >= here:
            break
    return dist


def part2(stdin: typing.TextIO):
    grid = ks.grid.parse_digits(stdin)

    best = 0
    for p in grid.keys():
        best = max(
            best,
            math.prod(
                view(grid, grid[p], ray)
                for ray in grid.rays_keys(p, include_start=False)
            ),
        )

    return best
