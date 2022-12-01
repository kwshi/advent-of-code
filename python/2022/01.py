# pyright: strict
from .. import ks


def parse():
    return [sum(map(int, chunk)) for chunk in ks.parse.chunks()]


def part1():
    return max(parse())


def part2():
    return sum(sorted(parse())[-3:])
