# pyright: strict
import typing

from . import pattern


def line(stdin: typing.TextIO) -> str:
    return stdin.readline().rstrip("\r\n")


def line_pattern(stdin: typing.TextIO, p: str) -> typing.Iterator[typing.Any]:
    return pattern.compile(p)(line(stdin))


def lines(stdin: typing.TextIO, *, ignore_empty: bool = False) -> typing.Iterator[str]:
    """
    parse input line-by-line. returns a generator that yields individual lines.
    """
    for line in stdin:
        stripped = line.rstrip("\r\n")
        if ignore_empty and not stripped:
            continue
        yield stripped


def lines_pattern(
    stdin: typing.TextIO, p: str
) -> typing.Iterator[typing.Iterator[typing.Any]]:
    """
    parse input line-by-line. returns a generator that yields individual lines.
    """
    return map(pattern.compile(p), lines(stdin))


def chunks(stdin: typing.TextIO) -> typing.Iterator[list[str]]:
    chunk: list[str] = []
    for line in lines(stdin):
        if line:
            chunk.append(line)
            continue
        if chunk:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def scanf(pat: str, s: str) -> typing.Iterator[typing.Any]:
    return pattern.compile(pat)(s)
