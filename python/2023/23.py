from .. import ks
import typing
import collections.abc as cabc


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
    hubs = {p for p in grid.keys() if len([*neighbors(grid, p)]) > 2}
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


def crawl(
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


def part1(stdin: typing.TextIO):
    grid = ks.grid.from_lines(stdin)
    start = ks.P2(0, 1)

    def neighbors(p: ks.P2):
        if p not in grid:
            return
        match grid[p]:
            case "^":
                q = p + (-1, 0)
                if q in grid:
                    yield q
            case "v":
                q = p + (1, 0)
                if q in grid:
                    yield q
            case "<":
                q = p + (0, -1)
                if q in grid:
                    yield q
            case ">":
                q = p + (0, 1)
                if q in grid:
                    yield q
            case ".":
                for q in p.circ1(1):
                    if q in grid:
                        yield q
            case _:
                return

    # dists = dict[ks.P2, int]()
    # dists[start] = 0
    # for _ in range(sum(grid.shape)):
    #    for p, d in [*dists.items()]:
    #        for q in neighbors(p):
    #            if q not in dists:
    #                dists[q] = d + 1
    #            else:
    #                dists[q] = max(d + 1, dists[q])

    # return max(dists.values())

    def search(
        seen: frozenset[ks.P2], current: ks.P2, dist: int = 0
    ) -> cabc.Iterator[int]:
        found = False
        for p in neighbors(current):
            if p in seen:
                continue
            found = True
            yield from search(seen | {p}, p, dist + 1)
        if not found:
            yield dist

    return max(search(frozenset(), start, 0)) - 1


def part(neighbors: NeighborsFunction):
    def solve(stdin: typing.TextIO):
        grid = ks.grid.from_lines(stdin)
        start, end = ks.P2(0, 1), grid.shape - (1, 2)
        graph = condense(grid, neighbors, extra_hubs=[start, end])
        return max(crawl(graph, start, end))

    return solve


part1 = part(neighbors1)
part2 = part(neighbors2)
