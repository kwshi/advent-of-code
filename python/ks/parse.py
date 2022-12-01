# pyright: strict
import sys
import typing


def lines() -> typing.Iterator[str]:
    """
    parse input line-by-line. returns a generator that yields individual lines.
    """
    for line in sys.stdin:
        yield line.rstrip("\r\n")


def chunks() -> typing.Iterator[list[str]]:
    chunk: list[str] = []
    for line in lines():
        if line:
            chunk.append(line)
            continue
        if chunk:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
