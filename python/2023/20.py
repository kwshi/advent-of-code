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

type ModuleType = typing.Literal['broadcaster', '&', '%']

@dc.dataclass
class Module:
    type: ModuleType|None
    name: str
    dests: list[str]
    inputs: list[str]

@dc.dataclass
class Pulse:
    src: str
    dest: str
    value: bool

@dc.dataclass
class State:
    output: bool
    inputs: dict[str, bool]

def parse(stdin: typing.TextIO):
    modules = dict[str, Module]()
    for line in stdin:
        key, dests = line.rstrip().split(' -> ')
        dests = dests.split(', ')
        for mtype in ('broadcaster', '&', '%'):
            if key.startswith(mtype):
                name = key.removeprefix(mtype)
                modules[name] = Module(mtype, name, dests, [])
                break
        else:
            raise ValueError(f'unrecognized module key {key}')

    blanks = set[str]()
    for module in modules.values():
        for dest in module.dests:
            if dest in modules: continue
            blanks.add(dest)
    for name in blanks:
            modules[name] = Module(None, name, [], [])

    for module in modules.values():
        for dest in module.dests:
            if dest not in modules: continue
            modules[dest].inputs.append(module.name)

    return modules

def press(modules: dict[str, Module], state: dict[str, State]):
    pulses = co.deque([Pulse('', '', False)])
    while pulses:
        pulse = pulses.popleft()
        yield pulse

        module = modules[pulse.dest]
        st = state[module.name]
        match module.type:
            case 'broadcaster'|None:
                value = pulse.value
            case '&':
                st.inputs[pulse.src] = pulse.value
                value = not all(st.inputs.values())
            case '%':
                if pulse.value: continue
                value = not state[module.name].output
        st.output = value

        for dest in module.dests:
            pulses.append(Pulse(module.name, dest, value))



def part1(stdin: typing.TextIO):
    modules = parse(stdin)
    state = {module.name: State(False, {inp: False for inp in module.inputs}) for module in modules.values()}

    low = high = 0
    for _ in range(1000):
        for pulse in press(modules, state):
            if pulse.value: high += 1
            else: low += 1

    return low * high



def part2(stdin: typing.TextIO):
    pass
