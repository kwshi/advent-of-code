# pyright: strict
from .. import ks
import typing

import collections as co


def parse(stdin: typing.TextIO):
    for line in ks.parse.lines(stdin):
        x, y = map(int, line.split(", "))
        yield x, y


def neighbors(p: tuple[int, int]):
    x, y = p
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def part1(stdin: typing.TextIO):
    tentative = {p: i for i, p in enumerate(parse(stdin))}

    xs, ys = zip(*tentative.keys())
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    nearest: dict[tuple[int, int], int] = {}
    front = co.deque(tentative.keys())
    unbounded: set[int] = set()
    while front:
        pos = front.popleft()
        if tentative[pos] == -1:
            continue

        nearest[pos] = tentative[pos]

        x, y = pos
        if x > x_max or y > y_max or x < x_min or y < y_min:
            unbounded.add(tentative[pos])
            continue

        for neighbor in neighbors(pos):
            if neighbor in tentative:
                continue
            tentative[neighbor] = tentative[pos]
            front.append(neighbor)

    counts = co.Counter(nearest.values())
    for key in unbounded:
        del counts[key]
    return max(counts.values())


def part1_alt(stdin: typing.TextIO):
    nearest: dict[tuple[int, int], int] = {}
    for i, p in enumerate(parse(stdin)):
        nearest[p] = i

    xs, ys = zip(*nearest.keys())
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    front = [*nearest.keys()]
    unbounded: set[int] = set()
    while front:
        claims: dict[tuple[int, int], int] = {}
        for p in front:
            x, y = p
            if x > x_max or y > y_max or x < x_min or y < y_min:
                unbounded.add(nearest[p])
                continue

            for neighbor in neighbors(p):
                if neighbor in nearest:
                    continue
                if neighbor in claims and claims[neighbor] != nearest[p]:
                    claims[neighbor] = -1
                    continue
                claims[neighbor] = nearest[p]

        nearest.update(claims)
        front = [*claims.keys()]
    print(len(nearest))

    counts = co.Counter(nearest.values())
    for key in unbounded:
        del counts[key]
    return max(counts.values())


def median(l: list[int]):
    return l[len(l) >> 1] if len(l) & 1 else l[len(l) >> 1] + l[(len(l) >> 1) - 1] >> 1


def part2(stdin: typing.TextIO):
    max_dist = 10000

    points = [*parse(stdin)]
    xs, ys = map(sorted, zip(*points))
    mid = median(xs), median(ys)

    def dist(pos: tuple[int, int]):
        x, y = pos
        return sum(abs(x - xx) + abs(y - yy) for xx, yy in points)

    if dist(mid) >= max_dist:
        return 0

    front = co.deque([mid])
    good = {mid: True}
    while front:
        pos = front.popleft()
        for neighbor in neighbors(pos):
            if neighbor in good:
                continue
            good[neighbor] = (g := dist(neighbor) < max_dist)
            if g:
                front.append(neighbor)

    return co.Counter(good.values())[True]
