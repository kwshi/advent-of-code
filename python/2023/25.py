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
    graph = co.defaultdict[str, set[str]](set)
    for line in stdin:
        src, dests = line.split(": ")
        for dest in dests.strip().split():
            graph[src].add(dest)
            graph[dest].add(src)
    return graph


def edges(graph: dict[str, set[str]]):
    for p, es in graph.items():
        for q in es:
            if p < q:
                yield p, q


def dfs(
    graph: dict[str, set[str]], flow: dict[tuple[str, str], int], src: str, sink: str
):
    frontier = [src]
    seen: dict[str, str | None] = {src: None}
    while frontier:
        current = frontier.pop()
        for p in graph[current]:
            if flow[current, p] == 1:
                continue
            if p in seen:
                continue
            seen[p] = current
            if p == sink:
                path = list[str]()
                while p is not None:
                    path.append(p)
                    p = seen[p]
                return path[::-1]
            frontier.append(p)


def flow(graph: dict[str, set[str]], src: str, sink: str):
    flow = {e: 0 for e in edges(graph)} | {(q, p): 0 for p, q in edges(graph)}
    while (path := dfs(graph, flow, src, sink)) is not None:
        print(path)
        for p, q in it.pairwise(path):
            assert flow[p, q] in {-1, 0}
            assert flow[q, p] == -flow[p, q]
            flow[p, q] += 1
            flow[q, p] -= 1

    return flow


def part1(stdin: typing.TextIO):
    graph = parse(stdin)
    es = {(min(p, q), max(p, q)) for p, q in it.combinations(graph.keys(), 2)} - {
        *edges(graph)
    }
    assert es
    src, sink = es.pop()
    f = flow(graph, src, sink)

    frontier = [src]
    seen = {src}
    while frontier:
        current = frontier.pop()
        for p in graph[current]:
            if f[current, p] == 1:
                continue
            if p in seen:
                continue
            seen.add(p)
            frontier.append(p)

    print(len(seen), len(graph.keys() - seen))
    return len(seen) * len(graph.keys() - seen)


def part2(stdin: typing.TextIO):
    return "hi"
