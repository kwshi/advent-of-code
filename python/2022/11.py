# pyright: strict
from .. import ks
import typing

import math
import operator as op
import dataclasses as dc
import heapq as hq

operators = {"*": op.mul, "+": op.add}


@dc.dataclass(kw_only=True)
class Monkey:
    items: list[int]
    operate: typing.Callable[[int], int]
    test: int
    true: int
    false: int
    count: int


def parse_expr(s: str):
    a, o, b = s.split()

    def evaluate(old: int):
        return operators[o](
            old if a == "old" else int(a), old if b == "old" else int(b)
        )

    return evaluate


@ks.func.listify
def parse(stdin: typing.TextIO):
    for i, chunk in enumerate(ks.parse.chunks(stdin)):
        monkey, starting, operation, test, true, false = chunk
        assert monkey == f"Monkey {i}:"
        yield Monkey(
            items=[*map(int, starting.removeprefix("  Starting items: ").split(", "))],
            operate=parse_expr(operation.removeprefix("  Operation: new = ")),
            test=int(test.removeprefix("  Test: divisible by ")),
            true=int(true.removeprefix("    If true: throw to monkey ")),
            false=int(false.removeprefix("    If false: throw to monkey ")),
            count=0,
        )


def run(monkeys: list[Monkey], n: int, adjust: typing.Callable[[int], int]):
    for _ in range(n):
        for m in monkeys:
            for item in m.items:
                new = adjust(m.operate(item))
                monkeys[m.true if new % m.test == 0 else m.false].items.append(new)
            m.count += len(m.items)
            m.items = []
    return math.prod(hq.nlargest(2, (m.count for m in monkeys)))


def part1(stdin: typing.TextIO):
    monkeys = parse(stdin)
    return run(monkeys, 20, lambda n: n // 3)


def part2(stdin: typing.TextIO):
    monkeys = parse(stdin)
    p = math.prod(m.test for m in monkeys)
    return run(monkeys, 10000, lambda n: n % p)
