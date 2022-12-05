# pyright: strict

import typing
import re

# patterns mostly taken from <https://docs.python.org/3/library/re.html#simulating-scanf>
regexps: dict[str, tuple[typing.Callable[[str], typing.Any], re.Pattern[str]]] = {
    "d": (int, re.compile(r"[+-]?\d+")),
    "u": (int, re.compile(r"\d+")),
    "s": (str, re.compile(r"\S+")),
    "f": (float, re.compile(r"[+-]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?")),
}


def parse(
    pat: str,
) -> typing.Iterator[
    str | tuple[str, typing.Callable[[str], typing.Any], re.Pattern[str]]
]:
    buf: list[str] = []

    escape = False
    for c in pat:
        if escape:
            escape = False
            if c == "%":
                buf.append("%")
                continue

            if buf:
                yield "".join(buf)
                buf = []

            if c not in regexps:
                raise ValueError(f"invalid escape code {c!r} in pattern {pat!r}")

            yield (c, *regexps[c])

            continue

        if c == "%":
            escape = True
            continue

        buf.append(c)

    if buf:
        yield "".join(buf)


def compile(pat: str) -> typing.Callable[[str], typing.Iterator[typing.Any]]:
    terms = [*parse(pat)]

    def run(input: str):
        pos = 0
        for term in terms:
            match term:
                case (c, conv, r):
                    m = r.match(input, pos)
                    assert (
                        m
                    ), f"failed to match token %{c} at position {pos} in {input!r}"
                    s = m.group(0)
                    pos += len(s)
                    yield conv(s)

                case str():
                    assert input.startswith(
                        term, pos
                    ), f"failed to match literal {term!r} at position {pos} in {input!r}"
                    pos += len(term)

    return run
