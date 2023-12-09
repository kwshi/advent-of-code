from collections.abc import Callable, Iterable
import typing

import itertools as it
import functools as ft


def make(f: Callable[[int, list[int]], int]):
    def extrapolate(f: Callable[[int, list[int]], int], ns: Iterable[int]):
        diffs = [*ns]
        layers = [diffs]
        while any(diffs):
            layers.append(diffs := [b-a for a, b in it.pairwise(diffs)])
        layers.reverse()
        return ft.reduce(f, layers, 0)
    def solve(stdin: typing.TextIO):
        return sum(map(ft.partial(extrapolate, f), (map(int,line.split()) for line in stdin)))
    return solve

part1 = make(lambda p, l: p+l[-1])
part2 = make(lambda p, l: l[0]-p)
