from .. import ks
import typing


# @dc.dataclass
# class ParseResult:
#    grid: ks.Grid[str]
#    mirrors: set[ks.P2]
#    row: list[list[int]]
#    column: list[list[int]]
#
#
# def parse(stdin: typing.TextIO):
#    grid = ks.grid.from_lines(stdin)
#    mirrors = {p for p, c in grid.items() if c != "."}
#    row: list[list[int]] = [[] for _ in range(grid.size0)]
#    column: list[list[int]] = [[] for _ in range(grid.size1)]
#    for p in mirrors:
#        row[p.x].append(p.y)
#        column[p.y].append(p.x)
#    for g in row:
#        g.sort()
#    for g in column:
#        g.sort()
#    return ParseResult(grid, mirrors, row, column)


# def trace(pr: ParseResult, start: tuple[ks.P2, ks.P2]):
#    frontier = [start]
#    seen = {start}
#    while frontier:
#        pos, dir = frontier.pop()
#        match dir:
#            case ks.P2(-1, 0):
#                i = bs.bisect_right(pr.column[pos.y], pos.x)
#                if i == 0:
#                    continue
#                p = pr.column[pos.y][i - 1], pos.y
#
#            case ks.P2(1, 0):
#                i = bs.bisect_left(pr.column[pos.y], pos.x)
#                if i == pr.grid.size0:
#                    continue
#                p = pr.column[pos.y][i], pos.y
#
#            case ks.P2(0, -1):
#                i = bs.bisect_right(pr.row[pos.x], pos.y)
#                if i == 0:
#                    continue
#                p = pos.x, pr.row[pos.x][i - 1]
#
#            case ks.P2(0, 1):
#                i = bs.bisect_left(pr.row[pos.x], pos.y)
#                if i == pr.grid.size1:
#                    continue
#                p = pos.x, pr.row[pos.x][i]
#
#            case _:
#                assert False, dir
#
#        children: list[tuple[ks.P2, ks.P2]] = []
#        match pr.grid[p]:
#            case "/":
#                children.append((ks.P2(p), dir.reflect((1, -1))))
#            case "\\":
#                children.append((ks.P2(p), dir.reflect((1, 1))))
#            case "-":
#                if dir.x:
#                    children.append((ks.P2(p), dir.rot(1)))
#                    children.append((ks.P2(p), dir.rot(-1)))
#                else:
#                    children.append((ks.P2(p), dir))
#            case "|":
#                if dir.y:
#                    children.append((ks.P2(p), dir.rot(1)))
#                    children.append((ks.P2(p), dir.rot(-1)))
#                else:
#                    children.append((ks.P2(p), dir))
#            case c:
#                assert False, c
#
#        for child in children:
#            if child in seen:
#                continue
#            seen.add(child)
#            frontier.append(child)
#    return len({p for p, _ in seen})


def trace(grid: ks.Grid[str], start: tuple[ks.P2, ks.P2]):
    seen: set[tuple[ks.P2, ks.P2]] = set()
    frontier = [start]
    while frontier:
        parent, direction = frontier.pop()
        next = parent + direction
        if next not in grid:
            continue
        children: list[tuple[ks.P2, ks.P2]] = []
        match grid[next]:
            case ".":
                # pass through
                children.append((next, direction))
            case "-" if not direction.x:
                children.append((next, direction))
            case "|" if not direction.y:
                children.append((next, direction))
            case "-" | "|":
                children.append((next, direction.rot(1)))
                children.append((next, direction.rot(-1)))
            case "/":
                children.append((next, direction.reflect((1, 1))))
            case "\\":
                children.append((next, direction.reflect((1, -1))))
            case c:
                assert False, c
        for child in children:
            if child in seen:
                continue
            seen.add(child)
            frontier.append(child)
    return {p for p, _ in seen}


def part1(stdin: typing.TextIO):
    return len(trace(ks.grid.from_lines(stdin), (ks.P2(0, -1), ks.P2(0, 1))))


@ks.func.max
def part2(stdin: typing.TextIO):
    grid = ks.grid.from_lines(stdin)
    for i in range(grid.size0):
        print("row", i)
        yield len(trace(grid, (ks.P2(i, -1), ks.P2(0, 1))))
        yield len(trace(grid, (ks.P2(i, grid.size1), ks.P2(0, -1))))
    for i in range(grid.size1):
        print("column", i)
        yield len(trace(grid, (ks.P2(-1, i), ks.P2(1, 0))))
        yield len(trace(grid, (ks.P2(grid.size0, i), ks.P2(-1, 0))))
