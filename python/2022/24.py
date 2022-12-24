# pyright: strict
from .. import ks
import typing

import math
import collections as co

west = ks.coord.Coord((0, -1))
east = ks.coord.Coord((0, 1))
north = ks.coord.Coord((-1, 0))
south = ks.coord.Coord((1, 0))

Blizzards = dict[ks.coord.Coord, set[ks.coord.Coord]]


def parse(stdin: typing.TextIO):
    grid = ks.grid.parse_chars(stdin)
    blizzards: Blizzards = {west: set(), east: set(), north: set(), south: set()}
    for pos, cell in grid.items():
        match cell:
            case "<":
                blizzards[west].add(ks.coord.Coord(pos))
            case ">":
                blizzards[east].add(ks.coord.Coord(pos))
            case "^":
                blizzards[north].add(ks.coord.Coord(pos))
            case "v":
                blizzards[south].add(ks.coord.Coord(pos))
            case _:
                pass
    return blizzards, grid.height, grid.width


def evolve(blizzards: Blizzards, height: int, width: int):
    new: Blizzards = {}
    for direction, points in blizzards.items():
        ps: set[ks.coord.Coord] = set()
        new[direction] = ps
        for point in points:
            p = point + direction
            x = (p.x - 1) % (height - 2) + 1
            y = (p.y - 1) % (width - 2) + 1
            ps.add(ks.coord.Coord(x, y))
    return new


def render(blizzards: Blizzards, height: int, width: int):
    chars: co.defaultdict[ks.coord.Coord, set[str]] = co.defaultdict(set)
    for direction, points in blizzards.items():
        for point in points:
            chars[point].add({west: "<", east: ">", north: "^", south: "v"}[direction])

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            bs = chars[ks.coord.Coord(i, j)]
            print(bs.pop() if len(bs) == 1 else "." if not bs else str(len(bs)), end="")
        print()
    print()


def evolutions(blizzards: Blizzards, height: int, width: int):
    original = blizzards
    versions: dict[int, Blizzards] = {}
    for i in range((height - 2) * (width - 2) // math.gcd(height - 2, width - 2)):
        versions[i] = blizzards
        blizzards = evolve(blizzards, height, width)
    assert blizzards == original
    return versions


def taken(blizzards: Blizzards, pos: ks.coord.Coord):
    return any(pos in bs for bs in blizzards.values())


def search(
    versions: dict[int, Blizzards],
    height: int,
    width: int,
    start: tuple[int, ks.coord.Coord],
    goal: ks.coord.Coord,
):
    time, origin = start
    front = co.deque([start])
    seen = set({(time % len(versions), origin)})
    while front:
        time, parent = front.popleft()
        bs = versions[(time + 1) % len(versions)]
        for step in [north, south, west, east, ks.coord.Coord()]:
            child = parent + step
            # if debug:
            #    print(parent, child, start, goal, origin)
            if taken(bs, child):
                continue
            if child == goal:
                return time + 1
            if (
                not (0 < child.x < height - 1 and 0 < child.y < width - 1)
                and child != origin
            ):
                continue
            if (t := (time + 1) % len(versions), child) in seen:
                continue
            seen.add((t, child))
            front.append((time + 1, child))
    assert False, "path not found"


def part1(stdin: typing.TextIO):
    blizzards, height, width = parse(stdin)
    versions = evolutions(blizzards, height, width)
    return search(
        versions,
        height,
        width,
        (0, ks.coord.Coord(0, 1)),
        ks.coord.Coord(height - 1, width - 2),
    )


def part2(stdin: typing.TextIO):
    blizzards, height, width = parse(stdin)
    versions = evolutions(blizzards, height, width)

    origin = ks.coord.Coord(0, 1)
    end = ks.coord.Coord(height - 1, width - 2)

    tgo = search(versions, height, width, (0, origin), end)
    tback = search(versions, height, width, (tgo, end), origin)
    return search(versions, height, width, (tback, origin), end)
