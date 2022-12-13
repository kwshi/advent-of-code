# pyright: strict
from .. import ks
import typing

import collections as co


def parse(stdin: typing.TextIO):
    grid = ks.grid.parse_chars(stdin)
    start = grid.find("S")
    end = grid.find("E")
    grid[start] = "a"
    grid[end] = "z"
    return start, end, grid


def bfs(
    grid: ks.grid.Grid[str],
    end: ks.grid.Key,
    is_start: typing.Callable[[ks.grid.Key], bool],
) -> int:
    front = co.deque([end])
    seen = {end: 0}
    while front:
        parent = front.popleft()
        dist = seen[parent] + 1
        for child in grid.neighbor_keys(parent):
            if child in seen or ord(grid[child]) + 1 < ord(grid[parent]):
                continue
            if is_start(child):
                return dist
            seen[child] = dist
            front.append(child)
    assert False, "not found"


def part1(stdin: typing.TextIO):
    start, end, grid = parse(stdin)
    return bfs(grid, end, lambda p: p == start)


def part2(stdin: typing.TextIO):
    _, end, grid = parse(stdin)
    return bfs(grid, end, lambda p: grid[p] == "a")
