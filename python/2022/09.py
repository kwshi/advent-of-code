# pyright: strict
from .. import ks
import typing

offset: dict[str, tuple[int, int]] = {
    "L": (-1, 0),
    "R": (1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def advance(a: ks.coord.Coord, b: ks.coord.Coord) -> ks.coord.Coord:
    return a if a.dist_max(b) <= 1 else a + (b - a).sign()


def solve(l: int) -> typing.Callable[[typing.TextIO], int]:
    @ks.func.count_unique
    def run(stdin: typing.TextIO) -> typing.Iterator[ks.coord.Coord]:
        rope = [ks.coord.Coord()] * l
        for d, n in ks.parse.lines_pattern(stdin, "%s %d"):
            for _ in range(n):
                rope[0] += offset[d]
                for i in range(l - 1):
                    rope[i + 1] = advance(rope[i + 1], rope[i])
                yield rope[-1]

    return run


part1 = solve(2)
part2 = solve(10)
