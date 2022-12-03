# pyright: strict
from .. import ks
import collections as co
import typing


def part1(stdin: typing.TextIO):
    twos = threes = 0
    for line in ks.parse.lines(stdin):
        counts = {*co.Counter(line.rstrip()).values()}
        twos += 2 in counts
        threes += 3 in counts
    return twos * threes


def part2(stdin: typing.TextIO):
    words = [*ks.parse.lines(stdin)]
    for i in range(len(words[0])):
        seen: set[str] = set()
        for word in words:
            chop = word[:i] + word[i + 1 :]
            if chop in seen:
                return chop
            seen.add(chop)
