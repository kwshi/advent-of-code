# pyright: strict

from .. import ks
import typing


digits = "012-="


def from_snafu(s: str) -> int:
    b = 0
    for c in s:
        b = b * 5 + digits.index(c)
    return b


def to_snafu(n: int) -> str:
    ds: list[str] = []
    while n:
        n, d = divmod(n, 5)
        n += d >= 3
        ds.append(digits[(d + 2) % 5 - 2])
    return "".join(reversed(ds))


def part1(stdin: typing.TextIO):
    return to_snafu(sum(map(from_snafu, ks.parse.lines(stdin))))
