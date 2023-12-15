import typing

import functools as ft
import collections.abc as cabc

type Entry = tuple[str, list[int]]


def parse(stdin: typing.TextIO) -> cabc.Iterator[Entry]:
    for line in stdin:
        left, right = line.strip().split()
        yield left, [*map(int, right.split(","))]


def count(template: str, blocks: list[int]):
    @ft.lru_cache(None)
    def go(t: int, b: int) -> int:
        # calculates number of ways to arrange `blocks[b:]` within `template[t:]`

        if b == len(blocks):
            return {*template[t:]} <= {".", "?"}

        block = blocks[b]
        total = 0

        # start after the first gap…
        start = template.replace("?", "#").find("#", t)
        if start == -1:
            # no spots left
            return 0

        # …move no further than the first `#`…
        pin = template.find("#", start)
        if pin == -1:
            pin = len(template)

        # …and end before the wall
        end = min(pin, len(template) - block)

        for place in range(start, end + 1):
            # check: is this a valid placement?
            if not (
                {*template[place : place + block]} <= {"#", "?"}
                and (place + block == len(template) or template[place + block] != "#")
            ):
                continue
            total += go(place + block + 1, b + 1)

        return total

    return go(0, 0)


def solver(preprocess: cabc.Callable[[Entry], Entry]):
    def solve(stdin: typing.TextIO):
        return sum(count(*preprocess(p)) for p in parse(stdin))

    return solve


part1 = solver(lambda p: p)
part2 = solver(lambda p: ("?".join([p[0]] * 5), p[1] * 5))


# BELOW: old, slow brute-force code for testing
def count_slow(template: str, blocks: list[int]):
    return sum(
        validate(template, make(len(template), blocks, pos))
        for pos in generate(template, len(template), blocks)
    )


def generate(
    template: str, total: int, pattern: list[int], start: int = 0
) -> typing.Iterable[list[int]]:
    match pattern:
        case []:
            if not ({*template[start:]} <= {"?", "."}):
                # no chunks left, but template requires some
                return
            yield []
        case [first, *rest]:
            # not enough slots
            if sum(t in "#?" for t in template[start:]) < sum(rest) + first:
                return

            gap = sum(rest) + len(rest)
            # k+first is at most total-gap
            for k in range(start, total - gap - first + 1):
                # try starting position k. is it even possible?
                if not (
                    all(template[k + i] in "#?" for i in range(first))
                    and (k + first == total or template[k + first] in ".?")
                ):
                    continue

                for p in generate(template, total, rest, k + first + 1):
                    yield [k, *p]

                # if position k has '#', cannot start after k.
                if template[k] == "#":
                    break


def make(width: int, pattern: list[int], pos: list[int]):
    fill = [False] * width
    for p, q in zip(pattern, pos):
        for i in range(p):
            fill[q + i] = True
    return fill


def render(fill: list[bool]):
    return "".join(".#"[f] for f in fill)


def validate(template: str, fill: list[bool]):
    return all(t == "?" or (t == "#") == f for t, f in zip(template, fill))
