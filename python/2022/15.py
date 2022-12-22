from .. import ks
import typing

import math
import string
import re
import itertools as it
import bisect as bs
import functools as ft
import collections as co
import operator as op
import dataclasses as dc
import heapq as hq
import pprint as pp
import graphlib as gl


def parse(stdin: typing.TextIO):
    for sx, sy, bx, by in ks.parse.lines_pattern(
        stdin, "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d"
    ):
        yield ks.coord.Coord(sx, sy), ks.coord.Coord(bx, by)


def part1(stdin: typing.TextIO):
    empty = set()
    y = 2000000  # 10 for sample
    for sensor, beacon in parse(stdin):
        for dx in range(sensor.dist_taxicab(beacon) - abs(sensor.y - y) + 1):
            empty.add(sensor.x + dx)
            empty.add(sensor.x - dx)
        if beacon.y == y:
            empty.remove(beacon.x)
    return len(empty)


def insert(
    intervals: typing.Iterable[tuple[int, int]], left: int, right: int
) -> typing.Iterator[tuple[int, int]]:
    start = False
    for l, r in intervals:
        match start:
            case True:
                yield l, r

            case False:
                if r < left - 1:
                    yield l, r
                    continue

                if l > right + 1:
                    yield left, right
                    yield l, r
                    start = True
                    continue

                if r <= right:
                    yield min(left, l), right
                    start = True
                    continue

                start = min(left, l)

            case int():
                if r <= right:
                    yield start, right
                pass


# TODO interval-set solution
# TODO n+1 solution (jonathan paulson's insight)
def part2(stdin: typing.TextIO):
    size = 4000000  # 20 for sample
    # size = 20

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
