import typing
import collections.abc as cabc
import re


class Parser[A](typing.Protocol):
    def parse(self, s: str, /) -> A:
        ...

    def map[B](self, f: cabc.Callable[[A], B]) -> "Map"[A, B]:
        return Map(f, self)


class Map[A, B](Parser[B]):
    _p: Parser[A]
    _f: cabc.Callable[[A], B]

    def __init__(self, f: cabc.Callable[[A], B], p: Parser[A]):
        self._f = f
        self._p = p

    def parse(self, s: str, /):
        return self._f(self._p.parse(s))


class Pair[A, B](Parser[tuple[A, B]]):
    _pa: Parser[A]
    _qb: Parser[B]

    def __init__(self, pa: Parser[A], pb: Parser[B]):
        self._pa = pa
        self._pb = pb

    def parse(self, s: str, /):
        return (self._pa.parse(s), self._pb.parse(s))


class Split(Parser[list[str]]):
    _sep: str | None
    _maxsplit: int

    def __init__(self, sep: str | None = None, maxsplit: int = -1):
        self._sep = sep
        self._maxsplit = maxsplit

    def parse(self, s: str, /):
        return s.split(self._sep, self._maxsplit)


class Strip(Parser[str]):
    _delim: str | None = None

    def __init__(self, delim: str | None = None, /):
        self._delim = delim

    def parse(self, s: str, /):
        return s.strip(self._delim)


class Grep(Parser[list[str]]):
    _pattern: re.Pattern[str]

    def __init__(self, pattern: str, /):
        self._pattern = re.compile(pattern)

    def parse(self, s: str, /):
        m = self._pattern.findall(s)
        if not m:
            raise ValueError(
                f"grep parser failed to match: pattern={self._pattern!r}, text={s!r}"
            )
        return [*map(str, m)]
