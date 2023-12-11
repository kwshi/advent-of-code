from .. import ks
import typing

import itertools as it
import bisect as bs


def solver(multiplier: int):
    @ks.func.sum
    def solve(stdin: typing.TextIO):
        grid = ks.grid.read_chars(stdin)
        stars = {p for p in grid.keys0() if grid[p] == '#'}
        stars0 = {p.x for p in stars}
        stars1 = {p.y for p in stars}
        empty0 = sorted({*range(grid.size0)} - stars0)
        empty1 = sorted({*range(grid.size0)} - stars1)

        for p, q in it.combinations(stars, 2):
            x1 = min(p.x, q.x)
            x2 = max(p.x, q.x)
            y1 = min(p.y, q.y)
            y2 = max(p.y, q.y)
            nx = bs.bisect_left(empty0, x2) - bs.bisect_left(empty0, x1)
            ny = bs.bisect_left(empty1, y2) - bs.bisect_left(empty1, y1)
            yield (multiplier-1)*(nx + ny) + (x2-x1) + (y2-y1)

    return solve

part1 = solver(2)
part2 = solver(1000000)
