from .. import ks
import typing

import re
import itertools as it
import collections as co

re_move = re.compile(r"\d+|[LR]")


def parse_moves(moves: list[str]):
    for m in moves:
        yield int(m) if m.isnumeric() else m


def parse(stdin: typing.TextIO):
    rows, moves = ks.parse.chunks(stdin)
    grid = {}
    first = None
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            if c == " ":
                continue
            if first is None:
                first = j
            grid[i, j] = c
    assert first is not None
    return grid, [*parse_moves(re_move.findall(moves[0]))], first


facing = {
    ks.coord.Coord(1, 0): 1,
    ks.coord.Coord(-1, 0): 3,
    ks.coord.Coord(0, 1): 0,
    ks.coord.Coord(0, -1): 2,
}


def part1(stdin: typing.TextIO):
    grid, moves, first = parse(stdin)
    pos = ks.coord.Coord(0, first)
    head = ks.coord.Coord(0, 1)

    row_min = {}
    row_max = {}
    col_min = {}
    col_max = {}
    for i, j in grid.keys():
        row_min[i] = min(row_min.get(i, 10000000), j)
        row_max[i] = max(row_max.get(i, -10000000), j)
        col_min[j] = min(col_min.get(j, 10000000), i)
        col_max[j] = max(col_max.get(j, -10000000), i)

    wrap = {
        ks.coord.Coord(1, 0): col_min,
        ks.coord.Coord(-1, 0): col_max,
        ks.coord.Coord(0, 1): row_min,
        ks.coord.Coord(0, -1): row_max,
    }

    for move in moves:
        match move:
            case int():
                for _ in range(move):
                    pp = pos + head
                    print("check", pos, pp)
                    if tuple(pp) not in grid:
                        k = pos.y if head.x else pos.x
                        pp = (
                            ks.coord.Coord(wrap[head][k], k)
                            if head.x
                            else ks.coord.Coord(k, wrap[head][k])
                        )
                        print("wrap", pos, pp, head)
                    if grid[*pp] == "#":
                        break
                    pos = pp

            case "L":
                head = ks.coord.Coord(-head.y, head.x)

            case "R":
                head = ks.coord.Coord(head.y, -head.x)

    print(pos, head)
    return (pos.x + 1) * 1000 + (pos.y + 1) * 4 + facing[head]


def part2(stdin: typing.TextIO):
    grid, moves, first = parse(stdin)

    wrap: dict[
        tuple[ks.coord.Coord, ks.coord.Coord], tuple[ks.coord.Coord, ks.coord.Coord]
    ] = {}

    size = 50
    right = ks.coord.Coord(0, 1)
    start = ks.coord.Coord(0, first)
    front = [(start, right)]
    sections = co.defaultdict(set)
    seen = set()
    while front:
        parent, pright = front.pop()
        for disp in facing.keys():
            neighbor = parent + disp
            if neighbor in seen:
                continue
            if tuple(neighbor) not in grid:
                continue

            seen.add(neighbor)

            gp = ks.coord.Coord(parent.x // size, parent.y // size)
            gn = ks.coord.Coord(neighbor.x // size, neighbor.y // size)
            if gp == gn:
                front.append((neighbor, pright))
                continue
            sections[gp].add(gn - gp)
            sections[gn].add(gp - gn)
            wrap[gp, disp] = gn, disp
            wrap[gn, -disp] = gp, -disp

            front.append((neighbor, pright))

    # wrap[(0, 1), ks.coord.Coord(0, -1)] = (2, 0), ks.coord.Coord(0, 1)
    # wrap[(0, 1), ks.coord.Coord(-1, 0)] = (2, 0), ks.coord.Coord(0, 1)

    counts = {k: len(n) for k, n in sections.items()}
    unfinished = {k for k, c in counts.items() if c < 4}
    while unfinished:
        for k, nds in sections.items():
            for a, b in it.combinations(nds, 2):
                cross = a.cross(b)
                if not cross:
                    continue
                # assert b not in sections[k + a]
                na, da = wrap[k, a]
                nb, db = wrap[k, b]
                dab = -da.cross_z(cross)
                dba = db.cross_z(cross)
                if dab in sections[na]:
                    assert dba in sections[nb]
                    continue
                wrap[na, dab] = nb, -dba
                wrap[nb, dba] = na, -dab
                sections[na].add(dab)
                sections[nb].add(dba)
                if len(sections[na]) == 4:
                    unfinished.discard(na)
                if len(sections[nb]) == 4:
                    unfinished.discard(nb)

    pos = start
    head = ks.coord.Coord(0, 1)

    row_min = {}
    row_max = {}
    col_min = {}
    col_max = {}
    for i, j in grid.keys():
        row_min[i] = min(row_min.get(i, 10000000), j)
        row_max[i] = max(row_max.get(i, -10000000), j)
        col_min[j] = min(col_min.get(j, 10000000), i)
        col_max[j] = max(col_max.get(j, -10000000), i)

    for move in moves:
        match move:
            case int():
                for _ in range(move):
                    pp = pos + head
                    if tuple(pp) not in grid:
                        g = pos // size
                        ng, nh = wrap[g, head]
                        hy = head.cross_z(-1)
                        ny = nh.cross_z(-1)

                        o = g * size + (size - 1) * ((head - hy + 1) // 2)
                        no = ng * size + (size - 1) * ((nh - ny + 1) // 2)

                        dp = pos - o
                        pp = no + dp @ head * nh + (dp @ hy) * ny - nh * (size - 1)
                        print("wrapping", pos, head, pp, nh)

                        if grid[*pp] != "#":
                            head = nh

                    if grid[*pp] == "#":
                        break
                    pos = pp

            case "L":
                head = ks.coord.Coord(-head.y, head.x)

            case "R":
                head = ks.coord.Coord(head.y, -head.x)

    print(pos, head)
    return (pos.x + 1) * 1000 + (pos.y + 1) * 4 + facing[head]
