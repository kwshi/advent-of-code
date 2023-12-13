from .. import ks
import typing

import io


def parse(stdin: typing.TextIO):
    chunks = stdin.read().strip().split("\n\n")
    for chunk in chunks:
        yield ks.grid.read_chars(io.StringIO(chunk))


def diff_h(grid: ks.grid.Grid[str], i: int):
    dist = min(i, grid.size0 - i)
    return sum(
        grid[i + j, k] != grid[i - j - 1, k]
        for k in range(grid.size1)
        for j in range(dist)
    )


def make(flips: int):
    def total_h(grid: ks.grid.Grid[str]):
        return sum(i for i in range(1, grid.size0) if diff_h(grid, i) == flips)

    def solve(stdin: typing.TextIO):
        h = v = 0
        for grid in parse(stdin):
            h += total_h(grid)
            grid.transpose()
            v += total_h(grid)
        return h * 100 + v

    return solve


part1 = make(0)
part2 = make(1)
