# pyright: strict
from .. import ks
import typing


def parse(stdin: typing.TextIO) -> set[tuple[int, int, int]]:
    return set(map(tuple, ks.parse.lines_pattern(stdin, "%d,%d,%d")))


def adjacent(p: tuple[int, int, int]):
    x, y, z = p
    for dx, dy, dz in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
        for sign in [-1, 1]:
            yield x + sign * dx, y + sign * dy, z + sign * dz


@ks.func.sumify
def part1(stdin: typing.TextIO):
    seen = parse(stdin)
    for p in seen:
        for a in adjacent(p):
            if a not in seen:
                yield 1


def part2(stdin: typing.TextIO):
    seen = parse(stdin)

    empty = ks.Uf()
    for p in seen:
        for a in adjacent(p):
            if a in seen:
                continue

            empty.add(a)
            for aa in adjacent(a):
                if aa in seen:
                    continue
                empty.add(aa)
                empty.merge(a, aa)

    xmax = max(x for x, _, _ in seen)
    xmin = min(x for x, _, _ in seen)
    ymax = max(y for _, y, _ in seen)
    ymin = min(y for _, y, _ in seen)
    zmax = max(z for _, _, z in seen)
    zmin = min(z for _, _, z in seen)

    for component in empty.components().values():
        if all(
            (xmin <= x <= xmax and ymin <= y <= ymax and zmin <= z <= zmax)
            for x, y, z in component
        ):
            continue

        return sum(a in seen for p in component for a in adjacent(p))
