from .. import ks
import typing

import itertools as it
import pprint as pp

type Brick = tuple[ks.P3, ks.P3]


def parse(stdin: typing.TextIO):
    for line in stdin:
        a, b = line.rstrip().split("~")
        yield ks.P3(*map(int, a.split(","))), ks.P3(*map(int, b.split(",")))


def fall(bricks: list[Brick]):
    bricks.sort(key=lambda ps: min(ps[0].z, ps[1].z))

    height = dict[ks.P2, tuple[int, int]]()
    pos = list[tuple[int, set[int]]]()
    for i, (a, b) in enumerate(bricks):
        xs = range(min(a.x, b.x), max(a.x, b.x) + 1)
        ys = range(min(a.y, b.y), max(a.y, b.y) + 1)
        h = max(a.z, b.z) - min(a.z, a.z) + 1
        base = 0
        for x, y in it.product(xs, ys):
            p = ks.P2(x, y)
            if p not in height:
                continue
            z, _ = height[p]
            base = max(base, z)

        deps = set[int]()
        for x, y in it.product(xs, ys):
            p = ks.P2(x, y)
            if p not in height:
                continue
            z, owner = height[p]
            if z == base:
                deps.add(owner)

        pos.append((base, deps))
        for x, y in it.product(xs, ys):
            height[ks.P2(x, y)] = (base + h, i)

    depend = [dep for _, dep in pos]
    support = [set[int]() for _ in pos]
    for i, dep in enumerate(depend):
        for d in dep:
            support[d].add(i)

    return depend, support


def part1(stdin: typing.TextIO):
    depend, _ = fall([*parse(stdin)])
    safe = {*range(len(depend))}
    for deps in depend:
        if len(deps) == 1:
            safe -= deps
    pp.pprint(safe)
    return len(safe)


@ks.func.sum
def part2(stdin: typing.TextIO):
    depend, support = fall([*parse(stdin)])
    for start in range(len(depend)):
        seen = {start}
        frontier = [start]
        while frontier:
            current = frontier.pop()
            for p in support[current]:
                if p in seen:
                    continue
                if depend[p] - seen:
                    continue
                frontier.append(p)
                seen.add(p)
        yield len(seen) - 1
