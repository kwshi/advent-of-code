# pyright: strict

from .. import ks
import typing
import string


def reactive(a: str, b: str):
    return a.lower() == b.lower() and a != b


def react(s: str):
    deletes: list[tuple[int, int]] = [(0, 0)]
    i = 1
    while i < len(s):

        j = k = i
        while 0 <= j - 1 and k + 1 <= len(s) and reactive(s[j - 1], s[k]):
            last_start, last_end = deletes[-1]
            j -= 1
            k += 1
            if j == last_end:
                deletes.pop()
                j = last_start

        if j == k:
            i += 1
            continue

        deletes.append((j, k))
        i = k + 1

    last = 0
    buf: list[str] = []
    for j, k in deletes:
        buf.append(s[last:j])
        last = k
    buf.append(s[last:])
    return "".join(buf)


def part1(stdin: typing.TextIO):
    return len(react(ks.parse.line(stdin)))


def part2(stdin: typing.TextIO):
    seq = ks.parse.line(stdin)
    return min(
        len(react(seq.replace(c, "").replace(c.upper(), "")))
        for c in string.ascii_lowercase
    )
