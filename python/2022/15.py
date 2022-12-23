# pyright: strict

from .. import ks
import typing


def parse(stdin: typing.TextIO):
    for sx, sy, bx, by in ks.parse.lines_pattern(
        stdin, "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d"
    ):
        yield ks.coord.Coord(sx, sy), ks.coord.Coord(bx, by)


def part1(stdin: typing.TextIO):
    y = 2000000  # 10 for sample
    empty = ks.Dis()
    beacons: set[int] = set()
    for sensor, beacon in parse(stdin):
        if (width := sensor.dist_manhattan(beacon) - abs(sensor.y - y)) < 0:
            continue
        empty.add(ks.Interval(sensor.x - width, sensor.x + width))
        if beacon.y == y:
            beacons.add(beacon.x)
    return sum(i.r - i.l + 1 for i in empty.intervals()) - len(beacons)


def part2(stdin: typing.TextIO):
    size = 4000000  # 20 for sample

    # my approach here uses a BST-like data structure for disjoint intervals to
    # scan each row for gaps. jonathanpaulson suggested (on reddit) another
    # clever trick to solve this: search the _boundary_ (distance d+1) around
    # each sensor; the promise that there is exactly one 1x1 gap in the region
    # ensures that it must lie on a boundary. I tried implementing that, but for
    # some reason I was still running out of memory.

    pairs = [*parse(stdin)]

    for y in range(size + 1):
        intervals = ks.IntervalSet()
        for sensor, beacon in pairs:
            w = sensor.dist_manhattan(beacon) - abs(sensor.y - y)
            if w < 0:
                continue
            chunk = ks.Interval(sensor.x - w, sensor.x + w) & (0, size)
            if chunk is not None:
                intervals.union(chunk)

        match [*intervals.intervals()]:
            case [_]:
                pass

            case [a, b]:
                assert a.r + 2 == b.l
                return (a.r + 1) * 4000000 + y

            case _:
                assert False, "multiple slots"
