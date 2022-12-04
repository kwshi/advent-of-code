# pyright: strict

import typing

import re
import dataclasses

re_int = re.compile(r"[+-]?\d+")
re_uint = re.compile(r"\d+")
re_word = re.compile(r"\S+")


@dataclasses.dataclass
class TermLiteral:
    s: str


@dataclasses.dataclass
class TermInt:
    pass


@dataclasses.dataclass
class TermIntUnsigned:
    pass


@dataclasses.dataclass
class TermWord:
    pass


Term = TermLiteral | TermInt | TermIntUnsigned | TermWord


def parse(pat: str) -> typing.Iterator[Term]:
    buf: list[str] = []

    escape = False
    for c in pat:
        if escape:
            escape = False
            if c == "%":
                buf.append("%")
                continue

            if buf:
                yield TermLiteral("".join(buf))
                buf = []

            match c:
                case "d":
                    yield TermInt()

                case "u":
                    yield TermIntUnsigned()

                case "s":
                    yield TermWord()

                case _:
                    raise ValueError(f"invalid escape code {c!r} in pattern {pat!r}")

            continue

        if c == "%":
            escape = True
            continue

        buf.append(c)

    if buf:
        yield TermLiteral("".join(buf))


def compile(pat: str) -> typing.Callable[[str], typing.Iterator[typing.Any]]:
    terms = [*parse(pat)]

    def run(input: str):
        pos = 0
        for term in terms:
            match term:

                case TermLiteral(lit):
                    assert input.startswith(
                        lit, pos
                    ), f"failed to match literal {lit!r} at position {pos} in {input!r}"
                    pos += len(lit)

                case TermInt():
                    m = re_int.match(input, pos)
                    assert m, f"failed to match int at position {pos} in {input!r}"
                    s = m.group(0)
                    pos += len(s)
                    yield int(s)

                case TermIntUnsigned():
                    m = re_uint.match(input, pos)
                    assert m, f"failed to match uint at position {pos} in {input!r}"
                    s = m.group(0)
                    pos += len(s)
                    yield int(s)

                case TermWord():
                    m = re_word.match(input, pos)
                    assert m, f"failed to match word at position {pos} in {input!r}"
                    s = m.group(0)
                    pos += len(s)
                    yield s

    return run
