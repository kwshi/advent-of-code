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

# @dc.dataclass
# class ResourceMap:
#    source


def parse(stdin: typing.TextIO):
    parts = stdin.read().strip().split("\n\n")
    seeds, *maps = parts

    seeds = map(int, seeds.removeprefix("seeds: ").split())
    ms = []
    for m in maps:
        title, *stuff = m.split("\n")
        f, t = title.split()[0].split("-to-")
        ms.append((f, t, [[*map(int, l.split())] for l in stuff]))

    return seeds, ms


def convert(converter: list[tuple[int, int, int]]):
    converter.sort(key=lambda p: p[1])

    def conv(n: int):
        i = bs.bisect_right(converter, n, key=lambda p: p[1]) - 1
        if i < 0:
            return n
        dest, source, width = converter[i]
        if source <= n < source + width:
            return dest + (n - source)
        else:
            return n

    return conv


def convert_image(
    converter: list[tuple[int, int, int]], intervals: list[ks.interval.Interval]
) -> list[ks.interval.Interval]:
    converter.sort(key=lambda p: p[1])

    outputs = ks.interval.Dis()
    for interval in intervals:
        print("interval", interval)
        # i = bs.bisect_left(converter, interval.l, key=lambda p: p[1] + p[2] - 1)
        # j = bs.bisect_right(converter, interval.r, key=lambda p: p[1])
        rem_left = interval.l
        for dest, left, width in converter:
            offset = dest - left
            right = left + width - 1
            print(left, right, offset)
            if right < rem_left:
                continue
            if rem_left > interval.r:
                break
            if left <= rem_left and right >= interval.r:
                print("hello?", rem_left, left)
                outputs.add(
                    ks.interval.Interval(rem_left + offset, interval.r + offset)
                )
                rem_left = right + 1
                continue
                # print([*outputs.intervals()])
                # should be done
            elif left <= rem_left and right < interval.r:
                print("x", rem_left, left)
                outputs.add(ks.interval.Interval(rem_left + offset, right + offset))
                rem_left = right + 1
                continue
            elif left > rem_left and right >= interval.r:
                if left > interval.r:
                    break
                outputs.add(ks.interval.Interval(rem_left, left - 1))
                outputs.add(ks.interval.Interval(left + offset, interval.r + offset))
                rem_left = right + 1
                # done
            elif left > rem_left and right < interval.r:
                print("yo")
                if left > interval.r:
                    break
                outputs.add(ks.interval.Interval(rem_left, left - 1))
                outputs.add(ks.interval.Interval(left + offset, right + offset))
                rem_left = right + 1
            else:
                assert False
        if rem_left <= interval.r:
            print("rem", rem_left)
            outputs.add(ks.interval.Interval(rem_left, interval.r))

    return [*outputs.intervals()]


@ks.func.min
def part1(stdin: typing.TextIO):
    seeds, ms = parse(stdin)
    for seed in seeds:
        for _, _, m in ms:
            seed = convert(m)(seed)
        yield seed


def part2(stdin: typing.TextIO):
    seeds, ms = parse(stdin)
    seeds = [*seeds]
    intervals: list[ks.interval.Interval] = []
    for a, b in ((seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)):
        intervals.append(ks.interval.Interval(a, a + b - 1))
    intervals.sort(key=lambda p: p.l)
    print(intervals)

    for _, _, conv in ms:
        intervals = convert_image(conv, intervals)
        print(intervals)
        pass

    return intervals[0].l
