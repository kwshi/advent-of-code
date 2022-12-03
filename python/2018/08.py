# pyright: strict
from .. import ks
import typing

import dataclasses as dc


@dc.dataclass
class Node:
    children: list[typing.Self]
    metadata: list[int]


def consume(nums: typing.Iterator[int]):
    c, m = next(nums), next(nums)
    return Node(
        children=[consume(nums) for _ in range(c)],
        metadata=[next(nums) for _ in range(m)],
    )


def parse(stdin: typing.TextIO):
    return consume(map(int, ks.parse.line(stdin).split()))


def total(node: Node):
    return sum(node.metadata) + sum(map(total, node.children))


def value(node: Node) -> int:
    return (
        sum(
            value(node.children[m - 1])
            for m in node.metadata
            if 1 <= m <= len(node.children)
        )
        if node.children
        else sum(node.metadata)
    )


def part1(stdin: typing.TextIO):
    return total(parse(stdin))


def part2(stdin: typing.TextIO):
    return value(parse(stdin))
