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
    for line in ks.parse.lines(stdin):
        a, b = line.split()
        yield a, int(b)


offset = {"L": (-1, 0), "R": (1, 0), "U": (0, 1), "D": (0, -1)}


def part1(stdin: typing.TextIO):
    hx, hy = 0, 0
    tx, ty = 0, 0
    seen = {(0, 0)}

    for d, n in parse(stdin):
        dx, dy = offset[d]
        # hx += n * dx
        # hy += n * dy
        for _ in range(n):
            hx += dx
            hy += dy
            while max(abs(tx - hx), abs(ty - hy)) > 1:
                if abs(tx - hx) > 0:
                    tx += 1 if hx > tx else -1
                if abs(ty - hy) > 0:
                    ty += 1 if hy > ty else -1
                seen.add((tx, ty))

    return len(seen)


def part2(stdin: typing.TextIO):
    rope = [(0, 0)] * 10
    seen = set()
    for d, n in parse(stdin):
        dx, dy = offset[d]
        for _ in range(n):
            hx, hy = rope[0]
            rope[0] = hx + dx, hy + dy

            for i in range(1, len(rope)):
                px, py = rope[i - 1]
                kx, ky = rope[i]
                while max(abs(kx - px), abs(ky - py)) > 1:
                    if abs(kx - px) > 0:
                        kx += 1 if px > kx else -1
                    if abs(ky - py) > 0:
                        ky += 1 if py > ky else -1
                rope[i] = kx, ky

            seen.add(rope[-1])

    return len(seen)

    pass
