# pyright: strict
from .. import ks
import typing


def parse(stdin: typing.TextIO):
    return [sum(map(int, chunk)) for chunk in ks.parse.chunks(stdin)]


def part1(stdin: typing.TextIO):
    return max(parse(stdin))


def part2(stdin: typing.TextIO):
    return sum(sorted(parse(stdin))[-3:])
