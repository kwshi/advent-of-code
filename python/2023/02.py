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
class Game:
    id: int
    rounds: list[dict[str, int]]


def parse_line(line: str):
    match = re.fullmatch(r"Game (\d+): (.*)", line.strip())
    assert match, repr(line)
    id, parts = match.groups()
    rounds: list[dict[str, int]] = []
    for part in parts.split("; "):
        round: dict[str, int] = {}
        for batch in part.split(", "):
            n, color = batch.split()
            round[color] = int(n)
        rounds.append(round)
    return Game(int(id), rounds)


def parse(stdin: typing.TextIO):
    return map(parse_line, stdin)


def part1(stdin: typing.TextIO):
    limit = {"red": 12, "green": 13, "blue": 14}
    return sum(
        game.id
        for game in parse(stdin)
        if all(
            all(n <= limit[color] for color, n in round.items())
            for round in game.rounds
        )
    )


@ks.func.sum
def part2(stdin: typing.TextIO):
    for game in parse(stdin):
        bound: dict[str, int] = {}
        for round in game.rounds:
            for color, n in round.items():
                bound[color] = max(bound.get(color, 0), n)
        yield math.prod(bound.values())
