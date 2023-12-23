from .. import ks
import typing


import functools as ft
import collections as co
import bisect as bs


def evolve(grid: ks.Grid[str], stuff: set[ks.P2]):
    for p in stuff:
        for q in p.circ1(1):
            if q in grid and grid[q] != "#":
                yield q


def part1_slow(stdin: typing.TextIO):
    grid = ks.grid.from_lines(stdin)

    start = grid.find("S")
    assert start is not None

    level = {start}
    for _ in range(64):
        level = {*evolve(grid, level)}
        print(len(level))

    print(len(level))
    return len(level)


def even_neighbors(grid: ks.Grid[str]):
    @ft.lru_cache(None)
    def get(p: ks.P2):
        one = {q for q in p.circ1(1) if q in grid and grid[q] != "#"}
        return {r for q in one for r in q.circ1(1) if r in grid and grid[r] != "#"}

    return get


def part1(stdin: typing.TextIO):
    grid = ks.grid.from_lines(stdin)

    start = grid.find("S")
    assert start is not None

    neighbors = even_neighbors(grid)

    frontier = co.deque[tuple[ks.P2, int]]([(start, 0)])
    seen = {start}
    while frontier:
        current, dist = frontier.popleft()
        for p in neighbors(current):
            if p in seen:
                continue
            seen.add(p)
            if dist + 2 == 64:
                continue
            frontier.append((p, dist + 2))

    return len(seen)


def even_neighbors_wrap(grid: ks.Grid[str]):
    @ft.lru_cache(None)
    def get(p: ks.P2):
        one = {q for q in p.circ1(1) if grid[q % grid.shape] != "#"}
        return {r for q in one for r in q.circ1(1) if grid[r % grid.shape] != "#"} - {p}

    return get


def part2(stdin: typing.TextIO):
    lines = [*stdin]
    grid = ks.grid.from_lines(lines)

    origin = grid.find("S")
    assert origin is not None

    assert grid.shape == (131, 131)
    assert 26501365 == 202300 * grid.size0 + grid.size0 // 2

    neighbors = even_neighbors_wrap(grid)

    start = {p for p in origin.circ1(1) if p in grid and p != "#"}

    frontier = co.deque[tuple[ks.P2, int]]((p, 1) for p in start)
    seen = {p: 1 for p in start}
    while frontier:
        current, dist = frontier.popleft()
        print(dist)
        for p in neighbors(current):
            if p in seen:
                continue
            seen[p] = dist + 2
            if dist + 2 == 6 * grid.size0 + grid.size0 // 2:
                continue
            frontier.append((p, dist + 2))

    history = [*seen.items()]
    data = [
        bs.bisect_right(history, k * 131 + 65, key=lambda p: p[1])
        for k in range(0, 7, 2)
    ]
    a, b, c, d = data
    x, y, z = b - a, c - b, d - c
    assert (α := y - x) == z - y

    # manual quadratic fit:
    # f(t) = u t² + v t + w
    # g(t) = f(t+2) - f(t) = u (4t + 4) + 2 v = 4 u t + 4 u + 2 v
    # h(t) = g(t+2) - g(t) = 8 u
    # u = α/8, v = g(0)/2-2u = x/2-α/4, w = f(0) = a

    print(data)

    def f(t: int):
        return (α * t**2 + (4 * x - 2 * α) * t) // 8 + a

    assert f(0) == a
    assert f(2) == b
    assert f(4) == c
    assert f(6) == d
    return f(202300)
