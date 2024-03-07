"""
Symbolic expression-graph evaluator. Featured in:
- 2015 day 7
- 2022 day 21
"""

# pyright: strict
import typing

import math
import collections


def diff(args: int | typing.Iterable[int], *rest: int) -> int:
    match args:
        case int():
            return args - sum(rest)
        case _:
            i = iter(args)
            return next(i) - sum(i) - sum(rest)


def div(args: int | typing.Iterable[int], *rest: int) -> int:
    match args:
        case int():
            return args // math.prod(rest)
        case _:
            i = iter(args)
            return next(i) // math.prod(i) // math.prod(rest)


common_ops: dict[str, typing.Callable[[typing.Iterable[int]], int]] = {
    "+": sum,
    "*": math.prod,
    "-": diff,
    "/": div,
}


def eval_graph(
    expressions: dict[
        str,
        int
        | tuple[typing.Callable[[typing.Iterable[int]], int], tuple[str | int, ...]],
    ]
) -> dict[str, int]:

    result: dict[str, int] = {}

    deps: dict[str, set[str]] = collections.defaultdict(set)
    rev_deps: collections.defaultdict[str, set[str]] = collections.defaultdict(set)
    leaf: set[str] = {*expressions.keys()}
    for key, expr in expressions.items():

        if isinstance(expr, int):
            continue

        _, params = expr
        for param in params:
            if isinstance(param, int):
                continue
            deps[key].add(param)
            rev_deps[param].add(key)
            leaf.discard(key)

    while leaf:
        key = leaf.pop()
        for parent in rev_deps[key]:
            (d := deps[parent]).remove(key)
            if d:
                continue

            leaf.add(parent)
            match expressions[parent]:
                case int() as n:
                    result[parent] = n
                case (f, params):
                    result[parent] = f(
                        param if isinstance(param, int) else result[param]
                        for param in params
                    )

    return result
