# pyright: strict
from .. import ks
import typing

import math


def parse_row(prefix: str, stdin: typing.TextIO):
    return map(int, next(stdin).removeprefix(prefix).split())


def parse(stdin: typing.TextIO):
    return parse_row("Time:", stdin), parse_row("Distance:", stdin)


def join(parts: typing.Iterable[int]):
    return int("".join(map(str, parts)))


def solve(entries: typing.Iterable[tuple[int, int]]):
    for t, d in entries:
        # if I wait 𝑠:
        # (𝑡-𝑠) ⋅ 𝑠 > 𝑑
        # 𝑡𝑠-𝑠²-𝑑  > 0
        # 𝑠²-𝑡𝑠+𝑑 < 0
        # 𝑠 = 𝑡/2 ± √[(𝑡/2)² - 𝑑]
        mid = t / 2
        disc = math.sqrt(mid**2 - d)
        yield (math.floor(mid + disc) - math.ceil(mid - disc) + 1)


@ks.func.prod
def part1(stdin: typing.TextIO):
    return solve(zip(*parse(stdin)))


@ks.func.prod
def part2(stdin: typing.TextIO):
    return solve([(*map(join, parse(stdin)),)])
