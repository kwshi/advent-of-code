from .. import ks
import typing


def parse(stdin: typing.TextIO):
    for line in ks.parse.lines(stdin):
        match line.split():
            case ["noop"]:
                yield None
            case ["addx", n]:
                yield int(n)


def run(program: typing.Iterable[int | None]) -> typing.Iterator[int]:
    x = 1
    for n in program:
        match n:
            case None:
                yield x
            case int():
                yield x
                yield x
                x += n


@ks.func.sumify
def part1(stdin: typing.TextIO):
    for i, x in enumerate(run(parse(stdin))):
        if i + 1 in {20, 60, 100, 140, 180, 220}:
            yield (i + 1) * x


def part2(stdin: typing.TextIO):
    image = ks.grid.from_constant(" ", 6, 40)
    for i, x in enumerate(run(parse(stdin))):
        row, col = i // 40, i % 40
        image[row, col] = " #"[abs(x - col) <= 1]
    image.render()
