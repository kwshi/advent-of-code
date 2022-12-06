# pyright: strict
from .. import ks
import typing


def parse(stdin: typing.TextIO):
    stack_lines, ins_lines = ks.parse.chunks(stdin)
    stack: list[list[str]] = [
        [] for _ in range(max(map(int, stack_lines.pop().strip().split())))
    ]
    for line in stack_lines:
        for s, item in zip(stack, line[1::4]):
            if item != " ":
                s.append(item)
    for s in stack:
        s.reverse()
    return stack, map(ks.parse.pattern.compile("move %u from %u to %u"), ins_lines)


def part1(stdin: typing.TextIO):
    stack, instructions = parse(stdin)
    for n, f, t in instructions:
        for _ in range(n):
            stack[t - 1].append(stack[f - 1].pop())
    return "".join(s.pop() for s in stack)


def part2(stdin: typing.TextIO):
    stack, instructions = parse(stdin)
    for n, f, t in instructions:
        stack[t - 1].extend(stack[f - 1][-n:])
        stack[f - 1][-n:] = []
    return "".join(s.pop() for s in stack)
