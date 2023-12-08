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

    #def find_cycle(start: str):
    #    # other pyright issue from yesterday: 'a, b, c'.split(', ').index(x) LiteralString and str
    #    # pyright issue: try removing type annotation on seen
    #    state: tuple[str, int] = (start, 0)
    #    seen: dict[tuple[str, int], int] = {state: 0}
    #    ends: dict[int, int] = {}
    #    for step in it.count(1):
    #        key, index = state
    #        key, index = state = rules[key][typing.cast(typing.Literal['L','R'],moves[index])], (index+1)%len(moves)
    #        if state in seen:
    #            return Cycle(seen[state], step - seen[state], ends)
    #        seen[state] = step
    #        if key.endswith('Z'):
    #            ends[step] = index
    #    assert False

    def simplify(rules: dict[str, Room]):
        bins: co.defaultdict[Room, set[str]] = co.defaultdict(set)
        for k, room in rules.items():
            bins[room].add(k)
        rewrite: dict[str, str] = {}
        final = True
        for bin in bins.values():
            canonical = min(bin)
            for room in bin: rewrite[room] = canonical
            final &= len(bin) == 1
        #pp.pprint(bins)
        #pp.pprint(rewrite)
        return {rewrite[k]: Room(rewrite[room.left], rewrite[room.right]) for k, room in rules.items()}, final




    moves, rooms = parse(stdin)
    print(len({k for k in rooms if k.endswith('A')}))

    #print()

    #print(len(rules))

    #done = False
    #while not done:
    #    rules, done = simplify(rules)
    #
    #pp.pprint(len(rules))

    #bins: co.defaultdict[Room, set[str]] = co.defaultdict(set)
    #for k, room in rules.items():
    #    bins[room].add(k)
    #rewrite: dict[str, str] = {}
    #for bin in bins.values():
    #    canonical = min(bin)
    #    for room in bin: rewrite[room] = canonical
    #new = {rewrite[k]: Room(rewrite[room.left], rewrite[room.right]) for k, room in rules.items()}
    #print(len(new), len(rules))

    #cycles = {k: find_cycle(k) for k in rules if k.endswith('A')}

    #"""
    #find min s such that

    #s in ends1' ∩ ends2'

    #where ends' defined as
    #{for n in ends where n≥start: n + cyclesize * k}

    #s mod cyclesize = n
    #"""


