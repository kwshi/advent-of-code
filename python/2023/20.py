from .. import ks
import typing
import collections.abc as cabc

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

type ModuleType = typing.Literal["broadcaster", "&", "%"]


@dc.dataclass
class Module:
    type: ModuleType | None
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
        key, dests = line.rstrip().split(" -> ")
        dests = dests.split(", ")
        for mtype in ("broadcaster", "&", "%"):
            if key.startswith(mtype):
                name = key.removeprefix(mtype)
                modules[name] = Module(mtype, name, dests, [])
                break
        else:
            raise ValueError(f"unrecognized module key {key}")

    blanks = set[str]()
    for module in modules.values():
        for dest in module.dests:
            if dest in modules:
                continue
            blanks.add(dest)
    for name in blanks:
        modules[name] = Module(None, name, [], [])

    for module in modules.values():
        for dest in module.dests:
            if dest not in modules:
                continue
            modules[dest].inputs.append(module.name)

    return modules


def press(
    modules: dict[str, Module],
    state: dict[str, State],
    init: Pulse = Pulse("", "", False),
):
    pulses = co.deque([init])
    while pulses:
        pulse = pulses.popleft()
        yield pulse

        module = modules[pulse.dest]
        st = state[module.name]
        match module.type:
            case "broadcaster" | None:
                value = pulse.value
            case "&":
                st.inputs[pulse.src] = pulse.value
                value = not all(st.inputs.values())
            case "%":
                if pulse.value:
                    continue
                value = not state[module.name].output
        st.output = value

        for dest in module.dests:
            pulses.append(Pulse(module.name, dest, value))


def init(modules: dict[str, Module]):
    return {
        module.name: State(False, {inp: False for inp in module.inputs})
        for module in modules.values()
    }


def part1(stdin: typing.TextIO):
    modules = parse(stdin)
    state = {
        module.name: State(False, {inp: False for inp in module.inputs})
        for module in modules.values()
    }

    counts = [0, 0]
    for _ in range(1000):
        for pulse in press(modules, state):
            counts[int(pulse.value)] += 1
    return math.prod(counts)


def deserialize(modules: dict[str, Module], order: list[str], values: tuple[bool, ...]):
    values_lookup = dict(zip(order, values))
    values_lookup[""] = False
    return {
        k: State(v, {i: values_lookup[i] for i in modules[k].inputs})
        for k, v in values_lookup.items()
    }


def serialize(modules: dict[str, Module], state: dict[str, State]):
    order = sorted(k for k in state if modules[k].type == "%")
    return tuple(state[k].output for k in order)


def part2(stdin: typing.TextIO):
    modules = parse(stdin)

    def search_dests(start: str, exclude_end: str):
        seen = {start}
        frontier = [start]
        while frontier:
            current = frontier.pop()
            for next in modules[current].dests:
                if next in seen or next == exclude_end:
                    continue
                seen.add(next)
                frontier.append(next)
        return seen

    def extract(start: str, merge_end: str):
        keys = search_dests(start, merge_end)
        submodules = {k: modules[k] for k in keys}
        submodules[""] = Module("broadcaster", "", [start], [])
        out = keys & {*modules[merge_end].inputs}
        assert len(out) == 1
        submodules[merge_end] = Module(None, merge_end, [], [*out])
        return submodules

    branches = {k: search_dests(k, "rx") for k in modules[""].dests}
    for k in branches.keys():
        module = modules[k]
        print(k, module)
        assert module.type == "%"
    for (a, x), (b, y) in it.combinations(branches.items(), 2):
        print(a, b, x & y)
        assert x & y == {"dn"}
    assert modules["dn"].type == "&"

    branches = {k: extract(k, "dn") for k in modules[""].dests}
    times = dict[str, int]()
    for start, branch in branches.items():
        print("evaluating", start)

        state = init(branch)
        history = {serialize(branch, state): 0}
        time = 0
        while True:
            activate = False
            for pulse in press(branch, state):
                if pulse.dest == "dn" and pulse.value:
                    activate = True
            time += 1
            snapshot = serialize(branch, state)
            if activate:
                print("activate", time)
            if snapshot in history:
                break
            history[snapshot] = time
        print(snapshot, time)
        assert history[snapshot] == 0
        times[start] = time
    return math.lcm(*times.values())
