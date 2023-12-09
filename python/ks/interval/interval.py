# pyright: strict
import typing

import dataclasses


@dataclasses.dataclass(init=False, frozen=True)
class Interval:
    l: int
    r: int

    Like = typing.Self | tuple[int, int]

    @typing.overload
    def __init__(self, i: tuple[int, int], /) -> None:
        ...

    @typing.overload
    def __init__(self, l: int, r: int | None = None, /) -> None:
        ...

    def __init__(self, l_or_i: int | tuple[int, int], r: int | None = None, /) -> None:
        match l_or_i:
            case int() as l:
                object.__setattr__(self, "l", l)
                object.__setattr__(self, "r", l if r is None else r)
            case (int() as l, int() as r):
                object.__setattr__(self, "l", l)
                object.__setattr__(self, "r", r)

    def __eq__(self, other: object) -> bool:
        match other:
            case Interval(l, r) | (int() as l, int() as r):
                return self.l == l and self.r == r
            case _:
                return False

    def __hash__(self) -> int:
        return hash((self.l, self.r))

    def ints(self) -> typing.Iterable[int]:
        return range(self.l, self.r + 1)

    def replace(self, l: int | None = None, r: int | None = None):
        if l is None:
            l = self.l
        if r is None:
            r = self.r
        return type(self)(l, r)

    def truncate(self, l: int | None = None, r: int | None = None):
        l = self.l if l is None else max(l, self.l)
        r = self.r if r is None else min(r, self.r)
        return type(self)(l, r)

    def shrink(self, l: int | None = None, r: int | None = None):
        l = self.l if l is None else self.l + l
        r = self.r if r is None else self.r - r
        return type(self)(l, r)

    def expand(self, l: int | None = None, r: int | None = None):
        l = self.l if l is None else self.l - l
        r = self.r if r is None else self.r + r
        return type(self)(l, r)

    def __contains__(self, other: int | Like) -> bool:
        match other:
            case int():
                return self.l <= other <= self.r
            case Interval(l, r) | (l, r):
                return self.l <= l and r <= self.r

    def __and__(self, other: int | Like) -> typing.Self | None:
        match other:
            case Interval(l, r) | (l, r) | ((int() as l) as r):
                ll, rr = max(l, self.l), min(r, self.r)
                return None if ll > rr else Interval(ll, rr)

    def __or__(self, other: int | Like) -> typing.Self | None:
        match other:
            case Interval(l, r) | (l, r) | ((int() as l) as r):
                return Interval(min(l, self.l), max(r, self.r))
