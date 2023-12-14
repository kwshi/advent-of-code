from .. import ks
import typing

import itertools as it


def collapse(grid: ks.grid.Grid[str]):
    for p in grid.keys0():
        if grid[p] != "O":
            continue
        q = p
        while q.x > 0 and grid[q - (1, 0)] == ".":
            q -= (1, 0)
        if p == q:
            continue
        grid[q] = "O"
        grid[p] = "."


def stringify(grid: ks.grid.Grid[str]):
    return "".join(grid.iter0())


def collapse_cycle(grid: ks.grid.Grid[str]):
    collapse(grid)  # n
    grid.rot(-1)
    collapse(grid)  # w
    grid.rot(-1)
    collapse(grid)  # s
    grid.rot(-1)
    collapse(grid)  # e
    grid.rot(-1)


def total(grid: ks.grid.Grid[str]):
    return sum(grid.size0 - p.x for p in grid.keys0() if grid[p] == "O")


@ks.func.sum
def part1(stdin: typing.TextIO):
    grid = ks.grid.read_chars(stdin)
    grid.display()
    collapse(grid)
    grid.display()
    return total(grid)


def find_cycle(grid: ks.grid.Grid[str]):
    memory = {stringify(grid): 0}
    for i in it.count(1):
        collapse_cycle(grid)
        s = stringify(grid)
        if s in memory:
            return memory[s], i - memory[s], memory
        memory[s] = i
    assert False


def part2(stdin: typing.TextIO):
    grid = ks.grid.read_chars(stdin)
    start, period, memory = find_cycle(grid)
    index: dict[int, str] = {}
    for s, i in memory.items():
        index[i] = s
    time = 1000000000
    q = index[(start + (time - start) % period)]
    g = ks.grid.read_chars(map("".join, it.batched(q, grid.size1)))
    return total(g)
