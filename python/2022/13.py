# pyright: strict

from .. import ks
import typing

import functools as ft
import ast


Packet = int | list["Packet"]


# annoying `as` patterns everywhere because pyright doesn't narrow tuple sub-expression types:
# <https://github.com/microsoft/pyright/issues/4208#issuecomment-1348755433>
def compare(a: Packet, b: Packet) -> int:
    match a, b:
        case (int() as a, int() as b):
            return a - b

        case (int() as a, list() as b):
            return compare([a], b)

        case (list() as a, int() as b):
            return compare(a, [b])

        case (list() as a, list() as b):
            for x, y in zip(a, b):
                c = compare(x, y)
                if c != 0:
                    return c
            return len(a) - len(b)

        case _:
            # because pyright doesn't understand how tuple pattern-matching exhaustion works
            assert False


@ks.func.sumify
def part1(stdin: typing.TextIO):
    for i, chunk in enumerate(ks.parse.chunks(stdin)):
        a, b = map(ast.literal_eval, chunk)
        if compare(a, b) < 0:
            yield i + 1


def part2(stdin: typing.TextIO):
    things = [
        *map(ast.literal_eval, ks.parse.lines(stdin, ignore_empty=True)),
        [[2]],
        [[6]],
    ]
    things.sort(key=ft.cmp_to_key(compare))
    return (1 + things.index([[2]])) * (1 + things.index([[6]]))
