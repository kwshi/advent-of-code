from .. import ks
import typing
import collections.abc as cabc
import itertools as it


type NeighborsFunction = cabc.Callable[[ks.Grid[str], ks.P2], cabc.Iterator[ks.P2]]


def neighbors1(grid: ks.Grid[str], p: ks.P2):
    if p not in grid:
        return
    offset = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    match grid[p]:
        case "^" | "v" | "<" | ">" as c:
            q = p + offset[c]
            if q in grid:
                yield q
        case ".":
            for q in p.circ1(1):
                if q in grid:
                    yield q
        case _:
            pass


def neighbors2(grid: ks.Grid[str], p: ks.P2):
    if p not in grid:
        return
    for q in p.circ1(1):
        if q in grid and grid[q] != "#":
            yield q


def condense(
    grid: ks.Grid[str],
    neighbors: NeighborsFunction,
    /,
    extra_hubs: cabc.Iterable[ks.P2],
):
    hubs = {p for p, c in grid.items() if len([*neighbors(grid, p)]) > 2 and c != "#"}
    hubs.update(extra_hubs)

    def hub_neighbors(start: ks.P2, move: ks.P2):
        if move in hubs:
            return {move: 1}

        frontier = [(move, int(1))]
        seen = {start, move}
        end = dict[ks.P2, int]()
        while frontier:
            p, d = frontier.pop()
            for q in neighbors(grid, p):
                if q in seen:
                    continue
                if q in hubs:
                    end[q] = d + 1
                    continue
                seen.add(q)
                frontier.append((q, d + 1))
        return end

    graph = {h: dict[ks.P2, int]() for h in hubs}
    for p, dist in graph.items():
        for move in neighbors(grid, p):
            for q, d in hub_neighbors(p, move).items():
                dist[q] = max(dist.get(q, d), d)

    return graph


# These two `crawl` functions are the same, but the `fast` implementation uses
# only a single `seen` set, taking care to push and pop elements in exactly the
# right order (DFS) so that it has the right elements at each iteration; in
# contrast, the `slow` implementation generates a new `frozenset` at each step,
# which is less error-prone, but uses a lot more memory (unless Python's
# `frozenset` has a clever implementation that I'm not aware of?).
def crawl_slow(
    graph: dict[ks.P2, dict[ks.P2, int]], start: ks.P2, end: ks.P2
) -> cabc.Iterator[int]:
    init = start, frozenset([start]), int()
    stack = [init]
    while stack:
        p, seen, dist = stack.pop()
        for q, d in graph[p].items():
            if q in seen:
                continue
            if q == end:
                yield dist + d
            stack.append((q, seen | {q}, dist + d))


def crawl_fast(
    graph: dict[ks.P2, dict[ks.P2, int]], start: ks.P2, end: ks.P2
) -> cabc.Iterator[int]:
    stack: list[tuple[ks.P2, int | None]] = [(start, 0)]
    seen = set[ks.P2]()
    while stack:
        p, dist = stack.pop()
        if dist is None:
            seen.remove(p)
            continue
        seen.add(p)
        stack.append((p, None))
        for q, d in graph[p].items():
            if q in seen:
                continue
            if q == end:
                yield dist + d
            stack.append((q, dist + d))


def part(neighbors: NeighborsFunction):
    def solve(stdin: typing.TextIO):
        grid = ks.grid.from_lines(stdin)
        start, end = ks.P2(0, 1), grid.shape - (1, 2)
        graph = condense(grid, neighbors, extra_hubs=[start, end])
        return max(crawl_fast(graph, start, end))

    return solve


part1 = part(neighbors1)
part2 = part(neighbors2)
