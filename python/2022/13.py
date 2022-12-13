from .. import ks
import typing

import functools as ft


def parse(stdin: typing.TextIO):
    for a, b in ks.parse.chunks(stdin):
        yield eval(a), eval(b)


def compare(a, b):
    match (a, b):
        case (int(), int()):
            return a - b

        case (int(), list()):
            return compare([a], b)

        case (list(), int()):
            return compare(a, [b])

        case (list(), list()):
            for x, y in zip(a, b):
                c = compare(x, y)
                if c == 0:
                    continue
                return c
            return len(a) - len(b)


@ks.func.sumify
def part1(stdin: typing.TextIO):
    for i, (a, b) in enumerate(parse(stdin)):
        if compare(a, b) < 0:
            yield i + 1


def part2(stdin: typing.TextIO):
    things = []
    for line in ks.parse.lines(stdin):
        if not line:
            continue
        things.append(eval(line))
    things.append([[2]])
    things.append([[6]])

    things.sort(key=ft.cmp_to_key(compare))
    return (1 + things.index([[2]])) * (1 + things.index([[6]]))
