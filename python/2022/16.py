# pyright: strict

from .. import ks
import typing

import itertools as it
import collections as co


def parse(stdin: typing.TextIO):
    graph: co.defaultdict[str, list[str]] = co.defaultdict(list)
    rates: dict[str, int] = {}

    for valve, rate, tunnels in ks.parse.lines_regexp(
        stdin, r"Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
    ):
        rates[valve] = int(rate)
        graph[valve].extend(tunnels.split(", "))

    dists: dict[tuple[str, str], int] = {}
    for start in graph.keys():
        front = co.deque([start])
        dists[start, start] = 0
        while front:
            parent = front.popleft()
            d = dists[start, parent] + 1
            for child in graph[parent]:
                if (start, child) in dists:
                    continue
                dists[start, child] = d
                front.append(child)

    return dists, rates


def dp(
    dists: dict[tuple[str, str], int],
    rates: dict[str, int],
    total: int,
):
    best: dict[tuple[frozenset[str], str, int], int] = {}
    nonzero = {k for k, r in rates.items() if r}

    for valve in nonzero:
        time = total - dists["AA", valve] - 1
        if time >= 0:
            best[frozenset([valve]), valve, time] = rates[valve] * time

    return best


def search(
    dists: dict[tuple[str, str], int],
    rates: dict[str, int],
    total: int,
):
    nonzero = {k for k, r in rates.items() if r}

    def go(
        path: frozenset[str],
        last: str,
        time: int,
        gains: int,
    ) -> typing.Iterator[tuple[frozenset[str], int]]:
        yield path, gains
        for unvisited in nonzero - path:
            t = time - dists[last, unvisited] - 1
            if t < 0:
                continue
            yield from go(
                path | {unvisited}, unvisited, t, gains + t * rates[unvisited]
            )

    best: dict[frozenset[str], int] = {}
    for seen, gains in go(frozenset([]), "AA", total, 0):
        best[seen] = max(best.get(seen, 0), gains)

    return best


def part1(stdin: typing.TextIO):
    dists, rates = parse(stdin)
    return max(search(dists, rates, 30).values())


def part2(stdin: typing.TextIO):
    dists, rates = parse(stdin)
    best = search(dists, rates, 26)
    return max(
        best[s1] + best[s2]
        for s1, s2 in it.product(best.keys(), repeat=2)
        if s1.isdisjoint(s2)
    )
