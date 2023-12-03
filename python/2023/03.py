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


@dc.dataclass
class ParseResult:
    symbols: dict[tuple[int, int], str]
    touches: dict[tuple[int, int], set[tuple[int, int]]]
    numbers: dict[tuple[int, int], int]
    resolve: dict[tuple[int, int], tuple[int, int]]


def parse(stdin: typing.TextIO):
    grid = {
        (i, j): c for i, row in enumerate(stdin) for j, c in enumerate(row.rstrip())
    }
    digits: set[tuple[int, int]] = set()
    symbols: dict[tuple[int, int], str] = {}
    for p, c in grid.items():
        if c.isnumeric():
            digits.add(p)
        elif c != ".":
            symbols[p] = c

    succ: dict[tuple[int, int], tuple[int, int] | None] = {p: None for p in digits}
    roots = {*digits}
    for i, j in digits:
        if (i, j + 1) in digits:
            succ[i, j] = (i, j + 1)
            roots.remove((i, j + 1))

    numbers: dict[tuple[int, int], int] = {}
    resolve: dict[tuple[int, int], tuple[int, int]] = {}
    for root in roots:
        val = 0
        node = root
        while node is not None:
            resolve[node] = root
            val = val * 10 + int(grid[node])
            node = succ[node]
        numbers[root] = val

    touches: dict[tuple[int, int], set[tuple[int, int]]] = {}
    for i, j in symbols:
        s = touches[i, j] = set()
        for di, dj in it.product([-1, 0, 1], repeat=2):
            p = resolve.get((i + di, j + dj))
            if p is not None:
                s.add(p)

    return ParseResult(symbols, touches, numbers, resolve)


def part1(stdin: typing.TextIO):
    result = parse(stdin)
    parts = set().union(*result.touches.values())
    return sum(result.numbers[p] for p in parts)


def part2(stdin: typing.TextIO):
    result = parse(stdin)
    return sum(
        math.prod(result.numbers[q] for q in v)
        for p, v in result.touches.items()
        if result.symbols[p] == "*" and len(v) == 2
    )
