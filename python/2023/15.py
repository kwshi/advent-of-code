from .. import ks
import typing

import collections as co


def parse(stdin: typing.TextIO):
    return stdin.read().strip().split(",")


def haash(s: str):
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val %= 256
    return val


def part1(stdin: typing.TextIO):
    return sum(map(haash, parse(stdin)))


def part2(stdin: typing.TextIO):
    boxes: co.defaultdict[int, co.OrderedDict[str, int]] = co.defaultdict(
        co.OrderedDict
    )
    for p in parse(stdin):
        if p.endswith("-"):
            label = p.removesuffix("-")
            boxes[haash(label)].pop(label, None)
        else:
            label, n = p.split("=")
            boxes[haash(label)][label] = int(n)
    return sum(
        (b + 1) * (i + 1) * n
        for b, box in boxes.items()
        for i, n in enumerate(box.values())
    )
