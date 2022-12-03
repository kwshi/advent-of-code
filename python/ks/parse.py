# pyright: strict
import typing


def line(stdin: typing.TextIO) -> str:
    return stdin.readline().rstrip("\r\n")


def lines(stdin: typing.TextIO) -> typing.Iterator[str]:
    """
    parse input line-by-line. returns a generator that yields individual lines.
    """
    for line in stdin:
        yield line.rstrip("\r\n")


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
