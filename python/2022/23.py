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
    for i, row in enumerate(ks.parse.lines(stdin)):
        for j, cell in enumerate(row):
            if cell == "#":
                yield ks.coord.Coord(j, -i)


dir_n = ks.coord.Coord(0, 1)
dir_ne = ks.coord.Coord(1, 1)
dir_nw = ks.coord.Coord(-1, 1)
dir_s = ks.coord.Coord(0, -1)
dir_se = ks.coord.Coord(1, -1)
dir_sw = ks.coord.Coord(-1, -1)
dir_e = ks.coord.Coord(1, 0)
dir_w = ks.coord.Coord(-1, 0)

dirs_all = [
    dir_n,
    dir_ne,
    dir_nw,
    dir_s,
    dir_se,
    dir_sw,
    dir_e,
    dir_w,
]

consider = [
    (dir_n, [dir_n, dir_ne, dir_nw]),
    (dir_s, [dir_s, dir_se, dir_sw]),
    (dir_w, [dir_w, dir_nw, dir_sw]),
    (dir_e, [dir_e, dir_ne, dir_se]),
]


def empty(
    elves: set[ks.coord.Coord], elf: ks.coord.Coord, dirs: list[ks.coord.Coord]
) -> bool:
    return all(elf + d not in elves for d in dirs)


def step(elves: set[ks.coord.Coord], i: int) -> set[ks.coord.Coord] | None:
    target: dict[ks.coord.Coord, ks.coord.Coord] = {}
    count: co.defaultdict[ks.coord.Coord, int] = co.defaultdict(int)

    for elf in elves:
        if empty(elves, elf, dirs_all):
            continue
        for k in range(4):
            d, dirs = consider[(i + k) % len(consider)]
            if empty(elves, elf, dirs):
                count[elf + d] += 1
                target[elf] = elf + d
                break

    moves = {elf: t for elf, t in target.items() if count[t] < 2}
    return {moves.get(elf, elf) for elf in elves} if moves else None


def part1(stdin: typing.TextIO):
    elves = {*parse(stdin)}
    for i in range(10):
        elves_next = step(elves, i)
        if elves_next is None:
            break
        elves = elves_next

    xmin = min(e.x for e in elves)
    xmax = max(e.x for e in elves)
    ymin = min(e.y for e in elves)
    ymax = max(e.y for e in elves)
    return sum(
        ks.coord.Coord(x, y) not in elves
        for x, y in it.product(range(xmin, xmax + 1), range(ymin, ymax + 1))
    )


def part2(stdin: typing.TextIO):
    elves = {*parse(stdin)}
    for i in it.count():
        elves_next = step(elves, i)
        if elves_next is None:
            return i + 1
        elves = elves_next
