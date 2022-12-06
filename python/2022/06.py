from .. import ks
import typing


def run(stdin: typing.TextIO, n: int):
    s = ks.parse.line(stdin)
    return n + next(i for i in range(len(s)) if len({*s[i : i + n]}) == n)


def part1(stdin: typing.TextIO):
    return run(stdin, 4)


def part2(stdin: typing.TextIO):
    return run(stdin, 14)
