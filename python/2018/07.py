# pyright: strict
from .. import ks
import typing

import string
import re
import collections as co
import heapq as hq
import graphlib as gl

re_order = re.compile(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin\.")


worker_count = 5
cost_offset = 60

cost = {c: i + 1 + cost_offset for i, c in enumerate(string.ascii_uppercase)}

Graph = co.defaultdict[str, set[str]]


def parse(stdin: typing.TextIO):
    forward: Graph = co.defaultdict(set)
    backward: Graph = co.defaultdict(set)
    for line in ks.parse.lines(stdin):
        match = re_order.fullmatch(line)
        assert match is not None, line
        prereq, step = match.groups()

        forward[prereq].add(step)
        backward[step].add(prereq)

    return forward, backward


def fulfill(forward: Graph, backward: Graph, task: str):
    for desc in forward[task]:
        (preds := backward[desc]).remove(task)
        if not preds:
            yield desc


def part1(stdin: typing.TextIO):
    forward, backward = parse(stdin)

    order: list[str] = []
    free = [*(forward.keys() - backward.keys())]
    hq.heapify(free)
    while free:
        top = hq.heappop(free)
        order.append(top)
        for freed in fulfill(forward, backward, top):
            hq.heappush(free, freed)

    return "".join(order)


def part2(stdin: typing.TextIO):
    forward, backward = parse(stdin)

    time = 0
    workers: list[tuple[int, str]] = []
    todo = [*(forward.keys() - backward.keys())]
    hq.heapify(todo)
    while todo or workers:
        while len(workers) < worker_count and todo:
            task = hq.heappop(todo)
            hq.heappush(workers, (time + cost[task], task))

        time, task = hq.heappop(workers)
        for freed in fulfill(forward, backward, task):
            hq.heappush(todo, freed)

    return time


def part1_alt(stdin: typing.TextIO):
    _, backward = parse(stdin)

    order: list[str] = []
    ts = gl.TopologicalSorter(backward)
    ts.prepare()
    queue: list[str] = []
    while ts:
        for r in ts.get_ready():
            hq.heappush(queue, r)
        ready = hq.heappop(queue)
        order.append(ready)
        ts.done(ready)

    return "".join(order)


def part2_alt(stdin: typing.TextIO):
    _, backward = parse(stdin)

    ts = gl.TopologicalSorter(backward)
    ts.prepare()
    time = 0
    workers: list[tuple[int, str]] = []
    todo: list[str] = []
    while ts or todo or workers:
        for r in ts.get_ready():
            hq.heappush(todo, r)
        while len(workers) < worker_count and todo:
            task = hq.heappop(todo)
            hq.heappush(workers, (time + cost[task], task))

        time, task = hq.heappop(workers)
        ts.done(task)

    return time
