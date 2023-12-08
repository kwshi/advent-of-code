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

@dc.dataclass(frozen=True)
class Room:
    left: str
    right: str

    def __getitem__(self, key:typing.Literal['L','R']):
        match key:
            case 'L': return self.left
            case 'R': return self.right

@dc.dataclass
class Cycle:
    start: int
    size: int
    ends: dict[int, int]




def parse(stdin: typing.TextIO):
    moves, rules = stdin.read().strip().split('\n\n')
    rs: dict[str, Room] = {}
    for rule in rules.split('\n'):
        lhs, right = rule.split(' = ')
        l, r = right.strip('()').split(', ')
        rs[lhs] = (Room(l, r))
    return moves, rs

@ks.func.sum
def part1(stdin: typing.TextIO):
    start = 'AAA'
    moves, rules = parse(stdin)
    for move in it.cycle(moves):
        match move:
            case 'L':
                start = rules[start].left
            case 'R':
                start = rules[start].right
        yield 1
        if start == 'ZZZ':
            break



@ks.func.sum
def part2_old(stdin: typing.TextIO):
    moves, rules = parse(stdin)
    states = {k for k in rules if k.endswith('A')}
    for move in it.cycle(moves):
        match move:
            case 'L':
                states = {rules[k].left for k in states}
            case 'R':
                states = {rules[k].right for k in states}
        yield 1
        if all(k.endswith('Z') for k in states):
            break




def part2(stdin: typing.TextIO):
    def find_cycle(start: str):
        # other pyright issue from yesterday: 'a, b, c'.split(', ').index(x) LiteralString and str
        # pyright issue: try removing type annotation on seen
        state: tuple[str, int] = (start, 0)
        seen: dict[tuple[str, int], int] = {state: 0}
        ends: dict[int, int] = {}
        for step in it.count(1):
            key, index = state
            key, index = state = rooms[key][typing.cast(typing.Literal['L','R'],moves[index])], (index+1)%len(moves)
            if state in seen:
                return Cycle(seen[state], step - seen[state], ends)
            seen[state] = step
            if key.endswith('Z'):
                ends[step] = index
        assert False

    moves, rooms = parse(stdin)
    cycles = {k: find_cycle(k) for k in rooms if k.endswith('A')}
    pp.pprint(cycles)
    sizes = [c.size for c in cycles.values()]

    # this works because of a _pure_ coincidence: that for each starting room, the step at which we first encounter an end room is exactly the size of the cycle, and the cycle begins at that ending room, and the cycle contains _only_ that one ending room. meaning, an end room is hit _exactly_ at multiples of the cycle size.
    return math.lcm(*sizes)
