import sys
import itertools as it


def parse():
    return map(int, sys.stdin)


def part1():
    return sum(parse())


def part2():
    seen = set()
    for s in it.accumulate(it.cycle(map(int, sys.stdin))):
        if s in seen:
            return s
        seen.add(s)
