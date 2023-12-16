from .. import ks
import typing

import math
import string
import re
import itertools as it
import bisect as bs
import functools as ft
import collections as co
import collections.abc as cabc
import operator as op
import dataclasses as dc
import heapq as hq
import pprint as pp
import graphlib as gl


def parse(stdin: typing.TextIO):
    pass


def part1(stdin: typing.TextIO):
    grid = ks.grid.read_chars(stdin)
    mirrors: dict[ks.P2, str] = {}
    for p in grid.keys0():
        if grid[p] != '.': mirrors[p] = grid[p]

    horiz: co.defaultdict[int, list[int]] = co.defaultdict(list)
    vert : co.defaultdict[int, list[int]]= co.defaultdict(list)
    for p in mirrors.keys():
        horiz[p.x].append(p.y)
        vert[p.y].append(p.x)
    for r in horiz.values(): r.sort()
    for r in vert.values(): r.sort()

    start = ( ks.P2(0, 0), ks.P2(0, 1))
    seen = {start}
    frontier = [start]
    while frontier:
        parent, pdir = frontier.pop()
        print(parent)
        next = parent + pdir
        if not (0 <= next.x < grid.size0 and 0 <= next.y < grid.size1):
            continue
        c = grid[next]
        children: list[tuple[ks.P2, ks.P2]] = []
        if c == '.' or (pdir.x == 0 and c == '-') or (pdir.y == 0 and c == '|'):
            # pass through
            children.append((next, pdir))
        elif (pdir.x == 0 and c == '|'):
            children.append((next, ks.P2(-1, 0)))
            children.append((next, ks.P2(1, 0)))
        elif (pdir.y == 0 and c == '-'):
            children.append((next, ks.P2(0, -1)))
            children.append((next, ks.P2(0, 1)))
        else:
            assert c in '/\\', c
            cdir = ks.P2(pdir.y, pdir.x) if c == '\\' else ks.P2(-pdir.y,-pdir.x)
            children.append((next, cdir))
        for child in children:
            assert child not in seen
            if child in seen:
                continue
            seen.add(child)
            frontier.append(child)
        #if len(seen) == 20: break
    return len({p for p, _ in seen})

def part2(stdin: typing.TextIO):
    pass
