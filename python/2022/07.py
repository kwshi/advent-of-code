# pyright: strict
from .. import ks
import typing


def parse(stdin: typing.TextIO):
    sizes: dict[tuple[str, ...], int] = {(): 0}
    here: list[str] = []
    for line in ks.parse.lines(stdin):
        match line.split():
            case ["$", "cd", "/"]:
                here = []
            case ["$", "cd", ".."]:
                here.pop()
            case ["$", "cd", d]:
                here.append(d)
            case ["$", "ls"]:
                pass
            case ["dir", d]:
                sizes[*here, d] = 0
            case [n, _]:
                for i in range(len(here) + 1):
                    sizes[*here[:i]] += int(n)
            case _:
                assert False, f"unrecognized command {line}"
    return sizes


def part1(stdin: typing.TextIO):
    return sum(v for v in parse(stdin).values() if v <= 100000)


def part2(stdin: typing.TextIO):
    sizes = parse(stdin)
    free = 70000000 - sizes[()]
    return min(v for v in sizes.values() if v + free >= 30000000)
