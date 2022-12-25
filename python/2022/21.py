# pyright: strict

from .. import ks
import typing

import functools as ft
import operator as op

import sympy as sp
import z3


ops: dict[str, typing.Callable[[float, float], float]] = {
    "+": op.add,
    "*": op.mul,
    "/": op.truediv,
    "-": op.sub,
}


def parse(stdin: typing.TextIO):
    for line in ks.parse.lines(stdin):
        key, expr = line.split(": ")
        match expr.split():
            case [a, o, b]:
                yield key, (ops[o], a, b)
            case [n]:
                yield key, int(n)
            case _:
                raise ValueError(f"failed to parse expr {expr!r}")


def part1(stdin: typing.TextIO):
    graph = dict(parse(stdin))

    @ft.cache
    def evaluate(key: str) -> float:
        match graph[key]:
            case int() as n:
                return n
            case (f, a, b):
                return f(evaluate(a), evaluate(b))

    return round(evaluate("root"))


def part2(stdin: typing.TextIO):
    return part2_sympy(stdin)


def part2_sympy(stdin: typing.TextIO):
    graph = dict(parse(stdin))

    @ft.cache
    def evaluate(key: str) -> typing.Any:  # because sympy expressions are untyped
        if key == "root":
            return

        if key == "humn":
            return sp.Symbol("humn")

        match graph[key]:
            case int() as n:
                return sp.Integer(n)
            case (f, a, b):
                return f(evaluate(a), evaluate(b))

    match graph["root"]:
        case (_, a, b):
            solutions: typing.Any = sp.solve(
                sp.Eq(evaluate(a), evaluate(b)), evaluate("humn")
            )
            return int(solutions.pop())

        case _:
            assert False


def part2_z3(stdin: typing.TextIO):
    graph = dict(parse(stdin))

    @ft.cache
    def evaluate(key: str) -> typing.Any:  # because sympy expressions are untyped
        if key == "root":
            return

        if key == "humn":
            return z3.Int("humn")

        match graph[key]:
            case int() as n:
                return z3.IntVal(n)
            case (f, a, b):
                return f(evaluate(a), evaluate(b))

    match graph["root"]:
        case (_, a, b):
            solver = z3.Solver()
            solver.add(evaluate(a) == evaluate(b))
            solver.check()
            return solver.model()[evaluate("humn")].as_long()

        case _:
            assert False
