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

pipes = {
    "L": {ks.P2().north, ks.P2().west},
    "F": {ks.P2().north, ks.P2().east},
    "J": {ks.P2().south, ks.P2().west},
    "7": {ks.P2().south, ks.P2().east},
    "|": {ks.P2().west, ks.P2().east},
    "-": {ks.P2().north, ks.P2().south},
}


def walk(grid: ks.Grid[str], start: ks.P2, direction: ks.P2):
    here = start + direction
    if here not in grid:
        return
    ends = pipes.get(grid[here])
    if ends is None or -direction not in ends:
        return

    direction = (ends - {-direction}).pop()
    steps = [start]
    while True:
        steps.append(here)
        here += direction
        if here == start:
            return steps
        direction = (pipes[grid[here]] - {-direction}).pop()


def parse(stdin: typing.TextIO):
    grid = ks.grid.from_lines(stdin)
    start = grid.find("S")
    assert start is not None

    for direction in ks.P2().circ1(1):
        path = walk(grid, start, direction)
        if path is not None:
            return path

    assert False, "no loop found"


def part1(stdin: typing.TextIO):
    return len(parse(stdin)) // 2


def part2(stdin: typing.TextIO):
    path = parse(stdin)
    s = 0
    for i, p in enumerate(path):
        q = path[(i + 1) % len(path)]
        s += p.cross(q)
    return (abs(s) - len(path)) // 2 + 1
