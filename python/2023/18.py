from .. import ks
import typing

import itertools as it
import re


directions = [ks.P2().east, ks.P2().south, ks.P2().west, ks.P2().north]


def parse(stdin: typing.TextIO):
    for line in stdin:
        match = re.match(r"([RDLU]) (\d+) \(#(.*)\)", line.strip())
        assert match, line
        direction, count, color = match.groups()
        hex = int(color, 16)
        yield (  # part 1, part 2
            directions["RDLU".index(direction)] * int(count),
            directions[hex % 16] * (hex // 16),
        )


def part(index: typing.Literal[0, 1]):
    def solve(stdin: typing.TextIO):
        points = [*it.accumulate((p[index] for p in parse(stdin)))]

        s = b = 0
        for i in range(len(points)):
            p, q = points[i], points[(i + 1) % len(points)]
            s += p.cross(q)
            b += (p - q).norm1
        return abs(s) // 2 + b // 2 + 1

    return solve


part1 = part(0)
part2 = part(1)
